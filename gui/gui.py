from typing import Literal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar, QFormLayout, QLineEdit
from gui.equipments_table import EquipmentsTable
from models import DBSession, Equipment
from gui.thread import PData, Worker

class SimulatorWindow(QWidget):
    def __init__(self) -> None:
        self.worker: Worker | None = None
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
        
        self.eq_pipeline = EquipmentsTable(self, 'pipeline')
        self.main_layout.addWidget(self.eq_pipeline)
        
        self.main_layout.addWidget(QLabel("Finalizados"))
        self.setup_finished()
        
        self.pgbar = QProgressBar()
        self.pgbar.setStyleSheet("""
            QProgressBar {
                border: 2px solid grey;
                border-radius: 5px;
                text-align: center;
            }

            QProgressBar::chunk {
                background-color: #00c853;  /* classic green */
                width: 20px;
            }
        """)
        self.main_layout.addWidget(self.pgbar)
        
        
    def setup_finished(self) -> None:
        lay = QFormLayout()
        self.led_obj_finished = QLineEdit()
        self.led_obj_finished.setText("0")
        self.led_obj_finished.setReadOnly(True)
        self.led_cases_finished = QLineEdit()
        self.led_cases_finished.setText("0")
        self.led_cases_finished.setReadOnly(True)
        self.led_time = QLineEdit()
        self.led_time.setReadOnly(True)
        lay.addRow("Objetos finalizados:", self.led_obj_finished)
        lay.addRow("Casos finalizados:", self.led_cases_finished)
        lay.addRow("Tempo:", self.led_time)
        self.main_layout.addLayout(lay)
        
                
    def update_progress(self, p: PData) -> None:
        self.pgbar.setValue(p.progress)
        for name, running in p.equipments_pipeline.items():
            self.eq_pipeline.update_equipment(name, running)
        self.led_cases_finished.setText(str(p.finished_cases_pipeline))
        self.led_obj_finished.setText(str(p.finished_objects_pipeline))
        self.led_time.setText(p.time.strftime("%d/%m/%Y %H:%M"))
        
    def start_thread(self) -> None:
        self.worker = Worker()
        self.pgbar.setMaximum(self.worker.iter.steps)
        self.worker.progress.connect(self.update_progress)
        self.worker.start()

    def closeEvent(self, event) -> None:
        if self.worker:
            self.worker.terminate()
        return super().closeEvent(event)



   