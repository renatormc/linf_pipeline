from datetime import datetime
from typing import Iterable
import logging
from sqlalchemy import and_, or_
from sqlalchemy.orm import Session
import config
from custom_type import SIM_METHOD, TimeValue
from models import Case, Equipment, Object, Step, Worker
from sheets import Planilha



def get_object_step(object: Object, name: str, db_session: Session) -> Step:
    query = db_session.query(Step).where(
        Step.object == object,
        Step.name == name
    )
    return query.one()


def countar_objetos_no_buffer_do_equipamento(equipment: Equipment, db_session: Session) -> int:
    query = db_session.query(Object).where(
        Object.current_location == equipment.name,
        Object.status == "BUFFER"
    )
    return query.count()


def contar_objetos_executando_no_equipamento(equipment: Equipment, db_session: Session) -> int:
    query = db_session.query(Object).where(
        Object.current_location == equipment.name,
        Object.status == "RUNNING",
    )
    return query.count()


def total_objetos_no_equipamento(equipment: Equipment, db_session: Session) -> int:
    query = db_session.query(Object).where(
        Object.current_location == equipment.name,
    )

    return query.count()


def numero_de_vagas_no_equipamento(equipment: Equipment, db_session: Session) -> int:
    return equipment.capacity - total_objetos_no_equipamento(equipment, db_session)

# def number_of_free_instances(equipment: Equipment) -> int:


def mover_objeto_para_buffer_do_proximo_equipamento(object: Object, db_session: Session, commit=True) -> None:
    if not object.next_step:
        raise Exception("there is not next step")
    next_step = get_object_step(object, object.next_step, db_session)
    object.current_location = next_step.name
    object.status = "BUFFER"
    object.duration_current_step = next_step.duration
    object.next_step = next_step.next_step
    db_session.add(object)
    logging.info(f"Moving {object} to {next_step.name}")
    if commit:
        db_session.commit()


def objetos_aguardando_equipamento(equipment: Equipment, time: TimeValue, limit: int, db_session: Session, pla: Planilha) -> Iterable[Object]:
    query = db_session.query(Object).where(
        Object.next_step == equipment.name,
        or_(
            and_(Object.status == "RUNNING", Object.start_current_step_executing + Object.duration_current_step <= time.time),
            Object.status == "INITIAL"
        )
    )
    if pla.vars.regime == "individual":
        query = query.where(Object.case.has(
            Case.worker_id != None,
            # ~Case.worker.has(
            #     Worker.cases.any(
            #         ~Case.objects.any(Object.status != "FINISHED")
            #     )
            # )
        ))
        if pla.vars.horario_trabalho == "Plantão":
            query = query.where(Object.case.has(Case.worker.has(Worker.day_sequence == time.day_sequence)))
    query = query.order_by(Object.case_id).limit(limit)
    return query.all()


def objetos_que_terminaram_de_executar(equipment: Equipment, time: datetime, db_session: Session) -> list[Object]:
    query = db_session.query(Object).where(
        Object.current_location == equipment.name,
        Object.status == "RUNNING",
        Object.start_current_step_executing + Object.duration_current_step <= time
    ).order_by(Object.case_id)
    return query.all()


def contar_casos_finalizados( db_session: Session) -> int:
    query = db_session.query(Case).where(
        ~Case.objects.any(Object.status != "FINISHED")
    )
    return query.count()


def contar_casos_em_andamento(db_session: Session, plan: Planilha) -> int:
    if plan.vars.regime == "individual":
        return db_session.query(Case).where(
            Case.worker_id != None
        ).count()
    query = db_session.query(Case).where(
        Case.objects.any(Object.status == "RUNNING")
    )
    return query.count()


def contar_objetos_finalizados(db_session: Session) -> int:
    query = db_session.query(Object).where(
        Object.status == "FINISHED"
    )
    return query.count()


def contar_objetos_no_equipamento(db_session: Session, name: str) -> int:
    query = db_session.query(Object).where(
        Object.current_location == name,
        Object.status == "RUNNING"
    )
    return query.count()


def proxima_pericia( db_session: Session) -> Case | None:
    query = db_session.query(Case).where(
        ~Case.objects.any(Object.status != "INITIAL"),
        Case.worker_id == None
    ).order_by(Case.id)
    return query.first()


def clear_db(db_session: Session) -> None:
    for equipment in db_session.query(Equipment).all():
        db_session.delete(equipment)
    db_session.commit()

    for per in db_session.query(Worker).all():
        db_session.delete(per)
    db_session.commit()

    for case_ in db_session.query(Case).all():
        db_session.delete(case_)
    db_session.commit()


def nomes_dos_equipamentos(db_session: Session) -> list[str]:
    query = db_session.query(Equipment.name)
    return [item[0] for item in query.all()]
