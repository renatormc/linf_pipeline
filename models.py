from datetime import datetime, timedelta
from typing import Literal, Optional
from sqlalchemy.orm import DeclarativeBase, scoped_session, sessionmaker, mapped_column, Mapped, relationship, Session
from sqlalchemy.types import TypeDecorator, Float
import sqlalchemy as sa
import config


def create_engine() -> sa.Engine:
    # return sa.create_engine(f"firebird+fdb://SYSDBA:masterkey@localhost:3050/{config.DBPATH}?charset=utf8")
    # return sa.create_engine(f"postgresql://{config.DB_USER}:{config.DB_PASSWORD}@localhost/pipeline")
    return  sa.create_engine(f"sqlite:///{config.DBPATH}")


def DBSession() -> Session:
    return Session(create_engine())


class Base(DeclarativeBase):
    pass


# class TimedeltaAsSeconds(TypeDecorator):
#     impl = Float
#     cache_ok = True

#     def process_bind_param(self, value, dialect):
#         if value is not None:
#             return int(value.total_seconds())

#     def process_result_value(self, value, dialect):
#         if value is not None:
#             return timedelta(seconds=value)


class WorkerModel(Base):
    __tablename__ = 'worker'
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    name: Mapped[str] = mapped_column(sa.String(100))
    cases: Mapped[list['CaseModel']] = relationship(back_populates="worker")

    def __repr__(self):
        return str(self.id)


class CaseModel(Base):
    __tablename__ = 'case'
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    evidences: Mapped[list['EvidenceModel']] = relationship(back_populates="case", cascade="all, delete-orphan")
    start: Mapped[datetime | None] = mapped_column(sa.DateTime)
    end: Mapped[datetime | None] = mapped_column(sa.DateTime)
    method: Mapped[str] = mapped_column(sa.String(30))
    worker_id: Mapped[int | None] = mapped_column(sa.Integer, sa.ForeignKey("worker.id"))
    worker: Mapped[Optional['WorkerModel']] = relationship(back_populates="cases", uselist=False)


    def __repr__(self):
        return str(self.id)


StatusObjeto = Literal["BUFFER", "RUNNING", "INITIAL", "FINISHED"]


class EvidenceModel(Base):
    __tablename__ = 'evidence'
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    type: Mapped[str] = mapped_column(sa.String(100))
    subtype: Mapped[str] = mapped_column(sa.String(100))
    case_id: Mapped[int] = mapped_column(sa.Integer, sa.ForeignKey("case.id"))
    case: Mapped['CaseModel'] = relationship(back_populates="evidences", uselist=False)
    steps: Mapped[list['StepModel']] = relationship(back_populates="evidence", cascade="all, delete-orphan", order_by="StepModel.order.asc()")
    

    def __repr__(self):
        return f"{self.type} {self.id}"


class EquipmentModel(Base):
    __tablename__ = 'equipment'
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    name: Mapped[str] = mapped_column(sa.String(100))
    lenght: Mapped[int] = mapped_column(sa.Integer)
    capacity: Mapped[int] = mapped_column(sa.Integer)
    method: Mapped[str] = mapped_column(sa.String(30))
    order: Mapped[int] = mapped_column(sa.Integer)
    
    def __repr__(self):
        return self.name


class StepModel(Base):
    __tablename__ = 'step'
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    name: Mapped[str] = mapped_column(sa.String(100))
    order: Mapped[int] = mapped_column(sa.Integer)
    duration: Mapped[timedelta] = mapped_column(sa.Interval)
    next_step: Mapped[str | None] = mapped_column(sa.String)
    previous_step: Mapped[str | None] = mapped_column(sa.String)
    evidence_id: Mapped[int] = mapped_column(sa.Integer, sa.ForeignKey("evidence.id"))
    evidence: Mapped['EvidenceModel'] = relationship(back_populates="steps", uselist=False)
   


    def __repr__(self):
        return str(self.id)

def create_tables() -> None:
    Base.metadata.create_all(create_engine())


