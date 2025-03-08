from datetime import datetime, timedelta
from sqlalchemy import and_, func, or_, select
from typing import Iterable, Iterator
from models import Equipment, Object, Case, Step, db_session
from models import Worker
import time

from repo import finish_object


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



def finish_objects_at_end_step(time: datetime) -> None:
    query = db_session.query(Step).where(
        Step.next_step == None,
        Step.start != None, 
        Step.start + Step.duration <= time
    )
    for step in query.all():
        finish_object(step, time, commit=False)
    db_session.commit()


def change_equipments(time: datetime) -> None:
    query = db_session.query(Equipment).order_by(Equipment.order.desc())
    for eq in query.all():
        
        steps = get_steps_executing_expired(eq, time)
        for step in steps:




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
        atualizar_pipeline(time)
