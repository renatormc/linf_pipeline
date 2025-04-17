from datetime import datetime, timedelta
from sqlalchemy import and_
from typing import Iterator, Literal
import logging
from tqdm import tqdm
from models import Case, DBSession, Equipment, Object
from models import Worker
import time
from sqlalchemy.orm import Session
from repo import count_finished_cases, count_finished_objects, count_objects_executing, \
    get_next_case, get_object_step, get_waiting_equipment, get_waiting_equipment_on_workers_desk, \
    move_next_step, number_of_vacancies
from term import CustomTerminal


class IntervalIterator:
    def __init__(self, data_inicial: datetime, data_final: datetime, delta: timedelta, sleep_interval: int | None = None):
        self.data_inicial = data_inicial
        self.data_final = data_final
        self.delta = delta
        self.sleep_interval = sleep_interval
        self.current = data_inicial
        self.steps = int((self.data_final - self.data_inicial)/self.delta)

    def __iter__(self) -> Iterator[datetime]:
        return self

    def __next__(self) -> datetime:
        if self.current >= self.data_final:
            raise StopIteration
        result = self.current
        self.current += self.delta
        if self.sleep_interval:
            time.sleep(self.sleep_interval)
        return result


def get_perito_disponivel(db_session: Session) -> Worker | None:
    query = db_session.query(Worker).where(
        Worker.cases.any(and_(
            Case.start != None,
            Case.end == None

        ))
    )
    return query.first()


def finish_objects_at_end_step(time: datetime, db_session: Session, remove_from_equipment=False, commit=True) -> None:
    query = db_session.query(Object).where(
        Object.next_step == None,
        Object.status == "RUNNING",
        Object.start_current_step_executing + Object.duration_current_step <= time
    )
    for object in query.all():
        logging.info(f"Finishing object {object.id}")
        object.current_location = None
        object.status = "FINISHED"
        object.start_current_step_executing = None
        if remove_from_equipment:
            object.current_location = "WORKER_DESK"
        db_session.add(object)
    if commit:
        db_session.commit()


def start_executing(equipment: Equipment, time: datetime, db_session: Session) -> None:
    n = equipment.lenght - count_objects_executing(equipment, db_session)
    query = db_session.query(Object).where(
        Object.current_location == equipment.name,
        Object.status == "BUFFER"
    ).order_by(Object.case_id).limit(n)
    for object in query.all():
        logging.info(f"Starting executing {object} on {equipment}")
        object.status = "RUNNING"
        object.start_current_step_executing = time
        db_session.add(object)
    db_session.commit()


def update_pipeline(time: datetime, db_session: Session) -> None:
    finish_objects_at_end_step(time, db_session)
    query = db_session.query(Equipment).order_by(Equipment.order.desc())
    for equipment in query.all():
        logging.info(f"Analysing equipment {equipment}")
        n = number_of_vacancies(equipment, db_session)
        objects = get_waiting_equipment(equipment, time, n, db_session)
        for object in objects:
            move_next_step(object, db_session)
        start_executing(equipment, time, db_session)


start_of_day = datetime.strptime("08:00", "%H:%M").time()
start_of_lunch = datetime.strptime("12:00", "%H:%M").time()
end_of_lunch = datetime.strptime("13:00", "%H:%M").time()
end_of_day = datetime.strptime("17:00", "%H:%M").time()


def is_working_time(time: datetime) -> bool:
    if time.weekday() in [5, 6]:
        return False
    t = time.time()
    if t >= start_of_day and t < start_of_lunch:
        return True
    if t >= end_of_lunch and t < end_of_day:
        return True
    return False


def update_current(time: datetime, db_session: Session) -> None:
    finish_objects_at_end_step(time, db_session, remove_from_equipment=True)
    if not is_working_time(time):
        return
    # Get free workers
    query = db_session.query(Worker).where(
        ~Worker.cases.any(Case.objects.any(Object.status != "FINISHED"))
    )
    for worker in query.all():
        c = get_next_case(db_session)
        if c:
            c.worker = worker
            for obj in c.objects:
                obj.current_location = "WORKER_DESK"
            db_session.add(c)
            db_session.commit()

    query2 = db_session.query(Equipment).order_by(Equipment.order)
    for equipment in query2.all():
        logging.info(f"Analysing equipment {equipment}")
        n = equipment.lenght - count_objects_executing(equipment, db_session)
        objs = get_waiting_equipment_on_workers_desk(equipment, n, db_session)
        for obj in objs:
            obj.current_location = equipment.name
            step = get_object_step(obj, obj.current_location, db_session)
            obj.next_step = step.next_step
            obj.status = "RUNNING"
            obj.start_current_step_executing = time
            db_session.add(obj)
    db_session.commit()


def simulate_lab(type: Literal['pipeline', 'current']) -> None:
    term = CustomTerminal()
    with term.fullscreen(), term.hidden_cursor(), DBSession() as db_session:
        inicio = datetime(2024, 1, 1, 0, 0, 0)
        fim = datetime(2024, 1, 31, 23, 59, 59)
        iter = IntervalIterator(inicio, fim, timedelta(minutes=30))
        for i, time in enumerate(iter):
            if type == 'pipeline':
                update_pipeline(time, db_session)
            else:
                update_current(time, db_session)
            term.draw_screen(time, count_finished_objects(db_session), count_finished_cases(db_session), (i+1)/iter.steps, db_session)


def print_stats() -> None:
    term = CustomTerminal()
    with term.fullscreen(), term.hidden_cursor(), DBSession() as db_session:
        term.draw_screen(None, count_finished_objects(db_session), count_finished_cases(db_session), None, db_session)
        input()


