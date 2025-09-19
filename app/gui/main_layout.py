import json
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
)
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QImage, QPixmap, QIcon
from app.gui.setting_dialog import SettingsDialog
from app.gui.log_popup import LogPopup
from app.cam.detector_config import DetectorState

CONFIG_FILE = 'config.json'
WATCH_DIR = './captured'

class MainLayout(QWidget):
    def __init__(self):
        super().__init__()
        ## load config
        self.config = DetectorState()
        self.config['add_newmember'] = False
        print('system setting', self.config)
        self.setWindowTitle("근태의 전설")
        self.resize(self.config['width'], self.config['height'])
        # 아이콘 설정
        self.setWindowIcon(QIcon("./image/icon.png"))  # 아이콘 파일 경로
        self.image_label = QLabel() ## 메인 화면 뷰어
        self.image_label.setAlignment(Qt.AlignCenter)
        # 초기 이미지 설정
        self.init_image()
        ## log window
        self.logger = LogPopup()
        ## 버튼 시작, 환경 설정
        self.start_button = QPushButton("카메라 시작")
        self.start_button.clicked.connect(self.start_camera)
        self.new_button = QPushButton("신규 등록")
        self.new_button.clicked.connect(self.new_member)
        self.log_button = QPushButton("로그 확인")
        self.log_button.clicked.connect(self.show_logs)
        self.setting_button = QPushButton("환경 설정")
        self.setting_button.clicked.connect(self.open_settings)
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.new_button)
        button_layout.addWidget(self.setting_button)
        button_layout.addWidget(self.log_button)
        ## 전체 레이아웃
        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        layout.addLayout(button_layout)
        self.setLayout(layout)
        ## cam Close Event 처리 관련
        self.cam_object = None
    ## cam viewer
    def get_viewer(self):
        return self.image_label
    ## cam close setting
    def set_cam_object(self, cam_object):
        self.cam_object = cam_object
    def get_config(self):
        return self.config
    def get_logger(self):
        return self.logger
    ## 메인 화면 이미지 초기화    
    def init_image(self):
        # 초기 이미지 설정
        pixmap = QPixmap("./image/cam.png")  # 이미지 파일 경로
        self.image_label.setPixmap(
            pixmap.scaled(self.config['width'],self.config['height'], Qt.KeepAspectRatio)
        )
    def start_camera(self):
        if self.cam_object.cam_opened:
            self.cam_object.stop_camera()
            self.start_button.setText("카메라 시작")
            self.init_image()
        else:
            self.cam_object.start_camera()
            self.start_button.setText("카메라 종료")
    def new_member(self):
        ## cam이 오픈되어 있을때 가능
        if self.cam_object.cam_opened:
            if self.config['add_newmember']:
                print('신규 인력 사진 촬영 종료')
                self.new_button.setText('신규 등록')
                self.config['add_newmember'] = False
            else:
                print('### 신규 인력 사진 촬영 시작')
                self.new_button.setText('신규 저장')
                self.config['add_newmember'] = True
            
        
    def show_logs(self):
        self.logger.show()
    def open_settings(self):
        dialog = SettingsDialog(self)
        if dialog.exec_():
            self.resize(self.config['width'], self.config['height'])
    def closeEvent(self, event):
        if self.cam_object:
            self.cam_object.close_cam()