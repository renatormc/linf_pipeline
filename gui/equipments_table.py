from PySide6.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView
from PySide6.QtCore import Qt
from custom_type import SIM_METHOD
from models import DBSession, Equipment
from repo import contar_objetos_no_equipamento



class EquipmentsTable(QTableWidget):
    def __init__(self, parent, sim_method: SIM_METHOD) -> None:
        super().__init__(parent, rowCount=0, columnCount=4)
        self.sim_method = sim_method
        self.eqmap: dict[str, int] = {}
        self.horizontalHeader().setStretchLastSection(True)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) #type: ignore
        self.setHorizontalHeaderLabels(["Equipamento", "Capacidade", "Quantidade", "Executando"])
        
        with DBSession() as db_session:
            eqs = db_session.query(Equipment).where(Equipment.method == self.sim_method).all()
            for eq in eqs:
                self.add_table_row(eq.name, eq.capacity, eq.lenght,  contar_objetos_no_equipamento(self.sim_method, db_session, eq.name))   

    def add_table_row(self, name: str, capacity: int, length: int, running: int) -> None:
        row_position = self.rowCount()
        self.insertRow(row_position)
        self.eqmap[name] = row_position
        item = QTableWidgetItem(name)
        item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        self.setItem(row_position, 0, item)
        item = QTableWidgetItem(str(capacity))
        item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        self.setItem(row_position, 1, item)
        item = QTableWidgetItem(str(length))
        item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        self.setItem(row_position, 2, item)
        item = QTableWidgetItem(str(running))
        item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        self.setItem(row_position, 3, item)

    def update_equipment(self, name: str, running: int) -> None:
        row = self.eqmap[name]
        item = self.item(row, 3)
        if item:
            item.setText(str(running))

    
        