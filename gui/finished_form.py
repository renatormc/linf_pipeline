from typing import Literal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QHeaderView, QProgressBar, QFormLayout, QLineEdit
from PySide6.QtCore import Qt

from custom_type import SIM_METHOD
from models import DBSession, Equipment
from repo import count_objects_in_equipments


class FinishedForm(QWidget):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        lay = QFormLayout()
        self.led_obj_finished = QLineEdit()
        self.led_obj_finished.setText("0")
        self.led_obj_finished.setReadOnly(True)
        self.led_cases_finished = QLineEdit()
        self.led_cases_finished.setText("0")
        self.led_cases_finished.setReadOnly(True)
        lay.addRow("Objetos finalizados:", self.led_obj_finished)
        lay.addRow("Casos finalizados:", self.led_cases_finished)
        self.setLayout(lay)

    def update(self, objects: int, cases: int) -> None:
        self.led_obj_finished.setText(str(objects))
        self.led_cases_finished.setText(str(cases))