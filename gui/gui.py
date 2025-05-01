from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar, QFormLayout, QLineEdit, QHBoxLayout
from PySide6.QtGui import QIcon
import config
from gui.equipments_table import EquipmentsTable
from gui.finished_form import FinishedForm
from models import DBSession, Equipment
from gui.thread import PData, Worker


class SimulatorWindow(QWidget):
    def __init__(self, scene: int) -> None:
        self.scene = scene
        self.worker: Worker | None = None
        super().__init__()
        with DBSession() as db_session:
            self.equipments = db_session.query(Equipment).all()
        self.eqmap: dict[str, int] = {}
        self.setup_ui()
        self.start_thread()

    def setup_ui(self) -> None:
        self.setWindowTitle("Pipeline simulator")
        self.setGeometry(100, 100, 400, 400)
        self.setWindowIcon(QIcon(str(config.APPDIR / "pipeline.png")))

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.main_layout.addWidget(QLabel("Equipamentos"))

        lay = QHBoxLayout()

        lay2 = QVBoxLayout()
        self.eq_individual = EquipmentsTable(self)
        lay2.addWidget(self.eq_individual)
        self.frm_finished_individual = FinishedForm()
        lay2.addWidget(self.frm_finished_individual)

        lay.addLayout(lay2)
        self.main_layout.addLayout(lay)

        lay4 = QFormLayout()
        self.led_time = QLineEdit()
        self.led_time.setReadOnly(True)
        lay4.addRow("Tempo:", self.led_time)
        self.main_layout.addLayout(lay4)

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

    def update_progress(self, p: PData) -> None:
        self.pgbar.setValue(p.progress)
        for name, running in p.equipments.items():
            self.eq_individual.update_equipment(name, running)
        self.frm_finished_individual.update_values(p.finished_objects, p.finished_cases, p.cases_running)
        # self.frm_finished_pipeline.update_values(p.finished_objects_pipeline, p.finished_cases_pipeline, p.cases_running_pipeline)
        self.led_time.setText(p.time.time.strftime("%d/%m/%Y %H:%M"))

    def start_thread(self) -> None:
        self.worker = Worker(self.scene)
        self.pgbar.setMaximum(self.worker.iter.steps)
        self.worker.progress.connect(self.update_progress)
        self.worker.start()

    def closeEvent(self, event) -> None:
        if self.worker:
            self.worker.terminate()
        return super().closeEvent(event)
