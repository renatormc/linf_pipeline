from datetime import datetime, timedelta
from sqlalchemy import and_
from typing import Iterable, Iterator
from models import Objeto, Pericia, Etapa, db_session
from models import Perito
import time


def interval_iterator(data_inicial: datetime, data_final: datetime, sleep_interval: int | None = None) -> Iterator[datetime]:
    data = data_inicial
    while data < data_final:
        yield data
        data += timedelta(minutes=1)
        if sleep_interval:
            time.sleep(sleep_interval)


def get_perito_disponivel() -> Perito | None:
    query = db_session.query(Perito).where(
        Perito.pericias.any(and_(
            Pericia.comeco != None,
            Pericia.fim == None

        ))
    )
    return query.first()






# def get_tarefa_com_recursos_disponiveis() -> Etapa | None:
#     query = db_session.query(Etapa).where(
#         ~Etapa.recursos_necessarios.any(~TipoRecurso.recursos.any(Recurso.tarefa_id == None))
#     ).join(Etapa.objeto).join(Objeto.pericia).order_by(Pericia.id)
#     return query.first()


# def iniciar_tarefa(tarefa: Etapa, current_time: datetime) -> None:
#     print(f"Iniciando tarefa {tarefa.nome}")
#     for tipo in tarefa.recursos_necessarios:
#         recurso = db_session.query(Recurso).where(
#             Recurso.tipo_id == tipo.id,
#             Recurso.tarefa_id == None
#         ).one()
#         recurso.tarefa = tarefa
#         db_session.add(recurso)
#     tarefa.comeco = current_time
#     tarefa.fim = current_time + timedelta(seconds=tarefa.duracao)
#     db_session.add(tarefa)
#     db_session.commit()


# def checar_tarefas_finalizadas(current_time: datetime) -> None:
#     query = db_session.query(Etapa).where(
#         Etapa.fim <= current_time
#     )
#     for tarefa in query.all():
#         for recurso in tarefa.recursos:
#             recurso.tarefa = None
#             db_session.add(recurso)
#         db_session.add(tarefa)
#     db_session.commit()


# def iniciar_novas_tarefas(current_time: datetime) -> None:
#     while True:
#         tarefa = get_tarefa_com_recursos_disponiveis()
#         if not tarefa:
#             break
#         iniciar_tarefa(tarefa, current_time)


def simular_atual() -> None:
    # inicio = datetime(2024, 1, 1, 0, 0, 0)
    # fim = datetime(2024, 12, 31, 23, 59, 59)
    # for time in interval_iterator(inicio, fim, 1):
    #     checar_tarefas_finalizadas(time)
    #     iniciar_novas_tarefas(time)
    pass
