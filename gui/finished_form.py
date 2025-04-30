from PySide6.QtWidgets import QWidget, QFormLayout, QLineEdit


class FinishedForm(QWidget):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        lay = QFormLayout()

        self.led_cases_running = QLineEdit()
        self.led_cases_running.setText("0")
        self.led_cases_running.setReadOnly(True)
        lay.addRow("Perícias em andamento:", self.led_cases_running)

        self.led_obj_finished = QLineEdit()
        self.led_obj_finished.setText("0")
        self.led_obj_finished.setReadOnly(True)
        lay.addRow("Objetos finalizados:", self.led_obj_finished)

       

        self.led_cases_finished = QLineEdit()
        self.led_cases_finished.setText("0")
        self.led_cases_finished.setReadOnly(True)
        lay.addRow("Casos finalizados:", self.led_cases_finished)

        self.setLayout(lay)

    def update_values(self, objects: int, cases: int, cases_running: int) -> None:
        self.led_cases_running.setText(str(cases_running))
        self.led_obj_finished.setText(str(objects))
        self.led_cases_finished.setText(str(cases))
