from datetime import datetime
from os import wait
from typing import Iterable
from models import Equipment, Object, Step, db_session


def start_execute_step(step: Step, time: datetime, commit=True) -> None:
    step.start = time
    step.end = None
    step.equipment.executing += 1
    step.equipment.waiting -= 1
    db_session.add(step)
    db_session.add(step.equipment)
    if commit:
        db_session.commit()


def start_waiting_step(step: Step, time: datetime, commit=True) -> None:
    step.start_wating = time
    step.start = None
    step.end = None
    step.equipment.waiting += 1
    db_session.add(step)
    db_session.add(step.equipment)
    if commit:
        db_session.commit()

def finish_object(step: Step, time: datetime, commit=True) -> None:
    step.end = time
    step.equipment.executing -= 1
    db_session.add(step)
    db_session.add(step.equipment)
    if commit:
        db_session.commit()


def get_steps_waiting(equipment: Equipment) -> Iterable[Step]:
    query = db_session.query(Step).where(
        Step.equipment == equipment,
        Step.start_wating != None,
        Step.start == None
    ).order_by(Step.order)
    return query.all()


def get_steps_executing(equipment: Equipment,  time: datetime) -> Iterable[Step]:
    query = db_session.query(Step).where(
        Step.equipment == equipment,
        Step.start != None,
        Step.start + Step.duration > time
    ).order_by(Step.order)
    return query.all()


def get_steps_finished(equipment: Equipment, time: datetime) -> Iterable[Step]:
    query = db_session.query(Step).where(
        Step.equipment == equipment,
        Step.start != None,
        Step.start + Step.duration <= time
    ).order_by(Step.order)
    return query.all()


def get_objects_waiting_equipment(equipment: Equipment, limit: int) -> Iterable[Step]:
    query = db_session.query(Step).where(
        Step.next_step == equipment.name,
        Step.start != None,
        Step.end == None
    ).join(Step.object).order_by(Object.case_id).limit(limit)
    return query.all()
