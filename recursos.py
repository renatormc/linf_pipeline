from datetime import timedelta
from typing import Literal, Protocol

ESTADO_EQUIPAMENTO = Literal['livre', 'ocupado']


class RecursoProtocol(Protocol):

    @property
    def estado(self) -> ESTADO_EQUIPAMENTO:
        ...

    @property
    def nome(self) -> str:
        ...

    @property
    def utilidades(self) -> list[str]:
        ...

    def iniciar_processamento(self, tempo: timedelta) -> None:
        ...


