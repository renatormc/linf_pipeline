from datetime import datetime, timedelta
from sqlalchemy import and_, or_
from typing import Iterable, Iterator
from models import Equipamento, Objeto, Pericia, db_session
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


def checar_andamento_equipamento(equipamento: Equipamento, tempo: datetime) -> None:
    query = db_session.query(Objeto).where(
        Objeto.etapa == equipamento.nome,
    )
    for obj in query.all():
        obj.atualizar_status(tempo)
        db_session.add(obj)
    db_session.commit()


def get_finalizadas_equipamento(equipamento: Equipamento, tempo: datetime) -> Iterable[Objeto]:
    query = db_session.query(Objeto).where(
        Objeto.etapa == equipamento.nome,
        Objeto.status == "AGUARDANDO_PROXIMA_ETAPA"
    ).order_by(Objeto.pericia_id)
    return query.all()


# def get_objetos_no_buffer(equipamento: Equipamento) -> Iterable[Objeto]:
#     query = db_session.query(Objeto).where(
#         Objeto.etapa == equipamento.nome,
#         Objeto.status == "BUFFER"
#     ).order_by(Objeto.pericia_id)
#     return query.all()


def atualizar_numeros_equipamento(equipamento: Equipamento) -> None:
    equipamento.aguardando = db_session.query(Objeto).where(
        Objeto.etapa == equipamento.nome,
        Objeto.status == "BUFFER"
    ).count()
    equipamento.executando = db_session.query(Objeto).where(
        Objeto.etapa == equipamento.nome,
        or_(Objeto.status == "EXECUTANDO", Objeto.status == "AGUARDANDO_PROXIMA_ETAPA")
    ).count()
    db_session.add(equipamento)
    db_session.commit()
    


def iniciar_novas_equipamento(equipamento: Equipamento, tempo: datetime) -> None:
    n = equipamento.capacidade - equipamento.executando
    if n > equipamento.aguardando:
        n = equipamento.aguardando
    query = db_session.query(Objeto).where(
        Objeto.etapa == equipamento.nome,
        Objeto.status == "BUFFER"
    ).limit(n).order_by(Objeto.pericia_id)
    for objeto in query.all():
        etapa = db_session.query(Etapa)



def puxar_para_equipamento(equipamento: Equipamento) -> None:
    query = db_session.query(Objeto).where(
        Objeto.proxima_etapa == equipamento.nome,
        Objeto.status == "AGUARDANDO_PROXIMA_ETAPA"
    ) \
        .order_by(Objeto.pericia_id) \
        .limit(contar_livre_equipamento(equipamento))
    n = query.count()
    for objeto in query.all():
        print(f"Puxando objeto {objeto.id} para equipamento {equipamento.nome}")
        objeto.status = "BUFFER"
        objeto.etapa = equipamento.nome
        db_session.add(objeto)
    db_session.add(equipamento)
    db_session.commit()
    

def checar_objetos_finalizados(tempo: datetime) -> None:
    query = db_session.query(Objeto).where(
        Objeto.proxima_etapa == None,
        Objeto.status == "EXECUTANDO",
    )
    for objeto in query.all():
        print(f"Finalizando objeto {objeto.id}")
        objeto.status = "FINALIZADO"
        objeto.fim = tempo
        objeto.etapa = None
        db_session.add(objeto)
    db_session.commit()


def atualizar_pipeline(tempo: datetime) -> None:
    for equipamento in db_session.query(Equipamento).all():
        checar_andamento_equipamento(equipamento, tempo)
    checar_objetos_finalizados(tempo)
    while True:
        query = db_session.query(Equipamento).where(
            Equipamento.livre > 0
        )
        eq = query.first()
        if not eq:
            break
        puxar_para_equipamento(eq)
        iniciar_novas_equipamento(eq, tempo)



def simular_atual() -> None:
    # inicio = datetime(2024, 1, 1, 0, 0, 0)
    # fim = datetime(2024, 12, 31, 23, 59, 59)
    # for time in interval_iterator(inicio, fim, 1):
    #     checar_tarefas_finalizadas(time)
    #     iniciar_novas_tarefas(time)
    pass

def simular_pipeline() -> None:
    inicio = datetime(2024, 1, 1, 0, 0, 0)
    fim = datetime(2024, 12, 31, 23, 59, 59)
    for time in interval_iterator(inicio, fim, 1):
        atualizar_pipeline(time)
        