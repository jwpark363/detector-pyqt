from PyQt5.QtWidgets import(
     QDialog, QVBoxLayout, QCheckBox, QComboBox, QPushButton,
     QLabel, QListWidget, QListWidgetItem, QHBoxLayout, QSpinBox
)
from PyQt5.QtGui import QFont
from typing import Dict, List
from gui.target_layout import TargetLayout


class SettingsDialog(QDialog):
    def __init__(self, parent=None, config:Dict[str,str|bool|int|List[str]]={}):
        super().__init__(parent)
        self.config = config
        self.setWindowTitle("환경설정")
        self.resize(400, 400)
        # 원하는 폰트 크기 설정
        font = QFont()
        font.setPointSize(7)

        # 좌우 반전 체크박스
        self.flip_checkbox = QCheckBox("좌우 반전")
        self.flip_checkbox.setChecked(self.config['flip'])
        # 해상도 선택
        self.resolution_combo = QComboBox()
        self.resolution_combo.addItems(["640x480", "800x600", "1280x720"])
        self.resolution_combo.setCurrentText(f"{str(self.config['width'])}x{str(self.config['height'])}")
        ## 탐지 대상
        target_layout = QVBoxLayout()
        self.target_list = TargetLayout(self.config['target_list'])
        target_layout.addWidget(self.target_list)
        # 최소 프레임 수
        self.min_frame_spin = QSpinBox()
        self.min_frame_spin.setRange(1, 100)
        self.min_frame_spin.setValue(self.config['count_limit'])
        # 저장 버튼
        self.save_button = QPushButton("저장")
        self.save_button.clicked.connect(self.accept)

        layout = QVBoxLayout()
        layout.addWidget(self.flip_checkbox)
        layout.addWidget(self.resolution_combo)
        layout.addWidget(QLabel("탐지 대상 선택(너비 x 높이)"))
        layout.addLayout(target_layout)
        # layout.addLayout(size_layout)
        layout.addWidget(QLabel("탐지 최소 프레임 수"))
        layout.addWidget(self.min_frame_spin)
        layout.addWidget(self.save_button)
        self.setLayout(layout)
    ## 호출한 곳에서 처리
    def get_settings(self):
        self.config['flip'] = self.flip_checkbox.isChecked()
        self.config['width'], self.config['height'] = map(int, self.resolution_combo.currentText().split('x'))
        self.config['target_list'] = self.target_list.get_targets()
        self.config['count_limit'] = self.min_frame_spin.value()
        return self.config
