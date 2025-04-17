import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel


class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        

    def setup_ui(self) -> None:
        self.setWindowTitle("PySide6 Example")
        self.setGeometry(100, 100, 300, 150)

        self.main_layout = QVBoxLayout()


    def setup_table(self) -> None:
        self.table = QTableWeidget(2, 3)
        self.table.setHorizontalHeaderLabels(["Name", "Age", "Country"])

        # Fill the table
        self.table.setItem(0, 0, QTableWidgetItem("Alice"))
        self.table.setItem(0, 1, QTableWidgetItem("30"))
        self.table.setItem(0, 2, QTableWidgetItem("USA"))

        self.table.setItem(1, 0, QTableWidgetItem("Bob"))
        self.table.setItem(1, 1, QTableWidgetItem("25"))
        self.table.setItem(1, 2, QTableWidgetItem("Canada"))

        layout.addWidget(self.table)
        self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MyWindow()
    window.show()

    sys.exit(app.exec())
