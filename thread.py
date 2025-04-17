from dataclasses import dataclass
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QProgressBar
)
from PySide6.QtCore import QThread, Signal
import time

from models import DBSession, Equipment
from repo import count_objects_in_equipments


@dataclass
class PData:
    progress: int
    equipments: dict[str, int]   

class Worker(QThread):
    progress = Signal(PData) 
    
    def __init__(self, equipments: list[Equipment], *args, **kwargs):
        self.equipments = equipments
        super().__init__(*args, **kwargs)

    def run(self) -> None:
        with DBSession() as db_session:
            for i in range(101):
                time.sleep(0.05)
                self.progress.emit(PData(i, {eq.name:  count_objects_in_equipments(db_session, eq.name) for eq in self.equipments}))