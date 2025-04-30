from datetime import datetime, timedelta
from typing import Literal, Optional
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship, Session
import sqlalchemy as sa
import config


def create_engine() -> sa.Engine:
    return sa.create_engine(f"postgresql://{config.DB_USER}:{config.DB_PASSWORD}@localhost/pipeline")


def DBSession() -> Session:
    return Session(create_engine())


class Base(DeclarativeBase):
    pass


class Worker(Base):
    __tablename__ = 'worker'
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    name: Mapped[str] = mapped_column(sa.String(100))
    day_sequence: Mapped[int] = mapped_column(sa.Integer)
    cases: Mapped[list['Case']] = relationship(back_populates="worker")

    def __repr__(self):
        return str(self.id)


class Case(Base):
    __tablename__ = 'case'
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    objects: Mapped[list['Object']] = relationship(back_populates="case", cascade="all, delete-orphan")
    start: Mapped[datetime | None] = mapped_column(sa.DateTime)
    end: Mapped[datetime | None] = mapped_column(sa.DateTime)
    method: Mapped[str] = mapped_column(sa.String(30))
    worker_id: Mapped[int | None] = mapped_column(sa.Integer, sa.ForeignKey("worker.id"))
    worker: Mapped[Optional['Worker']] = relationship(back_populates="cases", uselist=False)

    def __repr__(self):
        return str(self.id)


StatusObjeto = Literal["BUFFER", "RUNNING", "INITIAL", "FINISHED"]


class Object(Base):
    __tablename__ = 'object'
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    type: Mapped[str] = mapped_column(sa.String(100))
    subtype: Mapped[str] = mapped_column(sa.String(100))
    status: Mapped[StatusObjeto] = mapped_column(sa.String(100), default="INITIAL")
    current_location: Mapped[str | None] = mapped_column(sa.String(100))
    next_step: Mapped[str | None] = mapped_column(sa.String(100))
    duration_current_step: Mapped[timedelta | None] = mapped_column(sa.Interval)
    start_current_step_executing: Mapped[datetime | None] = mapped_column(sa.DateTime)
    case_id: Mapped[int] = mapped_column(sa.Integer, sa.ForeignKey("case.id"))
    case: Mapped['Case'] = relationship(back_populates="objects", uselist=False)
    steps: Mapped[list['Step']] = relationship(back_populates="object", cascade="all, delete-orphan", order_by="Step.order.asc()")

    def __repr__(self):
        return f"{self.type} {self.id}"

    def get_current_step(self, db_session: Session) -> 'Step':
        return db_session.query(Step).where(
            Step.name == self.current_location,
            Step.object_id == self.id
        ).one()


class Equipment(Base):
    __tablename__ = 'equipment'
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    name: Mapped[str] = mapped_column(sa.String(100))
    lenght: Mapped[int] = mapped_column(sa.Integer)
    capacity: Mapped[int] = mapped_column(sa.Integer)
    method: Mapped[str] = mapped_column(sa.String(30))
    order: Mapped[int] = mapped_column(sa.Integer)

    def __repr__(self):
        return self.name


class Step(Base):
    __tablename__ = 'step'
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    name: Mapped[str] = mapped_column(sa.String(100))
    order: Mapped[int] = mapped_column(sa.Integer)
    duration: Mapped[timedelta] = mapped_column(sa.Interval)
    next_step: Mapped[str | None] = mapped_column(sa.String)
    previous_step: Mapped[str | None] = mapped_column(sa.String)
    started_at: Mapped[datetime | None] = mapped_column(sa.DateTime)
    ended_at: Mapped[datetime | None] = mapped_column(sa.DateTime)
    waited: Mapped[timedelta | None] = mapped_column(sa.Interval)
    object_id: Mapped[int] = mapped_column(sa.Integer, sa.ForeignKey("object.id"))
    object: Mapped['Object'] = relationship(back_populates="steps", uselist=False)

    def __repr__(self):
        return str(self.id)


def create_tables() -> None:
    Base.metadata.create_all(create_engine())
