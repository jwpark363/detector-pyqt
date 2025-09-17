import json
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
)
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QImage, QPixmap, QIcon
from gui.setting_dialog import SettingsDialog
from gui.log_popup import LogPopup

CONFIG_FILE = 'config.json'
WATCH_DIR = './captured'

class MainLayout(QWidget):
    def __init__(self):
        super().__init__()
        ## load config
        with open(CONFIG_FILE,'r', encoding='utf-8') as f:
            system_config = json.load(f)
        self.SYSTEM_SETTING = system_config
        print('system setting', self.SYSTEM_SETTING)
        self.setWindowTitle("근태의 전설")
        self.resize(self.SYSTEM_SETTING['width'], self.SYSTEM_SETTING['height'])
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
        self.log_button = QPushButton("로그 확인")
        self.log_button.clicked.connect(self.show_logs)
        self.setting_button = QPushButton("환경 설정")
        self.setting_button.clicked.connect(self.open_settings)
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.start_button)
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
        return self.SYSTEM_SETTING
    def get_logger(self):
        return self.logger
    ## 메인 화면 이미지 초기화    
    def init_image(self):
        # 초기 이미지 설정
        pixmap = QPixmap("./image/cam.png")  # 이미지 파일 경로
        self.image_label.setPixmap(
            pixmap.scaled(self.SYSTEM_SETTING['width'],self.SYSTEM_SETTING['height'], Qt.KeepAspectRatio)
        )
    def start_camera(self):
        if self.cam_object.cam_opened:
            self.cam_object.stop_camera()
            self.start_button.setText("카메라 시작")
            self.init_image()
        else:
            self.cam_object.start_camera()
            self.start_button.setText("카메라 종료")
    def show_logs(self):
        self.logger.show()        
    def open_settings(self):
        dialog = SettingsDialog(self, self.SYSTEM_SETTING)
        if dialog.exec_():
            self.SYSTEM_SETTING = dialog.get_settings()
            self.resize(self.SYSTEM_SETTING['width'], self.SYSTEM_SETTING['height'])
            if self.cam_object:
                self.cam_object.set_config(self.SYSTEM_SETTING)
            ## save config
            with open(CONFIG_FILE,'w') as f:
                json.dump(self.SYSTEM_SETTING,f,indent=4)
    def closeEvent(self, event):
        if self.cam_object:
            self.cam_object.close_cam()