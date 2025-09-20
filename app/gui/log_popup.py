from datetime import datetime
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem
)
from PyQt5.QtGui import QIcon
# from PyQt5.QtCore import QTimer, QDateTime

class LogPopup(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("탐지 로그 확인")
        self.setWindowIcon(QIcon("./image/icon.png"))  # 아이콘 파일 경로
        self.resize(640, 480)
        layout = QVBoxLayout()
        self.table = QTableWidget()
        # self.table.setEditTriggers(QTableWidget.AllEditTriggers)
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["시간","ID","구분","저장여부","파일","비고"])
        header = self.table.horizontalHeader()
        header.setStyleSheet("QHeaderView::section { background-color: lightgray; }")
        layout.addWidget(self.table)
        self.setLayout(layout)
        # # 타이머 설정
        # self.timer = QTimer(self)
        # self.timer.timeout.connect(self.add_log)
        # self.timer.start(500)  # 로그 파일 읽어 내용 추가

    def add_log(self,id,cls,saved,file,desc=''):
        row = self.table.rowCount()
        self.table.insertRow(row)
        timestamp = datetime.today().strftime('%Y.%m.%d-%H:%M:%S')
        if saved:
            etc = f'ID {id} 파일이 저장 되었습니다' + f'({desc})' if len(desc) > 0 else ''
        else:
            etc = f'ID {id}가 탐지 되었습니다.' + f'({desc})' if len(desc) > 0 else ''
        self.table.setItem(row, 0, QTableWidgetItem(str(timestamp)))
        self.table.setItem(row, 1, QTableWidgetItem(str(id)))
        self.table.setItem(row, 2, QTableWidgetItem(str(cls)))
        self.table.setItem(row, 3, QTableWidgetItem(str(saved)))
        self.table.setItem(row, 4, QTableWidgetItem(str(file)))
        self.table.setItem(row, 5, QTableWidgetItem(str(etc)))
    def add_tts_log(self,id,cls,result):
        row = self.table.rowCount()
        self.table.insertRow(row)
        timestamp = datetime.today().strftime('%Y.%m.%d-%H:%M:%S')
        etc = f'ID {id}가 처리 되었습니다. ({result})'
        self.table.setItem(row, 0, QTableWidgetItem(str(timestamp)))
        self.table.setItem(row, 1, QTableWidgetItem(str(id)))
        self.table.setItem(row, 2, QTableWidgetItem(str(cls)))
        self.table.setItem(row, 3, QTableWidgetItem('TTS'))
        self.table.setItem(row, 4, QTableWidgetItem(''))
        self.table.setItem(row, 5, QTableWidgetItem(etc))
        
    # def update_log(self,row,log):
    #     for idx, data in enumerate(log):
    #         self.table.item(row,idx).setText(str(data))
'''
log_type : 1 - debuger, 
'''
# def logging(log_type,)