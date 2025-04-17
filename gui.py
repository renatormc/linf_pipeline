import sys
from typing import Literal
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, \
    QLabel, QTableWidget, QTableWidgetItem, QHeaderView, QProgressBar, QFormLayout, QLineEdit
from PySide6.QtCore import Qt

from models import DBSession, Equipment
from repo import count_objects_in_equipments
from thread import PData, Worker

class SimulatorWindow(QWidget):
    def __init__(self, sim_type: Literal['pipeline', 'current']) -> None:
        self.sim_type = sim_type
        super().__init__()
        with DBSession() as db_session:
            self.equipments = db_session.query(Equipment).all()
        self.eqmap: dict[str, int] = {}
        self.setup_ui()
        self.start_thread()
        

    def setup_ui(self) -> None:
        self.setWindowTitle("Pipeline simulator")
        self.setGeometry(100, 100, 600, 400)

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
        
        self.main_layout.addWidget(QLabel("Equipamentos"))
        self.setup_twd_equipments()
        
        self.main_layout.addWidget(QLabel("Finalziados"))
        self.setup_finished()
        
        self.pgbar = QProgressBar()
        self.main_layout.addWidget(self.pgbar)
        
    def add_table_row(self, name: str, capacity: int, length: int, running: int) -> None:
        row_position = self.twd_equipments.rowCount()
        self.twd_equipments.insertRow(row_position)
        self.eqmap[name] = row_position
        item = QTableWidgetItem(name)
        item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        self.twd_equipments.setItem(row_position, 0, item)
        item = QTableWidgetItem(str(capacity))
        item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        self.twd_equipments.setItem(row_position, 1, item)
        item = QTableWidgetItem(str(length))
        item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        self.twd_equipments.setItem(row_position, 2, item)
        item = QTableWidgetItem(str(running))
        item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        self.twd_equipments.setItem(row_position, 3, item)
        
    def update_equipment(self, name: str, running: int) -> None:
        row = self.eqmap[name]
        item = self.twd_equipments.item(row, 3)
        if item:
            item.setText(str(running))


    def setup_twd_equipments(self) -> None:
        self.twd_equipments = QTableWidget(0, 4)
        self.twd_equipments.horizontalHeader().setStretchLastSection(True)
        self.twd_equipments.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) #type: ignore
        self.twd_equipments.setHorizontalHeaderLabels(["Equipamento", "Capacidade", "Quantidade", "Executando"])
        
        with DBSession() as db_session:
            for eq in self.equipments:
                self.add_table_row(eq.name, eq.capacity, eq.lenght,  count_objects_in_equipments(db_session, eq.name))        

        self.main_layout.addWidget(self.twd_equipments)
        
    def setup_finished(self) -> None:
        lay = QFormLayout()
        self.led_obj_finished = QLineEdit()
        self.led_obj_finished.setText("0")
        self.led_obj_finished.setReadOnly(True)
        self.led_cases_finished = QLineEdit()
        self.led_cases_finished.setText("0")
        self.led_cases_finished.setReadOnly(True)
        lay.addRow("Objetos finalizados:", self.led_obj_finished)
        lay.addRow("Casos finalizados:", self.led_cases_finished)
        self.main_layout.addLayout(lay)
        
                
    def update_progress(self, p: PData) -> None:
        self.pgbar.setValue(p.progress)
        for name, running in p.equipments.items():
            self.update_equipment(name, running)
        self.led_cases_finished.setText(str(p.finished_cases))
        self.led_obj_finished.setText(str(p.finished_objects))
        
    def start_thread(self) -> None:
        self.worker = Worker(self.equipments, self.sim_type)
        self.worker.progress.connect(self.update_progress)
        self.worker.start()




   