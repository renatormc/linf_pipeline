from datetime import datetime, timedelta
from sqlalchemy import and_
from typing import Iterator
from models import Case, Equipment, Object, Step, db_session
from models import Worker
import time

from repo import get_finished_executing, get_waiting_equipment, move_next_step, number_of_vacancies



def interval_iterator(data_inicial: datetime, data_final: datetime, sleep_interval: int | None = None) -> Iterator[datetime]:
    data = data_inicial
    while data < data_final:
        yield data
        data += timedelta(minutes=1)
        if sleep_interval:
            time.sleep(sleep_interval)


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
        Object.status == "RUNNING",
        Object.start_current_step_executing + Object.duration_current_step <= time
    )
    for object in query.all():
        print(f"Finishing object {object.id}")
        object.current_step = None
        object.status = "FINISHED"
        object.start_current_step_executing = None
        db_session.add(object)
    if commit:
        db_session.commit()
        
        
def update_pipeline(time: datetime) -> None:
    finish_objects_at_end_step(time)
    query = db_session.query(Equipment).order_by(Equipment.order.desc())
    for equipment in query.all():
        print(f"Analising equipment {equipment}")
        objects = get_waiting_equipment(equipment, time, number_of_vacancies(equipment))
        for object in objects:
            move_next_step(object, time)


def simular_atual() -> None:
# inicio = datetime(2024, 1, 1, 0, 0, 0)
# fim = datetime(2024, 12, 31, 23, 59, 59)
# for time in interval_iterator(inicio, fim, 1):
#     checar_tarefas_finalizadas(time)
#     iniciar_novas_tarefas(time)
    pass

def simular_pipeline() -> None:
    inicio= datetime(2024, 1, 1, 0, 0, 0)
    fim= datetime(2024, 12, 31, 23, 59, 59)
    for time in interval_iterator(inicio, fim, 1):
        update_pipeline(time)
