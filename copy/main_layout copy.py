import threading
import json
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QImage, QPixmap, QIcon
from setting_dialog import SettingsDialog
from watchdog.observers import Observer
from file_handler import FileCreatedHandler

CONFIG_FILE = 'config.json'
WATCH_DIR = './captured'

class MainLayout(QVBoxLayout):
    def __init__(self,_parent):
        super().__init__()
        self._parent = _parent
        ## load config
        with open(CONFIG_FILE,'r', encoding='utf-8') as f:
            system_config = json.load(f)
        self.SYSTEM_SETTING = system_config
        print('system setting', self.SYSTEM_SETTING)
        ## 이미지 처리 부분 반드시 연결해야함
        self.image_label = _parent.viewer
        self.image_label.setAlignment(Qt.AlignCenter)
        self.init_image()
        ## 버튼 시작, 환경 설정
        self.start_button = QPushButton("카메라 시작")
        self.start_button.clicked.connect(self.start_camera)
        self.setting_button = QPushButton("환경 설정")
        self.setting_button.clicked.connect(self.open_settings)
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.setting_button)
        ## 전체 레이아웃
        # layout = QVBoxLayout()
        self.addWidget(self.image_label)
        self.addLayout(button_layout)
        ## 파일 생성 감시 이벤트
        self.file_handler = FileCreatedHandler('event handler',WATCH_DIR)
        self.observer = Observer()
        self.observer.schedule(self.file_handler,WATCH_DIR,recursive=False)
        threading.Thread(target=self.observer.start, daemon=True).start()
    def init_image(self):
        # 초기 이미지 설정
        pixmap = QPixmap("./image/cam.png")  # 이미지 파일 경로
        self.image_label.setPixmap(
            pixmap.scaled(self.SYSTEM_SETTING['width'],self.SYSTEM_SETTING['height'], Qt.KeepAspectRatio)
        )
    def start_camera(self):
        if self._parent.cam_opened:
            self._parent.stop_camera()
            self.start_button.setText("카메라 시작")
            self.init_image()
        else:
            self._parent.start_camera()
            self.start_button.setText("카메라 종료")
    def open_settings(self):
        dialog = SettingsDialog(self._parent,self.SYSTEM_SETTING)
        if dialog.exec_():
            self.SYSTEM_SETTING = dialog.get_settings()
            self._parent.reset_setting(self.SYSTEM_SETTING)
            ## save config
            with open(CONFIG_FILE,'w') as f:
                json.dump(self.SYSTEM_SETTING,f,indent=4)