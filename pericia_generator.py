from models import StepModel, EvidenceModel, CaseModel, WorkerModel,  EquipmentModel,  DBSession
from sheets import Planilha


def new_equipments(nome: str, quantidade: int, buffer: int, order: int) -> tuple[EquipmentModel, EquipmentModel]:
    eqs = (EquipmentModel(), EquipmentModel())
    for eq in eqs:
        eq.order = order
        eq.name = nome  
        eq.lenght = quantidade
        eq.capacity = buffer + quantidade
    eqs[0].method = "current"
    eqs[1].method = "pipeline"
    return eqs

def new_cases() -> tuple[CaseModel, CaseModel]:
    c1 = CaseModel()
    c1.method = "current"
    c2 = CaseModel()
    c2.method = "pipeline"
    return c1, c2

def new_evidences(pla: Planilha) -> tuple[EvidenceModel, EvidenceModel]:
    evidencias = (EvidenceModel(), EvidenceModel())
    type = pla.gerar_tipo_evidencia()
    subtype = pla.gerar_subtipo_evidencia(type)
    for evidencia in evidencias:
        evidencia.type = pla.gerar_tipo_evidencia()
        evidencia.subtype = subtype
        steps: list[StepModel] = []
        for i, item in enumerate(pla.get_etapas(evidencia.type, evidencia.subtype)):
            step = StepModel()
            step.name = item.etapa
            if i > 0:
                steps[i-1].next_step = item.etapa
                step.previous_step = steps[i-1].name
            step.evidence = evidencia
            step.order = i
            step.duration = item.tempo_minimo
            steps.append(step)
    return evidencias


def populate_db_cases(numero: int) -> None:
    with DBSession() as db_session:
        pla = Planilha()

        # cadastrar peritos
        for i in range(12):
            perito = WorkerModel()
            perito.name = f"Perito {i+1}"
            db_session.add(perito)
        db_session.commit()

        # cadastrar tipos step
        eqmap: dict[str, tuple[EquipmentModel, EquipmentModel]] = {}
        for i, eq in enumerate(pla.get_equipamentos()):
            eqs = new_equipments(eq.nome, eq.quantidade, eq.buffer, i)
            eqmap[eq.nome] = eqs
            db_session.add(eqs[0])
            db_session.add(eqs[1])
        db_session.commit()

        for pericia in db_session.query(CaseModel).all():
            db_session.delete(pericia)
        db_session.commit()
        for _ in range(numero):
            cases = new_cases()
            for i in range(pla.gerar_qtd_evidencias()):
                objs = new_evidences(pla)
                cases[0].evidences.append(objs[0])
                cases[1].evidences.append(objs[1])
               
            db_session.add(cases[0])
            db_session.add(cases[1])
        db_session.commit()

    # backup_db()

