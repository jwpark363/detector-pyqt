import sys, cv2, threading
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QLabel, QWidget
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap, QIcon
from ultralytics import YOLO
from watchdog.observers import Observer
from file_handler import FileCreatedHandler
from gui.main_layout import MainLayout
from object_tracker import ObjectTracker

CONFIG_FILE = 'config.json'
WATCH_DIR = './captured'

# class DetectorCam(QWidget):
class DetectorCam:
    def __init__(self):
        print('*** new detector cam object...')
        self.viewer = None
        self.flip = True
        self.tracker = None
        ## cam 처리에 필요한 변수들
        self.cam = None
        self.cam_opened = False
        self.current_frame = None
        print('*** load YOLO model...')
        self.model = YOLO("yolo11n.pt")
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        ## 파일 생성 감시 이벤트
        print('*** File Event Handler initializing...')
        self.file_handler = FileCreatedHandler('event handler',WATCH_DIR)
        self.observer = Observer()
        self.observer.schedule(self.file_handler,WATCH_DIR,recursive=False)
        threading.Thread(target=self.observer.start, daemon=True).start()
        print('*** new detector cam object completed!!!')
    ## 종료 이벤트시 timer, cam 종료 처리 위해
    def close_cam(self):
        self.timer.stop()
        if self.cam is not None:
            self.cam.release()    
    ## cam viewer
    def set_viewer(self, viewer:QLabel):
        self.viewer = viewer
    ## flip
    def set_config(self, config):
        # print('detector',config)
        self.flip = config['flip']
        if self.tracker:
            self.tracker.init_config(config)
    ## tracker
    def set_tracker(self, tracker:ObjectTracker):
        self.tracker = tracker
    ## 카메라 스타트    
    def start_camera(self):
        self.cam = cv2.VideoCapture(0)  # 0번 카메라
        self.timer.start(50)  # 30ms마다 프레임 업데이트
        self.cam_opened = True
    def stop_camera(self):
        self.timer.stop()
        if self.cam:
            self.cam.release()
        self.cam_opened = False
    # def reset_setting(self,setting):
    #     self.setting = setting
    #     self.resize(self.setting['width'], self.setting['height'])
    def update_frame(self):
        ret, frame = self.cam.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = None
            if self.model:
                results = self.model.track(frame, persist=True, verbose=False, )
            if self.flip:
                frame = cv2.flip(frame,1)
            ## 현재 프레임 저장
            self.current_frame = frame
            ## tracking
            if results and len(results) > 0 :
                if self.tracker:
                    self.tracker.check_n_save(frame,results[0].boxes.data)
                frame = results[0].plot()
                ## 사이즈 출력
                for box in results[0].boxes.data:
                    box = box.to('cpu')
                    x1,y1,x2,y2 = box[:4].numpy().astype(int)
                    cv2.putText(frame, ## 박스의 넓이 x 높이 출력
                        f'{abs(x2-x1)}x{abs(y2-y1)}',
                        (x1+5,y1+25),
                        cv2.FONT_HERSHEY_SIMPLEX,1,
                        (0,0,255),
                        2
                    )
            h, w, ch = frame.shape
            bytes_per_line = ch * w
            qt_image = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
            self.viewer.setPixmap(QPixmap.fromImage(qt_image))
    def save_image(self):
        ## 현재 프레임 파일로 저장
        if self.current_frame is not None:
            # print(self.current_frame)
            captured_image = self.current_frame.copy()
            captured_image = cv2.cvtColor(captured_image,cv2.COLOR_RGB2BGR)
            print(type(captured_image),captured_image.shape)
            captured_file = f'{WATCH_DIR}/{datetime.today().timestamp()}.jpg'
            cv2.imwrite(captured_file, captured_image)
