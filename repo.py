from datetime import datetime
from typing import Iterable
import logging
from sqlalchemy import and_, or_
from sqlalchemy.orm import Session
from custom_type import SIM_METHOD
from models import Case, Equipment, Object, Step, Worker


def get_object_step(object: Object, name: str, db_session: Session) -> Step:
    query = db_session.query(Step).where(
        Step.object == object,
        Step.name == name
    )
    return query.one()


def count_objects_on_buffer(equipment: Equipment, db_session: Session) -> int:
    query = db_session.query(Object).where(
        Object.case.has(Case.method == equipment.method),
        Object.current_location == equipment.name,
        Object.status == "BUFFER"
    )
    return query.count()


def count_objects_executing(equipment: Equipment, db_session: Session) -> int:
    query = db_session.query(Object).where(
        Object.current_location == equipment.name,
        Object.status == "RUNNING",
        Object.case.has(Case.method == equipment.method)
    )
    return query.count()


def count_total_objects(equipment: Equipment, db_session: Session) -> int:
    query = db_session.query(Object).where(
        Object.current_location == equipment.name,
        Object.case.has(Case.method == equipment.method)
    )

    return query.count()


def number_of_vacancies(equipment: Equipment, db_session: Session) -> int:
    return equipment.capacity - count_total_objects(equipment, db_session)

# def number_of_free_instances(equipment: Equipment) -> int:


def move_next_step(object: Object, db_session: Session, commit=True) -> None:
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


def get_waiting_equipment(equipment: Equipment, time: datetime, limit: int, db_session: Session) -> Iterable[Object]:
    query = db_session.query(Object).where(
        Object.case.has(Case.method == equipment.method),
        Object.next_step == equipment.name,
        or_(
            and_(Object.status == "RUNNING", Object.start_current_step_executing + Object.duration_current_step <= time),
            Object.status == "INITIAL"
        )
    )
    if equipment.method == "current":
        query = query.where(Object.case.has(Case.worker_id != None))
    query = query.order_by(Object.case_id).limit(limit)
    return query.all()


# def get_waiting_equipment_on_workers_desk(equipment: Equipment, limit: int, db_session: Session) -> Iterable[Object]:
#     query = db_session.query(Object).where(
#         Object.case.has(Case.method == equipment.method),
#         Object.current_location == "WORKER_DESK",
#         Object.next_step == equipment.name
#     ).order_by(Object.case_id).limit(limit)
#     return query.all()


def get_finished_executing(equipment: Equipment, time: datetime, db_session: Session) -> list[Object]:
    query = db_session.query(Object).where(
        Object.case.has(Case.method == equipment.method),
        Object.current_location == equipment.name,
        Object.status == "RUNNING",
        Object.start_current_step_executing + Object.duration_current_step <= time
    ).order_by(Object.case_id)
    return query.all()


def count_finished_cases(method: SIM_METHOD, db_session: Session) -> int:
    query = db_session.query(Case).where(
        Case.method == method,
        ~Case.objects.any(Object.status != "FINISHED")
    )
    return query.count()


def count_cases_running(method: SIM_METHOD, db_session: Session) -> int:
    query = db_session.query(Case).where(
        Case.method == method,
        Case.objects.any(Object.status == "RUNNING")
    )
    return query.count()


def count_finished_objects(method: SIM_METHOD, db_session: Session) -> int:
    query = db_session.query(Object).where(
        Object.case.has(Case.method == method),
        Object.status == "FINISHED"
    )
    return query.count()


def count_objects_in_equipments(method: SIM_METHOD, db_session: Session, name: str) -> int:
    query = db_session.query(Object).where(
        Object.case.has(Case.method == method),
        Object.current_location == name,
        Object.status == "RUNNING"
    )
    return query.count()


def get_next_case(method: SIM_METHOD, db_session: Session) -> Case | None:
    query = db_session.query(Case).where(
        Case.method == method,
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

    # for step in db_session.query(Step).all():
    #     db_session.delete(step)
    # db_session.commit()

    for case_ in db_session.query(Case).all():
        db_session.delete(case_)
    db_session.commit()


def get_equipments_names(db_session: Session) -> list[str]:
    query = db_session.query(Equipment.name).where(Equipment.method == "pipeline")
    return [item[0] for item in query.all()]
