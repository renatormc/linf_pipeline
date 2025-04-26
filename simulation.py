from dataclasses import dataclass
from datetime import datetime, timedelta
from sqlalchemy import and_, func
from typing import Iterator
import logging
from config import DB_USER
import config
from custom_type import SIM_METHOD, TimeValue
from models import Case, Equipment, Object
from models import Worker
import time
from sqlalchemy.orm import Session
from repo import count_objects_executing,    get_next_case, get_waiting_equipment,    move_next_step, number_of_vacancies





class IntervalIterator:
    def __init__(self, data_inicial: datetime, data_final: datetime, delta: timedelta, sleep_interval: int | None = None):
        self.data_inicial = data_inicial
        self.data_final = data_final
        self.delta = delta
        self.sleep_interval = sleep_interval
        self.current = data_inicial
        self.steps = int((self.data_final - self.data_inicial)/self.delta)

    def __iter__(self) -> Iterator[TimeValue]:
        return self

    def __next__(self) -> TimeValue:
        if self.current >= self.data_final:
            raise StopIteration

        result = TimeValue(time=self.current, day_sequence=(self.current.date() - self.data_inicial.date()).days % 4)
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


def finish_objects_at_end_step(method: SIM_METHOD, time: TimeValue, db_session: Session, commit=True) -> None:
    query = db_session.query(Object).where(
        Object.case.has(Case.method == method),
        Object.next_step == None,
        Object.status == "RUNNING",
        Object.start_current_step_executing + Object.duration_current_step <= time.time
    )
    if method == "current":
        query = query.where(Object.case.has(Case.worker.has(Worker.day_sequence == time.day_sequence)))
    for object in query.all():
        logging.info(f"Finishing object {object.id}")
        object.current_location = None
        object.status = "FINISHED"
        object.start_current_step_executing = None
        db_session.add(object)
    if commit:
        db_session.commit()


def start_executing(equipment: Equipment, time: TimeValue, db_session: Session) -> None:
    n = equipment.lenght - count_objects_executing(equipment, db_session)
    query = db_session.query(Object).where(
        Object.case.has(Case.method == equipment.method),
        Object.current_location == equipment.name,
        Object.status == "BUFFER"
    )
    if equipment.method == "current" and config.TODOS_NO_PLANTAO:
        query = query.where(Object.case.has(Case.worker.has(Worker.day_sequence == time.day_sequence)))
    query = query.order_by(Object.case_id).limit(n)
    for object in query.all():
        logging.info(f"Starting executing {object} on {equipment}")
        object.status = "RUNNING"
        object.start_current_step_executing = time.time
        db_session.add(object)
    db_session.commit()


def worker_finish_cases(db_session: Session) -> None:
    query = db_session.query(Case).where(
        Case.worker_id != None,
        Case.method == "current",
        ~Case.objects.any(Object.status != "FINISHED")
    )
    for c in query.all():
        c.worker_id = None
        db_session.add(c)
    db_session.commit()


def update_lab(method: SIM_METHOD, time: TimeValue, db_session: Session) -> None:
    finish_objects_at_end_step(method, time, db_session)
    worker_finish_cases(db_session)
    if method == "current" and config.TODOS_NO_PLANTAO:
        atribuir_novas(db_session)
    query = db_session.query(Equipment).where(Equipment.method == method).order_by(Equipment.order.desc())
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


def atribuir_novas(db_session: Session) -> None:
    query = db_session.query(Worker).outerjoin(Worker.cases) \
        .group_by(Worker.id) \
        .having(func.count(Case.id) < config.MAX_CASES_PER_WORKER)
    for worker in query.all():
        c = get_next_case("current", db_session)
        if c:
            c.worker = worker
            db_session.add(c)
            db_session.commit()
