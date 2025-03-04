from datetime import datetime
from typing import Optional
from sqlalchemy.orm import DeclarativeBase, scoped_session, sessionmaker, mapped_column, Mapped, relationship
import sqlalchemy as sa
import config


engine = sa.create_engine(f"sqlite:///{config.LOCAL_FOLDER / 'pericias.db'}")

SessionMaker = sessionmaker(autocommit=False,
                            autoflush=False,
                            bind=engine)
db_session = scoped_session(SessionMaker)


class Base(DeclarativeBase):
    pass

tipo_recurso_tarefa = sa.Table('tipo_recurso_tarefa', Base.metadata,
                          sa.Column('tipo_recurso', sa.Integer, sa.ForeignKey('tipo_recurso.id'), nullable=False),
                          sa.Column('tarefa', sa.Integer, sa.ForeignKey('tarefa.id'), nullable=False),
                          sa.PrimaryKeyConstraint('tipo_recurso', 'tarefa'))


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
    pericia_id: Mapped[int] = mapped_column(sa.Integer, sa.ForeignKey("pericia.id"))
    pericia: Mapped['Pericia'] = relationship(back_populates="objetos", uselist=False)
    tarefas: Mapped[list['Tarefa']] = relationship(back_populates="objeto", cascade="all, delete-orphan")

    def __repr__(self):
        return f"{self.tipo} - {self.subtipo}"


class Tarefa(Base):
    __tablename__ = 'tarefa'
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(sa.String(100))
    comeco: Mapped[datetime | None] = mapped_column(sa.DateTime)
    fim: Mapped[datetime | None] = mapped_column(sa.DateTime)
    duracao: Mapped[int] = mapped_column(sa.Integer)
    ordem: Mapped[int] = mapped_column(sa.Integer)
    objeto_id: Mapped[int] = mapped_column(sa.Integer, sa.ForeignKey("objeto.id"))
    objeto: Mapped['Objeto'] = relationship(back_populates="tarefas", uselist=False)
    recursos: Mapped[list['Recurso']] = relationship(back_populates="tarefa")
    recursos_necessarios: Mapped[list['TipoRecurso']] = relationship(secondary=tipo_recurso_tarefa, back_populates="tarefas")

    def __repr__(self):
        return str(self.nome)


class TipoRecurso(Base):
    __tablename__ = 'tipo_recurso'
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(sa.String(100))
    recursos: Mapped[list['Recurso']] = relationship(back_populates="tipo", cascade="all, delete-orphan")
    tarefas: Mapped[list['Tarefa']] = relationship( secondary=tipo_recurso_tarefa, back_populates="recursos_necessarios")

    def __repr__(self):
        return self.nome


class Recurso(Base):
    __tablename__ = 'recurso'
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(sa.String(100))
    tipo_id: Mapped[int] = mapped_column(sa.Integer, sa.ForeignKey("tipo_recurso.id"))
    tipo: Mapped['TipoRecurso'] = relationship(back_populates="recursos", uselist=False)
    tarefa_id: Mapped[int | None] = mapped_column(sa.Integer, sa.ForeignKey("tarefa.id"))
    tarefa: Mapped[Optional['Tarefa']] = relationship(back_populates="recursos", uselist=False)

    def __repr__(self):
        return self.nome


Base.metadata.create_all(engine)
