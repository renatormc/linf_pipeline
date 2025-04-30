from dataclasses import dataclass
from datetime import timedelta
from PySide6.QtCore import QThread, Signal
from custom_type import TimeValue
from models import DBSession
from repo import contar_casos_em_andamento, contar_casos_finalizados, contar_objetos_finalizados, contar_objetos_no_equipamento, \
    nomes_dos_equipamentos
from sheets import Planilha
from simulation import IntervalIterator, update_lab


@dataclass
class PData:
    progress: int
    equipments_current: dict[str, int]
    equipments_pipeline: dict[str, int]
    finished_objects_current: int
    finished_objects_pipeline: int
    finished_cases_current: int
    finished_cases_pipeline: int
    cases_running_pipeline: int
    cases_running_current: int
    time: TimeValue


class Worker(QThread):
    progress = Signal(PData)

    def __init__(self,  *args, **kwargs):
        with DBSession() as db_session:
            self.equipments = nomes_dos_equipamentos(db_session)
        self.plan = Planilha()
        super().__init__(*args, **kwargs)
        self.iter = IntervalIterator(self.plan.vars.data_inicial, self.plan.vars.data_final, timedelta(minutes=30))

    def run(self) -> None:
        with DBSession() as db_session:
            for i, time in enumerate(self.iter):
                update_lab("individual", time, db_session, self.plan)
                update_lab("pipeline", time, db_session, self.plan)
               
                self.progress.emit(PData(
                    equipments_current={eq: contar_objetos_no_equipamento("individual", db_session, eq) for eq in self.equipments},
                    equipments_pipeline={eq: contar_objetos_no_equipamento("pipeline", db_session, eq) for eq in self.equipments},
                    progress=i+1,
                    finished_cases_current=contar_casos_finalizados("individual", db_session),
                    finished_cases_pipeline=contar_casos_finalizados("pipeline", db_session),
                    cases_running_current=contar_casos_em_andamento("individual", db_session),
                    cases_running_pipeline=contar_casos_em_andamento("pipeline", db_session),
                    finished_objects_current=contar_objetos_finalizados("individual", db_session),
                    finished_objects_pipeline=contar_objetos_finalizados("pipeline", db_session),
                    time=time
                ))
