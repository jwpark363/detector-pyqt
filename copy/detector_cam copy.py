import sys, threading
import cv2
import json
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QLabel, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QFileDialog
)
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QImage, QPixmap, QIcon
from setting_dialog import SettingsDialog
from watchdog.observers import Observer
from file_handler import FileCreatedHandler

CONFIG_FILE = 'config.json'
WATCH_DIR = './captured'

class DetectorCam(QWidget):
    def __init__(self):
        super().__init__()
        ## capture image
        self.current_frame = None
        ## load config
        with open(CONFIG_FILE,'r', encoding='utf-8') as f:
            system_config = json.load(f)
        self.SYSTEM_SETTING = system_config
        print('system setting', self.SYSTEM_SETTING)
        self.setWindowTitle("근태의 전설")
        self.resize(self.SYSTEM_SETTING['width'], self.SYSTEM_SETTING['height'])
        # ✅ 아이콘 설정
        self.setWindowIcon(QIcon("./image/icon.png"))  # 아이콘 파일 경로
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        # 초기 이미지 설정
        self.init_image()
        ## 버튼 시작, 환경 설정
        self.cam_opened = False
        self.start_button = QPushButton("카메라 시작")
        self.start_button.clicked.connect(self.start_camera)
        self.setting_button = QPushButton("환경 설정")
        self.setting_button.clicked.connect(self.open_settings)
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.setting_button)
        ## 전체 레이아웃
        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        layout.addLayout(button_layout)
        self.setLayout(layout)
        self.cap = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        ## 파일 생성 감시 이벤트
        self.file_handler = FileCreatedHandler('event handler',WATCH_DIR)
        self.observer = Observer()
        self.observer.schedule(self.file_handler,WATCH_DIR,recursive=False)
        threading.Thread(target=self.observer.start, daemon=True).start()
    def start_camera(self):
        print(self.cam_opened)
        if self.cam_opened:
            self.timer.stop()
            if self.cap:
                self.cap.release()
            self.start_button.setText("카메라 시작")
            self.cam_opened = False
            self.init_image()
        else:
            self.cap = cv2.VideoCapture(0)  # 0번 카메라
            self.timer.start(30)  # 30ms마다 프레임 업데이트
            self.start_button.setText("카메라 종료")
            self.cam_opened = True
    def open_settings(self):
        dialog = SettingsDialog(self,self.SYSTEM_SETTING)
        if dialog.exec_():
            self.SYSTEM_SETTING = dialog.get_settings()
            self.resize(self.SYSTEM_SETTING['width'], self.SYSTEM_SETTING['height'])
            ## save config
            with open(CONFIG_FILE,'w') as f:
                json.dump(self.SYSTEM_SETTING,f,indent=4)
            ## 파일 저장 이벤트 테스트
            self.save_image()
    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            if self.SYSTEM_SETTING['flip']:
                frame = cv2.flip(frame,1)
            ## 현재 프레임 저장
            self.current_frame = frame
            h, w, ch = frame.shape
            bytes_per_line = ch * w
            qt_image = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
            self.image_label.setPixmap(QPixmap.fromImage(qt_image))
    def save_image(self):
        ## 현재 프레임 저장
        if self.current_frame is not None:
            # print(self.current_frame)
            captured_image = self.current_frame.copy()
            print(type(captured_image),captured_image.shape)
            captured_file = f'{WATCH_DIR}/{datetime.today().timestamp()}.jpg'
            cv2.imwrite(captured_file, captured_image)
    def closeEvent(self, event):
        self.timer.stop()
        if self.cap:
            self.cap.release()
    def init_image(self):
        # 초기 이미지 설정
        pixmap = QPixmap("./image/cam.png")  # 이미지 파일 경로
        self.image_label.setPixmap(
            pixmap.scaled(self.SYSTEM_SETTING['width'],self.SYSTEM_SETTING['height'], Qt.KeepAspectRatio)
        )
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = DetectorCam()
    win.show()
    sys.exit(app.exec_())