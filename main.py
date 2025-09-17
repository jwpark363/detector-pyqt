import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from lib.detector_cam import DetectorCam
from gui.main_layout import MainLayout
from lib.object_tracker import ObjectTracker
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("./image/icon.png"))
    win = MainLayout()
    detector = DetectorCam()
    tracker = ObjectTracker()
    tracker.init_config(win.get_config())
    tracker.set_logger(win.get_logger())
    detector.set_viewer(win.get_viewer())
    detector.set_tracker(tracker)
    detector.set_config(win.get_config())
    win.set_cam_object(detector)
    win.show()
    sys.exit(app.exec_())