import config
from models import Step, Object, Case, Worker,  Equipment,  DBSession
from sheets import Planilha
from sqlalchemy.orm import Session

def new_equipment(nome: str, quantidade: int, buffer: int, order: int) -> Equipment:
    eq = Equipment()
    eq.order = order
    eq.name = nome  
    eq.lenght = quantidade
    eq.capacity = buffer + quantidade
    return eq

def new_object(pla: Planilha) -> Object:
    objeto = Object()
    type = pla.gerar_tipo_objeto()
    subtype = pla.gerar_subtipo_objeto(type)
    objeto.type = type
    objeto.subtype = subtype
    steps: list[Step] = []
    for i, item in enumerate(pla.get_etapas(objeto.type, objeto.subtype)):
        step = Step()
        step.name = item.etapa
        if i > 0:
            steps[i-1].next_step = item.etapa
            step.previous_step = steps[i-1].name
        else:
            objeto.next_step = item.etapa
        step.object = objeto
        step.order = i
        step.duration = item.tempo_minimo
        steps.append(step)
    return objeto


def cadastrar_peritos(pla: Planilha, db_session: Session) -> None:
    for p in pla.get_peritos():
        perito = Worker()
        perito.name = p.nome
        perito.day_sequence = p.sequencia
        db_session.add(perito)
    db_session.commit()
    
    
def cadastrar_equipamentos(pla: Planilha, db_session: Session) -> None:
    # eqmap: dict[str, Equipment] = {}
    for i, eq in enumerate(pla.get_equipamentos()):
        equipment = new_equipment(eq.nome, eq.quantidade, eq.buffer, i)
        # eqmap[eq.nome] = equipment
        db_session.add(equipment)
    db_session.commit()


def populate_db_cases(numero: int) -> None:
    with DBSession() as db_session:
        pla = Planilha(1)

        cadastrar_peritos(pla, db_session)
        cadastrar_equipamentos(pla, db_session)

        for pericia in db_session.query(Case).all():
            db_session.delete(pericia)
        db_session.commit()
        for _ in range(numero):
            case = Case()
            for i in range(pla.gerar_qtd_objetos()):
                obj = new_object(pla)
                case.objects.append(obj)
               
            db_session.add(case)
        db_session.commit()


