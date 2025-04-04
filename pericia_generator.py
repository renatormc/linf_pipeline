from manage import backup_db
from models import Step, Object, Case, Worker,  Equipment,  DBSession
from sheets import Planilha



def populate_db_cases(numero: int) -> None:
    with DBSession() as db_session:
        pla = Planilha()

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
            equipamento.lenght = eq.quantidade
            equipamento.capacity = eq.buffer + eq.quantidade
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
                pericia.objects.append(objeto)
            db_session.add(pericia)
        db_session.commit()

    # backup_db()

