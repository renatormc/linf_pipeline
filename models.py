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


recurso_tarefa = sa.Table('recurso_tarefa', Base.metadata,
                          sa.Column('recurso', sa.Integer, sa.ForeignKey('recurso.id'), nullable=False),
                          sa.Column('tarefa', sa.Integer, sa.ForeignKey('tarefa.id'), nullable=False),
                          sa.PrimaryKeyConstraint('recurso', 'tarefa'))


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
    perito_id: Mapped[int | None] = mapped_column(sa.Integer, sa.ForeignKey("perito.id"))
    perito: Mapped[Optional['Perito']] = relationship(back_populates="pericias", uselist=False)

    def __repr__(self):
        return str(self.id)


class Objeto(Base):
    __tablename__ = 'objeto'
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    tipo: Mapped[str] = mapped_column(sa.String(100))
    subtipo: Mapped[str] = mapped_column(sa.String(100))
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
    recursos: Mapped[list['Recurso']] = relationship(back_populates="tarefas", secondary=recurso_tarefa)

    def __repr__(self):
        return str(self.nome)


class Recurso(Base):
    __tablename__ = 'recurso'
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(sa.String(100))
    quantidade: Mapped[int] = mapped_column(sa.Integer)
    quantidade_ocupado: Mapped[int] = mapped_column(sa.Integer, default=0)
    tarefas: Mapped['Tarefa'] = relationship(back_populates="recursos", secondary=recurso_tarefa)

    def __repr__(self):
        return str(self.id)


Base.metadata.create_all(engine)
