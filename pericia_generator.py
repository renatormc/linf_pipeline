from sqlalchemy import delete
from models import Objeto, Pericia, Perito,  Etapa, TipoEtapa,  db_session
from sheets import Planilha


def popular_db_pericias(numero: int) -> None:
    pla = Planilha()

    for per in db_session.query(Perito).all():
        db_session.delete(per)
    db_session.commit()
    # cadastrar peritos
    for i in range(12):
        perito = Perito()
        perito.nome = f"Perito {i+1}"
        db_session.add(perito)
    db_session.commit()

    # cadastrar tipos etapa
    etapasmap: dict[str, TipoEtapa] = {}
    for te in pla.get_tipos_etapa():
        tipo = TipoEtapa()
        tipo.nome = te.nome
        tipo.vagas = te.vagas
        tipo.tamanho_buffer = te.buffer
        etapasmap[tipo.nome] = tipo
        db_session.add(tipo)
    db_session.commit()

    for pericia in db_session.query(Pericia).all():
        db_session.delete(pericia)
    db_session.commit()
    for _ in range(numero):
        pericia = Pericia()
        for i in range(pla.gerar_qtd_objetos()):
            objeto = Objeto()
            objeto.tipo = pla.gerar_tipo_objeto()
            objeto.subtipo = pla.gerar_subtipo_objeto(objeto.tipo)
            for i, item in enumerate(pla.get_etapas(objeto.tipo, objeto.subtipo)):
                etapa = Etapa()
                etapa.nome = item.etapa
                etapa.duracao = item.tempo_minimo.seconds
                etapa.ordem = i
                etapa.tipo = etapasmap[item.etapa]
                etapa.objeto = objeto
                db_session.add(etapa)
            pericia.objetos.append(objeto)
        db_session.add(pericia)
    db_session.commit()
