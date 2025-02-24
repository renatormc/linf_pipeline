from sqlalchemy.orm import DeclarativeBase, scoped_session, sessionmaker, mapped_column, Mapped, relationship
import sqlalchemy as sa


engine = sa.create_engine("sqlite://")

SessionMaker = sessionmaker(autocommit=False,
                            autoflush=False,
                            bind=engine)
db_session = scoped_session(SessionMaker)


class Base(DeclarativeBase):
    pass

   

class Pericia(Base):
    __tablename__ = 'pericia'
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    objetos: Mapped[list['Objeto']] = relationship(back_populates="pericia", cascade="all, delete-orphan")

    def __repr__(self):
        return str(self.id)
    

class Objeto(Base):
    __tablename__ = 'objeto'
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    pericia_id: Mapped[int] = mapped_column(sa.Integer, sa.ForeignKey("pericia.id"))
    pericia: Mapped['Pericia'] = relationship(back_populates="objetos", cascade="all, delete-orphan", uselist=False)
    tarefas: Mapped[list['Tarefa']] = relationship(back_populates="objeto", cascade="all, delete-orphan")

    def __repr__(self):
        return str(self.id)
    

class Tarefa(Base):
    __tablename__ = 'tarefa'
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(sa.String(100))
    comeco: Mapped[int | None] = mapped_column(sa.Integer)
    fim: Mapped[int | None] = mapped_column(sa.Integer)
    duracao: Mapped[int] = mapped_column(sa.Integer)
    ordem: Mapped[int] = mapped_column(sa.Integer)
    objeto_id: Mapped[int] = mapped_column(sa.Integer, sa.ForeignKey("objeto.id"))
    objeto: Mapped['Pericia'] = relationship(back_populates="tarefas", uselist=False)
    recursos: Mapped[list['Recurso']] = relationship(back_populates="tarefa")
    
    def __repr__(self):
        return str(self.nome)
    
    
class Recurso(Base):
    __tablename__ = 'recurso'
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(sa.String(100))
    tarefa_id: Mapped[int | None] = mapped_column(sa.Integer, sa.ForeignKey("tarefa.id"))
    tarefa: Mapped['Tarefa'] = relationship(back_populates="recursos", uselist=False)

    def __repr__(self):
        return str(self.id)


Base.metadata.create_all(engine)