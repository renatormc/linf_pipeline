from sqlalchemy import delete
from models import Objeto, Pericia, Recurso, Tarefa, db_session
from sheets import Planilha


def popular_db_pericias(numero: int) -> None:
    pla = Planilha()

    #Cadastrar recursos
    for it in pla.get_recursos():
        for _ in range(it.quantidade):
            rec = Recurso()
            rec.nome = it.nome
            db_session.add(rec)
    db_session.commit()

    for pericia in db_session.query(Pericia).all():
        db_session.delete(pericia)
    db_session.commit()
    for _ in range(numero):
        pericia = Pericia()
        for i in range(pla.gerar_qtd_objetos()):
            tipo = pla.gerar_tipo_objeto()
            objeto = Objeto(tipo=tipo, subtipo=pla.gerar_subtipo_objeto(tipo))
            for i, item in enumerate(pla.get_tarefas(objeto.tipo, objeto.subtipo)):
                tarefa = Tarefa()
                tarefa.nome = item.tarefa
                tarefa.duracao = item.duracao.seconds
                tarefa.ordem = i
                tarefa.recursos_necessarios = item.recursos
                objeto.tarefas.append(tarefa)
            pericia.objetos.append(objeto)
        db_session.add(pericia)
    db_session.commit()
