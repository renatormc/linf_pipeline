import config
from models import Step, Object, Case, Worker,  Equipment,  DBSession
from sheets import Planilha


def new_equipments(nome: str, quantidade: int, buffer: int, order: int) -> tuple[Equipment, Equipment]:
    eqs = (Equipment(), Equipment())
    for eq in eqs:
        eq.order = order
        eq.name = nome  
        eq.lenght = quantidade
        eq.capacity = buffer + quantidade
    eqs[0].method = "current"
    eqs[1].method = "pipeline"
    return eqs

def new_cases() -> tuple[Case, Case]:
    c1 = Case()
    c1.method = "current"
    c2 = Case()
    c2.method = "pipeline"
    return c1, c2

def new_objects(pla: Planilha) -> tuple[Object, Object]:
    objetos = (Object(), Object())
    type = pla.gerar_tipo_objeto()
    subtype = pla.gerar_subtipo_objeto(type)
    for objeto in objetos:
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
    return objetos


def populate_db_cases(numero: int) -> None:
    with DBSession() as db_session:
        pla = Planilha()

        # cadastrar peritos
        for p in pla.get_peritos():
            perito = Worker()
            perito.name = p.nome
            perito.day_sequence = p.sequencia
            db_session.add(perito)
        db_session.commit()

        # cadastrar tipos step
        eqmap: dict[str, tuple[Equipment, Equipment]] = {}
        for i, eq in enumerate(pla.get_equipamentos()):
            eqs = new_equipments(eq.nome, eq.quantidade, eq.buffer, i)
            eqmap[eq.nome] = eqs
            db_session.add(eqs[0])
            db_session.add(eqs[1])
        db_session.commit()

        for pericia in db_session.query(Case).all():
            db_session.delete(pericia)
        db_session.commit()
        for _ in range(numero):
            cases = new_cases()
            for i in range(pla.gerar_qtd_objetos()):
                objs = new_objects(pla)
                cases[0].objects.append(objs[0])
                cases[1].objects.append(objs[1])
               
            db_session.add(cases[0])
            db_session.add(cases[1])
        db_session.commit()

    # backup_db()

