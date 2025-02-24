from dataclasses import dataclass
from datetime import timedelta
from typing import Literal, Protocol, Type, TypedDict

RECURSO = Literal['perito', 'computador', 'ufed', 'tableau']

@dataclass
class TipoTarefa:
    nome: str
    duracao: timedelta
    recursos: list[RECURSO]


@dataclass
class TipoObjeto:
    nome: str
    tarefas: list[TipoTarefa]

TIPO_PERICIA = list[TipoObjeto]


celular_logica = TipoObjeto(nome="celular_logica", tarefas=[
    TipoTarefa(nome="higienizacao", duracao=timedelta(minutes=30), recursos=[]),
    TipoTarefa(nome="higienizacao", duracao=timedelta(minutes=30)),
    TipoTarefa(nome="higienizacao", duracao=timedelta(minutes=30)),
    TipoTarefa(nome="higienizacao", duracao=timedelta(minutes=30)),
])



tipos_pericia: list[TIPO_PERICIA] = [

]