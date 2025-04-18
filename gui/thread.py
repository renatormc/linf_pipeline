from dataclasses import dataclass
from datetime import datetime, timedelta
from PySide6.QtCore import QThread, Signal

from models import DBSession
from repo import count_finished_cases, count_finished_objects, count_objects_in_equipments
from simulation import IntervalIterator, update_current, update_pipeline


@dataclass
class PData:
    progress: int
    equipments_current: dict[str, int]
    equipments_pipeline: dict[str, int]
    finished_objects_current: int
    finished_objects_pipeline: int
    finished_cases_current: int
    finished_cases_pipeline: int
    time: datetime


class Worker(QThread):
    progress = Signal(PData)

    def __init__(self, equipments: list[str], *args, **kwargs):
        self.equipments = equipments
        super().__init__(*args, **kwargs)
        inicio = datetime(2024, 1, 1, 0, 0, 0)
        fim = datetime(2024, 1, 31, 23, 59, 59)
        self.iter = IntervalIterator(inicio, fim, timedelta(minutes=30))

    def run(self) -> None:
        with DBSession() as db_session:
            for i, time in enumerate(self.iter):
                update_pipeline(time, db_session)
                update_current(time, db_session)
                self.progress.emit(PData(
                    equipments_current={eq: count_objects_in_equipments("current", db_session, eq) for eq in self.equipments},
                    equipments_pipeline={eq: count_objects_in_equipments("pipeline", db_session, eq) for eq in self.equipments},
                    progress=i+1,
                    finished_cases_current=count_finished_cases("current", db_session),
                    finished_cases_pipeline=count_finished_cases("pipeline", db_session),
                    finished_objects_current=count_finished_objects("current", db_session),
                    finished_objects_pipeline=count_finished_objects("pipeline", db_session),
                    time=time
                ))
