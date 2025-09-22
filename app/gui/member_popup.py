import requests
from PyQt5.QtWidgets import QWidget, QTableView, QVBoxLayout
from PyQt5.QtCore import Qt, QAbstractTableModel
from PyQt5.QtGui import QIcon

class MemberTableModel(QAbstractTableModel):
    def __init__(self, columns, data):
        super().__init__()
        self._columns = columns
        self._data = data

    def rowCount(self, parent=None):
        return len(self._data)

    def columnCount(self, parent=None):
        return len(self._data[0])

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            return str(self._data[index.row()][index.column()])
        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self._columns[section]
            else:
                return section
        return None

class MemberPopup(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("직원 리스트 확인")
        self.setWindowIcon(QIcon("./image/icon.png"))  # 아이콘 파일 경로
        self.resize(640, 480)
        response = requests.get('http://localhost:8000/members')
        members = response.json()
        data = []
        for member in members:
            data.append([member['employee_id'],member['name'],member['reg_date']])
        model = MemberTableModel(['사번','이름','등록일'],data)
        table_view = QTableView()
        table_view.setModel(model)
        layout = QVBoxLayout()
        layout.addWidget(table_view)
        self.setLayout(layout)
