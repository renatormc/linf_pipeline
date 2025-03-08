from models import Step, Object, Case, Worker,  Equipment,  db_session
from sheets import Planilha


def popular_db_pericias(numero: int) -> None:
    pla = Planilha()

    for per in db_session.query(Worker).all():
        db_session.delete(per)
    db_session.commit()
    # cadastrar peritos
    for i in range(12):
        perito = Worker()
        perito.name = f"Perito {i+1}"
        db_session.add(perito)
    db_session.commit()

    # cadastrar tipos step
    eqmap: dict[str, Equipment] = {}
    for i, eq in enumerate(pla.get_equipamentos()):
        equipamento = Equipment()
        equipamento.order = i
        equipamento.name = eq.nome  
        equipamento.buffer = eq.buffer
        equipamento.capacity = eq.quantidade
        eqmap[eq.nome] = equipamento
        db_session.add(equipamento)
    db_session.commit()

    for pericia in db_session.query(Case).all():
        db_session.delete(pericia)
    db_session.commit()
    for _ in range(numero):
        pericia = Case()
        for i in range(pla.gerar_qtd_objetos()):
            objeto = Object()
            objeto.type = pla.gerar_tipo_objeto()
            objeto.subtype = pla.gerar_subtipo_objeto(objeto.type)
            steps: list[Step] = []
            for i, item in enumerate(pla.get_etapas(objeto.type, objeto.subtype)):
                if i > 0:
                    steps[i-1].next_step = item.etapa
                step = Step()
                step.equipment = eqmap[item.etapa]
                step.object = objeto
                step.order = i
                step.duration = item.tempo_minimo
                steps.append(step)
            pericia.objects.append(objeto)
        db_session.add(pericia)
    db_session.commit()
