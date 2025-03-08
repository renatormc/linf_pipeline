from datetime import datetime, timedelta
from typing import Literal, Optional
from sqlalchemy.orm import DeclarativeBase, scoped_session, sessionmaker, mapped_column, Mapped, relationship, Session
from sqlalchemy.types import TypeDecorator, Float
from sqlalchemy.ext.hybrid import hybrid_property
import sqlalchemy as sa
from sqlalchemy import event
import config
from sqlalchemy_utils import observes


engine = sa.create_engine(f"sqlite:///{config.LOCAL_FOLDER / 'cases.db'}")

SessionMaker = sessionmaker(autocommit=False,
                            autoflush=False,
                            bind=engine)
db_session = scoped_session(SessionMaker)


class Base(DeclarativeBase):
    pass


class TimedeltaAsSeconds(TypeDecorator):
    impl = Float

    def process_bind_param(self, value, dialect):
        if value is not None:
            return int(value.total_seconds())

    def process_result_value(self, value, dialect):
        if value is not None:
            return timedelta(seconds=value)


class Worker(Base):
    __tablename__ = 'worker'
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    name: Mapped[str] = mapped_column(sa.String(100))
    cases: Mapped[list['Case']] = relationship(back_populates="worker")

    def __repr__(self):
        return str(self.id)


class Case(Base):
    __tablename__ = 'case'
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    objects: Mapped[list['Object']] = relationship(back_populates="case", cascade="all, delete-orphan")
    start: Mapped[datetime | None] = mapped_column(sa.DateTime)
    end: Mapped[datetime | None] = mapped_column(sa.DateTime)
    worker_id: Mapped[int | None] = mapped_column(sa.Integer, sa.ForeignKey("worker.id"))
    worker: Mapped[Optional['Worker']] = relationship(back_populates="cases", uselist=False)

    def __repr__(self):
        return str(self.id)


# StatusObjeto = Literal["BUFFER", "EXECUTANDO", "AGUARDANDO_PROXIMA_ETAPA", "FINALIZADO"]


class Object(Base):
    __tablename__ = 'object'
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    type: Mapped[str] = mapped_column(sa.String(100))
    subtype: Mapped[str] = mapped_column(sa.String(100))
    case_id: Mapped[int] = mapped_column(sa.Integer, sa.ForeignKey("case.id"))
    case: Mapped['Case'] = relationship(back_populates="objects", uselist=False)
    steps: Mapped[list['Step']] = relationship(back_populates="object", cascade="all, delete-orphan", order_by="Step.order.asc()")

    def __repr__(self):
        return f"{self.type} - {self.subtype}"


class Equipment(Base):
    __tablename__ = 'equipment'
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    name: Mapped[str] = mapped_column(sa.String(100))
    buffer: Mapped[int] = mapped_column(sa.Integer)
    capacity: Mapped[int] = mapped_column(sa.Integer)
    order: Mapped[int] = mapped_column(sa.Integer)
    waiting: Mapped[int] = mapped_column(sa.Integer, default=0)
    executing: Mapped[int] = mapped_column(sa.Integer, default=0)
    steps: Mapped[list['Step']] = relationship(back_populates="equipment")


    def __repr__(self):
        return self.name


class Step(Base):
    __tablename__ = 'step'
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    start_wating: Mapped[datetime | None] = mapped_column(sa.DateTime)
    start: Mapped[datetime | None] = mapped_column(sa.DateTime)
    end: Mapped[datetime | None] = mapped_column(sa.DateTime)
    order: Mapped[int] = mapped_column(sa.Integer)
    next_step: Mapped[str | None] = mapped_column(sa.String(100))
    duration: Mapped[timedelta] = mapped_column(TimedeltaAsSeconds)
    object_id: Mapped[int] = mapped_column(sa.Integer, sa.ForeignKey("object.id"))
    object: Mapped['Object'] = relationship(back_populates="steps", uselist=False)
    equipment_id: Mapped[int] = mapped_column(sa.Integer, sa.ForeignKey("equipment.id"))
    equipment: Mapped['Equipment'] = relationship(back_populates="steps")


    def __repr__(self):
        return str(self.id)


Base.metadata.create_all(engine)

# def after_update_step(mapper, connection, target: 'Step') -> None:
#     session = Session(bind=connection)
#     target.equipment.executing = session.query(Step).where(
#         Step.equipment_id == target.equipment_id,
#         Step.start != None,
#         Step.end == None
#     ).count()
#     target.equipment.waiting = session.query(Step).where(
#         Step.equipment_id == target.equipment_id,
#         Step.start == None
#     ).count()
#     session.add(target.equipment)
#     session.commit()


# event.listen(Step, 'after_update', after_update_step)
