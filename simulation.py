from datetime import datetime, timedelta
from sqlalchemy import and_
from typing import Iterator
import logging
from tqdm import tqdm
from models import Case, Equipment, Object, Step, db_session
from models import Worker
import time

from repo import count_finished_cases, count_finished_objects, count_objects_executing, get_waiting_equipment, move_next_step, number_of_vacancies


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


def get_perito_disponivel() -> Worker | None:
    query = db_session.query(Worker).where(
        Worker.cases.any(and_(
            Case.start != None,
            Case.end == None

        ))
    )
    return query.first()


def finish_objects_at_end_step(time: datetime, commit=True) -> None:
    query = db_session.query(Object).where(
        Object.next_step == None,
        Object.status == "EXECUTING",
        Object.start_current_step_executing + Object.duration_current_step <= time
    )
    for object in query.all():
        logging.info(f"Finishing object {object.id}")
        object.current_step = None
        object.status = "FINISHED"
        object.start_current_step_executing = None
        db_session.add(object)
    if commit:
        db_session.commit()


def start_executing(equipment: Equipment, time: datetime) -> None:
    n = equipment.capacity - count_objects_executing(equipment)
    query = db_session.query(Object).where(
        Object.current_step == equipment.name,
        Object.status == "BUFFER"
    ).order_by(Object.case_id).limit(n)
    for object in query.all():
        logging.info(f"Starting executing {object} on {equipment}")
        object.status == "EXECUTING"
        object.start_current_step_executing = time
        db_session.add(object)
    db_session.commit()


def update_pipeline(time: datetime) -> None:
    finish_objects_at_end_step(time)
    query = db_session.query(Equipment).order_by(Equipment.order.desc())
    for equipment in query.all():
        logging.info(f"Analysing equipment {equipment}")
        objects = get_waiting_equipment(equipment, time, number_of_vacancies(equipment))
        for object in objects:
            move_next_step(object, time)
        start_executing(equipment, time)


def simular_atual() -> None:
    pass


def simular_pipeline() -> None:
    inicio = datetime(2024, 1, 1, 0, 0, 0)
    # fim = datetime(2024, 12, 31, 23, 59, 59)
    fim = datetime(2024, 1, 31, 23, 59, 59)
    iter = IntervalIterator(inicio, fim, timedelta(minutes=30))
    with tqdm(total=iter.steps) as pbar:
        for i, time in enumerate(iter):
            pbar.update(1)
            update_pipeline(time)
    print(f"Cases finished: {count_finished_cases()}")
    print(f"Objects finished: {count_finished_objects()}")
