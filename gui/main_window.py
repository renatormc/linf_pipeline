from datetime import datetime, timedelta
from PySide6.QtWidgets import QMainWindow,  QSystemTrayIcon, QMenu, QApplication
from PySide6.QtGui import QAction, QTextCursor
from sqlalchemy.orm import Session
from gui.simulation_thread import ProgressData, SimulationThread
from models import create_engine
from repo import count_finished_cases, count_finished_objects
from simulation import IntervalIterator
from .main_window_ui import Ui_MainWindow

def label_text(value: str) -> str:
    return f"<span style=\"font-size: 20px; color: blue;\">{value}</span>"

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.connections()
        self.sim_thread: SimulationThread | None = None
        self.db_session: Session | None = None
        self.iter: IntervalIterator | None = None


    def connections(self) -> None:
        self.ui.btn_simulate_pipeline.clicked.connect(self.start_simulation)
        self.ui.btn_stop.clicked.connect(self.stop_simulation)
    
    def start_simulation(self) -> None:
        self.db_session = Session(create_engine())
        inicio = datetime.combine(self.ui.det_start.date().toPython(), datetime.min.time())
        fim = datetime.combine(self.ui.det_end.date().toPython(), datetime.max.time())
        self.iter = IntervalIterator(inicio, fim, timedelta(minutes=30))
        self.sim_thread = SimulationThread(self.iter, "pipeline")
        self.sim_thread.progress.connect(self.update_progress)
        self.sim_thread.finished.connect(self.on_thread_finish)
        self.ui.progressBar.setValue(0)
        
        self.ui.progressBar.setMaximum(self.iter.steps)
        self.ui.btn_simulate_pipeline.setEnabled(False)
        self.ui.btn_stop.setEnabled(True)
        self.sim_thread.start()
        
    
    def stop_simulation(self) -> None:
        if self.sim_thread:
            self.sim_thread.terminate()
    
    def update_progress(self, p: ProgressData) -> None:
        if self.db_session:
            self.ui.progressBar.setValue(p.value)
            n = count_finished_cases(self.db_session)
            self.ui.lbl_finished_cases.setText(label_text(str(n)))
            n = count_finished_objects(self.db_session)
            self.ui.lbl_finished_objects.setText(label_text(str(n)))
            self.ui.lbl_time.setText(label_text(p.time.strftime("%d/%m/%Y %H:%M:%S")))
            self.db_session.close()
            self.db_session = None
            
    def on_thread_finish(self) -> None:
        self.ui.btn_simulate_pipeline.setEnabled(True)
        self.ui.btn_stop.setEnabled(False)

   


