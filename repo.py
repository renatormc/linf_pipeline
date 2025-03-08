from datetime import datetime
from typing import Iterable

from sqlalchemy import and_, or_
from models import Equipment, Object, Step, db_session


def get_object_step(object: Object, name: str) -> Step:
    query = db_session.query(Step).where(
        Step.object == object,
        Step.name == name
    )
    return query.one()


def count_objects_on_buffer(equipment: Equipment) -> int:
    query = db_session.query(Object).where(
        Object.current_step == equipment.name,
        Object.status == "BUFFER"
    )
    return query.count()


def count_objects_executing(equipment: Equipment) -> int:
    query = db_session.query(Object).where(
        Object.current_step == equipment.name,
        Object.status == "EXECUTING"
    )
    return query.count()


def count_total_objects(equipment: Equipment) -> int:
    query = db_session.query(Object).where(
        Object.current_step == equipment.name,
        or_(Object.status == "EXECUTING", Object.status == "BUFFER")
    )
    return query.count()


def number_of_vacancies(equipment: Equipment) -> int:
    return equipment.buffer + equipment.buffer - count_total_objects(equipment)


def move_next_step(object: Object, commit=True) -> None:
    if not object.next_step:
        raise Exception("there is not next step")
    next_step = get_object_step(object, object.next_step)
    object.current_step = next_step.name
    object.status = "BUFFER"
    object.duration_current_step = next_step.duration
    object.next_step = next_step.next_step
    db_session.add(object)
    if commit:
        db_session.commit()


def get_waiting_equipment(equipment: Equipment, time: datetime, limit: int) -> Iterable[Object]:
    query = db_session.query(Object).where(
        Object.next_step == equipment.name,
        or_(
            and_(Object.status == "EXECUTING", Object.start_current_step_executing + Object.duration_current_step <= time),
            Object.status == "INITIAL"
        )
    ).order_by(Object.case_id).limit(limit)
    return query.all()


def start_waiting_on_equipment(equipment: Equipment, time: datetime, commit=True) -> None:
    query = db_session.query(Object).where(
        Object.current_step == equipment.name,
        Object.status == "BUFFER"
    ).limit(equipment.capacity - count_objects_executing(equipment)).order_by(Object.case_id)
    objects = query.all()
    for object in objects:
        print(f"{object.type} entering on buffer of {equipment.name}")
        object.status = "EXECUTING"
        object.start_current_step_executing = time
        db_session.add(object)
        
    if commit:
        db_session.commit()


def get_finished_executing(equipment: Equipment, time: datetime) -> list[Object]:
    query = db_session.query(Object).where(
        Object.current_step == equipment.name,
        Object.status == "EXECUTING",
        Object.start_current_step_executing + Object.duration_current_step <= time
    ).order_by(Object.case_id)
    return query.all()
