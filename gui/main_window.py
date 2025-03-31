from datetime import datetime, timedelta
from PySide6.QtWidgets import QMainWindow,  QSystemTrayIcon, QMenu, QApplication
from PySide6.QtGui import QAction, QTextCursor

from gui.simulation_thread import ProgressData, SimulationThread
from repo import count_finished_cases, count_finished_objects
from simulation import IntervalIterator
from .main_window_ui import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.connections()
        self.thread: SimulationThread | None = None
        self.iter: IntervalIterator | None = None


    def connections(self) -> None:
        self.ui.btn_start.clicked.connect(self.start_simulation)
        self.ui.btn_stop.clicked.connect(self.stop_simulation)
    
    def start_simulation(self) -> None:
        inicio = datetime(2024, 1, 1, 0, 0, 0)
        fim = datetime(2024, 1, 31, 23, 59, 59)
        self.iter = IntervalIterator(inicio, fim, timedelta(minutes=30))
        self.thread = SimulationThread(self.iter, "pipeline")
        self.thread.progress.connect(self.update_progress)
        self.thread.finished.connect(self.on_thread_finish)
        self.ui.progressBar.setValue(0)
        self.ui.progressBar.setMaximum(self.iter.steps)
        self.ui.btn_start.setEnabled(False)
        self.ui.btn_stop.setEnabled(True)
        self.thread.start()
        
    
    def stop_simulation(self) -> None:
        if self.thread:
            self.thread.terminate()
    
    def update_progress(self, p: ProgressData) -> None:
        self.ui.progressBar.setValue(p.value)
        n = count_finished_cases()
        self.ui.lbl_finished_cases.setText(str(n))
        n = count_finished_objects()
        self.ui.lbl_finished_objects.setText(str(n))
        self.ui.lbl_time.setText(p.time.strftime("%d/%m/%Y %H:%M:%S"))
        
    def on_thread_finish(self) -> None:
        self.ui.btn_start.setEnabled(True)
        self.ui.btn_stop.setEnabled(False)

   


