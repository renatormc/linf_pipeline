from datetime import datetime, timedelta
from typing import Literal, Optional
from unittest.util import strclass
from sqlalchemy.orm import DeclarativeBase, scoped_session, sessionmaker, mapped_column, Mapped, relationship
from sqlalchemy.types import TypeDecorator, Float
from sqlalchemy.ext.hybrid import hybrid_property
import sqlalchemy as sa
import config
from sqlalchemy_utils import observes


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


# StatusObjeto = Literal["BUFFER", "EXECUTANDO", "AGUARDANDO_PROXIMA_ETAPA", "FINALIZADO"]


class Objeto(Base):
    __tablename__ = 'objeto'
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    tipo: Mapped[str] = mapped_column(sa.String(100))
    subtipo: Mapped[str] = mapped_column(sa.String(100))
    # status: Mapped[StatusObjeto] = mapped_column(sa.String(100), default="AGUARDANDO_PROXIMA_ETAPA")
    # etapa: Mapped[str | None] = mapped_column(sa.String(100))
    proxima_etapa: Mapped[str | None] = mapped_column(sa.String(100))
    pericia_id: Mapped[int] = mapped_column(sa.Integer, sa.ForeignKey("pericia.id"))
    pericia: Mapped['Pericia'] = relationship(back_populates="objetos", uselist=False)
    etapas: Mapped[list['Etapa']] = relationship(back_populates="objeto", cascade="all, delete-orphan", order_by="Etapa.order.asc()")
    
    
    # def atualizar_status(self, time: datetime) -> None:
    #     if self.etapa == None and self.proxima_etapa is None:
    #         self.status = "FINALIZADO"
    #     elif self.fim_etapa_corrente is None:
    #         self.status = "BUFFER"
    #     elif self.fim_etapa_corrente > time:
    #         self.status = "EXECUTANDO"
    #     else:
    #         self.status = "AGUARDANDO_PROXIMA_ETAPA"
        

    # def etapa_depois(self, etapa: str) -> str | None:
    #     try:
    #         return self.etapas[self.etapas.index(etapa) + 1]
    #     except IndexError:
    #         return None

    # @observes("etapa")
    # def _etapa_changed(self, etapa: str) -> None:
    #     self.proxima_etapa = self.etapa_depois(etapa)
        
      

    def __repr__(self):
        return f"{self.tipo} - {self.subtipo}"


class Equipamento(Base):
    __tablename__ = 'equipamento'
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(sa.String(100))
    buffer: Mapped[int] = mapped_column(sa.Integer)
    capacidade: Mapped[int] = mapped_column(sa.Integer)
    etapas: Mapped[list['Etapa']] = relationship(back_populates="equipamento")
    
          
    def __repr__(self):
        return self.nome
    
    
class Etapa(Base):
    __tablename__ = 'etapa'
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    inicio: Mapped[datetime | None] = mapped_column(sa.DateTime)
    fim: Mapped[datetime | None] = mapped_column(sa.DateTime)
    order: Mapped[int] = mapped_column(sa.Integer)
    objeto_id: Mapped[int] = mapped_column(sa.Integer, sa.ForeignKey("objeto.id"))
    objeto: Mapped['Objeto'] = relationship(back_populates="etapas", uselist=False)
    equipamento_id: Mapped[int] = mapped_column(sa.Integer, sa.ForeignKey("equipamento.id"))
    equipamento: Mapped['Equipamento'] = relationship(back_populates="etapas")
    
    def __repr__(self):
        return str(self.id)
    

Base.metadata.create_all(engine)

