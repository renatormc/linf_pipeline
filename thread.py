from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Literal
from PySide6.QtCore import QThread, Signal
import time

from models import DBSession, Equipment
from repo import count_finished_cases, count_finished_objects, count_objects_in_equipments
from simulation import IntervalIterator, update_current, update_pipeline


@dataclass
class PData:
    progress: int
    equipments: dict[str, int]   
    finished_objects: int
    finished_cases: int

class Worker(QThread):
    progress = Signal(PData) 
    
    def __init__(self, equipments: list[Equipment], type: Literal['pipeline', 'current'], *args, **kwargs):
        self.equipments = equipments
        self.type = type
        super().__init__(*args, **kwargs)
        inicio = datetime(2024, 1, 1, 0, 0, 0)
        fim = datetime(2024, 1, 31, 23, 59, 59)
        self.iter = IntervalIterator(inicio, fim, timedelta(minutes=30))

    def run(self) -> None:
        with DBSession() as db_session:
            for i, time in enumerate(self.iter):
                if self.type == 'pipeline':
                    update_pipeline(time, db_session)
                else:
                    update_current(time, db_session)
                
                self.progress.emit(PData(
                    equipments={eq.name: count_objects_in_equipments(db_session, eq.name) for eq in self.equipments},
                    progress=i+1,
                    finished_cases=count_finished_cases(db_session),
                    finished_objects=count_finished_objects(db_session)
                ))
                