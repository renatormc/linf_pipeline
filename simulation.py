from datetime import datetime, timedelta
from sqlalchemy import and_
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
        Objeto.status == "EXECUTANDO",
        Objeto.fim == None
    )
    for obj in query.all():
        obj.fim = tempo
        obj.status = "AGUARDANDO_PROXIMA_ETAPA"
        db_session.add(obj)
    db_session.commit()

def contar_buffer_equipamento(equipamento: Equipamento) -> int:
    query = db_session.query(Objeto).where(
        Objeto.etapa == equipamento.nome,
        Objeto.status == "BUFFER"
    )
    return query.count()

def contar_executando_equipamento(equipamento: Equipamento) -> int:
    query = db_session.query(Objeto).where(
        Objeto.etapa == equipamento.nome,
        Objeto.status == "EXECUTANDO"
    )
    return query.count()

def contar_livre_equipamento(equipamento: Equipamento) -> int:
    return equipamento.capacidade - contar_executando_equipamento(equipamento) - contar_buffer_equipamento(equipamento)


def iniciar_novas_equipamento(equipamento: Equipamento, tempo: datetime) -> None:
    n_executando = contar_executando_equipamento(equipamento)
    vagas = equipamento.capacidade - n_executando
    query = db_session.query(Objeto).where(
        Objeto.etapa == equipamento.nome,
        Objeto.status == "BUFFER"
    ).limit(vagas).order_by(Objeto.pericia_id)
    for obj in query.all():
        print(f"Iniciando objeto {obj.id} no equipamento {equipamento.nome}")
        obj.status = "EXECUTANDO"
        obj.comeco = tempo
        db_session.add(obj)
    db_session.commit()



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
        