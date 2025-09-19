from PyQt5.QtWidgets import(
     QDialog, QVBoxLayout, QCheckBox, QComboBox, QPushButton,
     QLabel, QSpinBox
)
from app.gui.target_layout import TargetLayout
from app.cam.detector_config import DetectorState

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.config = DetectorState()
        self.setWindowTitle("환경설정")
        self.resize(400, 400)
        # 출퇴근 모드 체크박스
        self.mode_checkbox = QCheckBox("출근 모드")
        self.mode_checkbox.setChecked(self.config['mode'] == 'check_in')
        # 사용 모델 - recognition model 사용 여부
        self.recognition_model = QCheckBox("얼굴 인식모델 사용")
        self.recognition_model.setChecked(self.config['recognition_model'])
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
        layout.addWidget(self.mode_checkbox)
        layout.addWidget(self.recognition_model)
        layout.addWidget(self.resolution_combo)
        layout.addWidget(QLabel("탐지 대상 선택(너비 x 높이)"))
        layout.addLayout(target_layout)
        # layout.addLayout(size_layout)
        layout.addWidget(QLabel("탐지 최소 프레임 수"))
        layout.addWidget(self.min_frame_spin)
        layout.addWidget(self.save_button)
        self.setLayout(layout)
        
    def accept(self) -> None:
        self.config['mode'] = 'check_in' if self.mode_checkbox.isChecked() else 'check_out'
        self.config['recognition_model'] = self.recognition_model.isChecked()
        self.config['width'], self.config['height'] = map(int, self.resolution_combo.currentText().split('x'))
        self.config['target_list'] = self.target_list.get_targets()
        self.config['count_limit'] = self.min_frame_spin.value()
        self.config.save()        
        return super().accept()