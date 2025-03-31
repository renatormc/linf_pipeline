from dataclasses import dataclass
from typing import Literal
from PySide6.QtCore import QThread, Signal
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from models import DBSession
from simulation import IntervalIterator, update_current, update_pipeline

@dataclass
class ProgressData:
    value: int
    time: datetime

class SimulationThread(QThread):
    progress = Signal(ProgressData) 
    
    def __init__(self, it: IntervalIterator, type: Literal["pipeline", "current"]) -> None:
        super().__init__()
        self.it = it
        self.type = type

    def run(self) -> None:
        with DBSession() as db_session:
            inicio = datetime(2024, 1, 1, 0, 0, 0)
            fim = datetime(2024, 1, 31, 23, 59, 59)
            iter = IntervalIterator(inicio, fim, timedelta(minutes=30))
            for i, time in enumerate(iter):
                if self.type == 'pipeline':
                    update_pipeline(time, db_session)
                else:
                    update_current(time, db_session)
                self.progress.emit(ProgressData(i + 1, time))
