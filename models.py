from datetime import datetime, timedelta
from typing import Literal, Optional
from sqlalchemy.orm import DeclarativeBase, scoped_session, sessionmaker, mapped_column, Mapped, relationship
from sqlalchemy.types import TypeDecorator, Float
import sqlalchemy as sa
import config


engine = sa.create_engine(f"sqlite:///{config.LOCAL_FOLDER / 'pericias.db'}")

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

class Perito(Base):
    __tablename__ = 'perito'
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(sa.String(100))
    pericias: Mapped[list['Pericia']] = relationship(back_populates="perito")

    def __repr__(self):
        return str(self.id)


class Pericia(Base):
    __tablename__ = 'pericia'
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    objetos: Mapped[list['Objeto']] = relationship(back_populates="pericia", cascade="all, delete-orphan")
    comeco: Mapped[datetime | None] = mapped_column(sa.DateTime)
    fim: Mapped[datetime | None] = mapped_column(sa.DateTime)
    perito_id: Mapped[int | None] = mapped_column(sa.Integer, sa.ForeignKey("perito.id"))
    perito: Mapped[Optional['Perito']] = relationship(back_populates="pericias", uselist=False)

    def __repr__(self):
        return str(self.id)


class Objeto(Base):
    __tablename__ = 'objeto'
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    tipo: Mapped[str] = mapped_column(sa.String(100))
    subtipo: Mapped[str] = mapped_column(sa.String(100))
    comeco: Mapped[datetime | None] = mapped_column(sa.DateTime)
    fim: Mapped[datetime | None] = mapped_column(sa.DateTime)
    etapa: Mapped[int] = mapped_column(sa.Integer, default=0)
    proxima_etapa: Mapped[str | None] = mapped_column(sa.String(100))
    ultima_etapa: Mapped[int] = mapped_column(sa.Integer, default=0)
    pericia_id: Mapped[int] = mapped_column(sa.Integer, sa.ForeignKey("pericia.id"))
    pericia: Mapped['Pericia'] = relationship(back_populates="objetos", uselist=False)
    etapas: Mapped[list['Etapa']] = relationship(back_populates="objeto", cascade="all, delete-orphan")

    def __repr__(self):
        return f"{self.tipo} - {self.subtipo}"



class Equipamento(Base):
    __tablename__ = 'equipamento'
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(sa.String(100))
    buffer: Mapped[int] = mapped_column(sa.Integer)
    quantidade: Mapped[int] = mapped_column(sa.Integer)
    quantidade_ocupada: Mapped[int] = mapped_column(sa.Integer, default=0)
    etapas: Mapped[list['Etapa']] = relationship(back_populates="equipamento", cascade="all, delete-orphan")

    def __repr__(self):
        return self.nome


EstapaStatus = Literal["PENDENTE", "BUFFER", "EXECUTANDO", "FINALIZADA"]


class Etapa(Base):
    __tablename__ = 'etapa'
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(sa.String(100))
    duracao: Mapped[timedelta] = mapped_column(TimedeltaAsSeconds)
    ordem: Mapped[int] = mapped_column(sa.Integer)
    objeto_id: Mapped[int] = mapped_column(sa.Integer, sa.ForeignKey("objeto.id"))
    objeto: Mapped['Objeto'] = relationship(back_populates="etapas", uselist=False)
    equipamento_id: Mapped[int] = mapped_column(sa.Integer, sa.ForeignKey("equipamento.id"))
    equipamento: Mapped['Equipamento'] = relationship(back_populates="etapas", uselist=False)

          
    def __repr__(self):
        return self.nome


Base.metadata.create_all(engine)
