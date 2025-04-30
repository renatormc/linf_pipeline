from datetime import datetime, timedelta
from sqlalchemy import and_, func
from typing import Iterator
import logging
from custom_type import SIM_METHOD, TimeValue
from models import Case, DBSession, Equipment, Object, Step
from models import Worker
import time
from sqlalchemy.orm import Session
from repo import contar_objetos_executando_no_equipamento,    proxima_pericia, objetos_aguardando_equipamento, \
    mover_objeto_para_buffer_do_proximo_equipamento, numero_de_vagas_no_equipamento
from sheets import Planilha


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


def perito_disponivel(db_session: Session) -> Worker | None:
    query = db_session.query(Worker).where(
        Worker.cases.any(and_(
            Case.start != None,
            Case.end == None

        ))
    )
    return query.first()


def marcar_como_finalizados_objetos_que_finalzaram_etapa(method: SIM_METHOD, time: TimeValue, db_session: Session, plan: Planilha, commit=True) -> None:
    query = db_session.query(Object).where(
        Object.case.has(Case.method == method),
        Object.next_step == None,
        Object.status == "RUNNING",
        Object.start_current_step_executing + Object.duration_current_step <= time.time
    )
    if method == "individual" and plan.vars.horario_individual == "Plantão":
        query = query.where(Object.case.has(Case.worker.has(Worker.day_sequence == time.day_sequence)))
    for object in query.all():
        logging.info(f"Finishing object {object.id}")
        object.current_location = None
        object.status = "FINISHED"
        
        object.start_current_step_executing = None
        db_session.add(object)
    if commit:
        db_session.commit()


def puxar_do_buffer_para_execucao(equipment: Equipment, time: TimeValue, db_session: Session, plan: Planilha) -> None:
    n = equipment.lenght - contar_objetos_executando_no_equipamento(equipment, db_session)
    query = db_session.query(Object).where(
        Object.case.has(Case.method == equipment.method),
        Object.current_location == equipment.name,
        Object.status == "BUFFER"
    )
    if equipment.method == "individual" and plan.vars.horario_individual == "Plantão":
        query = query.where(Object.case.has(Case.worker.has(Worker.day_sequence == time.day_sequence)))
    query = query.order_by(Object.case_id).limit(n)
    for object in query.all():
        logging.info(f"Starting executing {object} on {equipment}")
        object.status = "RUNNING"
        object.start_current_step_executing = time.time
        step = object.get_current_step(db_session)
        step.started_at = time.time
        step.ended_at = step.started_at + step.duration
        if step.order > 0:
            previous_step = db_session.query(Step).where(
                Step.object_id == object.id,
                Step.order == step.order - 1
            ).one()
            if step.started_at and previous_step.ended_at:
                step.waited = step.started_at - previous_step.ended_at
                
        db_session.add(step)
        db_session.add(object)
    db_session.commit()


def tirar_do_nome_do_perito_as_finalizadas(db_session: Session) -> None:
    query = db_session.query(Case).where(
        Case.worker_id != None,
        Case.method == "individual",
        ~Case.objects.any(Object.status != "FINISHED")
    )
    for c in query.all():
        c.worker_id = None
        db_session.add(c)
    db_session.commit()


def update_lab(method: SIM_METHOD, time: TimeValue, db_session: Session, plan: Planilha) -> None:
    if not e_horario_de_trabalho(method, time.time, plan):
        return
    marcar_como_finalizados_objetos_que_finalzaram_etapa(method, time, db_session, plan)
    tirar_do_nome_do_perito_as_finalizadas(db_session)
    if method == "individual":
        atribuir_novas_pericias_aos_peritos_ociosos(time, db_session, plan)
    query = db_session.query(Equipment).where(Equipment.method == method).order_by(Equipment.order.desc())
    for equipment in query.all():
        logging.info(f"Analysing equipment {equipment}")
        n = numero_de_vagas_no_equipamento(equipment, db_session)
        objetos = objetos_aguardando_equipamento(equipment, time, n, db_session, plan)
        for objeto in objetos:
            mover_objeto_para_buffer_do_proximo_equipamento(objeto, db_session)
        puxar_do_buffer_para_execucao(equipment, time, db_session, plan)


start_of_day = datetime.strptime("08:00", "%H:%M").time()
start_of_lunch = datetime.strptime("12:00", "%H:%M").time()
end_of_lunch = datetime.strptime("13:00", "%H:%M").time()
end_of_day = datetime.strptime("17:00", "%H:%M").time()


def e_horario_de_trabalho(method: SIM_METHOD, time: datetime, plan: Planilha) -> bool:
    if (method == "individual" and plan.vars.horario_individual == "Plantão") or (method == "pipeline" and plan.vars.horario_pipeline == "Plantão"):
        return True 
    if time.weekday() in [5, 6]:
        return False
    t = time.time()
    if t >= start_of_day and t < start_of_lunch:
        return True
    if t >= end_of_lunch and t < end_of_day:
        return True
    return False


def atribuir_novas_pericias_aos_peritos_ociosos(time: TimeValue, db_session: Session,  plan: Planilha) -> None:
    query = db_session.query(Worker).outerjoin(Worker.cases) \
        .group_by(Worker.id) \
        .having(func.count(Case.id) < plan.vars.max_pericias_por_perito)
    if plan.vars.horario_individual == "Plantão":
        query = query.having(Worker.day_sequence == time.day_sequence)
    for worker in query.all():
        c = proxima_pericia("individual", db_session)
        if c:
            c.worker = worker
            db_session.add(c)
            db_session.commit()


def print_stats() -> None:
    with DBSession() as db_session:
        res = db_session.query(func.sum(Step.waited)).select_from(Step).where(
            Step.object.has(Object.case.has(Case.method == "individual"))
        ).scalar()
        print(f"Tempo de espera total individual: {res}")
        res = db_session.query(func.sum(Step.waited)).select_from(Step).where(
            Step.object.has(Object.case.has(Case.method == "pipeline"))
        ).scalar()
        print(f"Tempo de espera total pipeline: {res}")
