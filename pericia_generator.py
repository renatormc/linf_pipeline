from sqlalchemy import delete
from models import Objeto, Pericia, Perito, Recurso, Tarefa, TipoRecurso, db_session
from sheets import Planilha


def popular_db_pericias(numero: int) -> None:
    pla = Planilha()

    #cadastrar peritos
    for nome in pla.get_peritos():
        perito = Perito()
        perito.nome = nome
        db_session.add(perito)
    db_session.commit()
    
    #Cadastrar recursos
    recmap: dict[str, TipoRecurso] = {}
    for it in pla.get_recursos():
        tipo_recurso = TipoRecurso()
        tipo_recurso.nome = it.nome
        db_session.add(tipo_recurso)
        recmap[it.nome] = tipo_recurso
        for i in range(it.quantidade):
            recurso = Recurso()
            recurso.tipo = tipo_recurso
            recurso.nome = f"{it.nome} {i + 1}"
            db_session.add(recurso)
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
                for rec in item.recursos:
                    tarefa.recursos_necessarios.append(recmap[rec])
                objeto.tarefas.append(tarefa)
            pericia.objetos.append(objeto)
        db_session.add(pericia)
    db_session.commit()
