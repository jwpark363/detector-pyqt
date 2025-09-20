import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon, QFont
from app.cam.detector_cam import DetectorCam
from app.gui.main_layout import MainLayout
from app.cam.object_tracker import ObjectTracker
from app.cam.detector_config import DetectorState

if __name__ == "__main__":
    ## 전체 상태관리 클래스 초기화(싱글톤)
    config = DetectorState() ## 필요한 객체에서 생성하여 사용하면됨

    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("./image/icon.png"))
    # 원하는 폰트 크기 설정
    font = QFont()
    font.setPointSize(12)
    app.setFont(font)
    win = MainLayout()
    detector = DetectorCam()
    tracker = ObjectTracker()
    config.set_detector(detector)    
    config.set_viewer(win.get_viewer())    
    config.set_logger(win.get_logger())
    config.set_tracker(tracker)
    ## main window에 cam 연결 필요
    # win.set_cam_object(detector)
    win.show()
    sys.exit(app.exec_())