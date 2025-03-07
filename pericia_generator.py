from models import Objeto, Pericia, Perito,  Equipamento,  db_session
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
    eqmap: dict[str, Equipamento] = {}
    for eq in pla.get_equipamentos():
        equipamento = Equipamento()
        equipamento.nome = eq.nome  
        equipamento._buffer = eq.buffer
        equipamento.capacidade = eq.quantidade
        eqmap[eq.nome] = equipamento
        db_session.add(equipamento)
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
            objeto.etapas = [item.etapa for item in pla.get_etapas(objeto.tipo, objeto.subtipo)]
            objeto.status = "AGUARDANDO_PROXIMA_ETAPA"
            objeto.proxima_etapa = objeto.etapas[0]
            pericia.objetos.append(objeto)
        db_session.add(pericia)
    db_session.commit()
