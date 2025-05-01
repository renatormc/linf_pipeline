from dataclasses import dataclass
from datetime import timedelta
from PySide6.QtCore import QThread, Signal
from custom_type import TimeValue
from models import DBSession
from pericia_generator import cadastrar_peritos
from repo import contar_casos_em_andamento, contar_casos_finalizados, contar_objetos_finalizados, \
    contar_objetos_no_equipamento, nomes_dos_equipamentos
from sheets import Planilha
from simulation import IntervalIterator, update_lab


@dataclass
class PData:
    progress: int
    equipments: dict[str, int]
    finished_objects: int
    finished_cases: int
    cases_running: int
    time: TimeValue


class Worker(QThread):
    progress = Signal(PData)

    def __init__(self, scene: int, *args, **kwargs) -> None:
        self.scene = scene
        with DBSession() as db_session:
            self.equipments = nomes_dos_equipamentos(db_session)
        self.plan = Planilha(scene)
        super().__init__(*args, **kwargs)
        self.iter = IntervalIterator(self.plan.vars.data_inicial, self.plan.vars.data_final, timedelta(minutes=30))

    def run(self) -> None:
        with DBSession() as db_session:
            cadastrar_peritos(self.plan, db_session)
            for i, time in enumerate(self.iter):
                update_lab(time, db_session, self.plan)
                self.progress.emit(PData(
                    equipments={eq: contar_objetos_no_equipamento(db_session, eq) for eq in self.equipments},
                    progress=i+1,
                    finished_cases=contar_casos_finalizados(db_session),
                    cases_running=contar_casos_em_andamento(db_session, self.plan),
                    finished_objects=contar_objetos_finalizados(db_session),
                    time=time
                ))
