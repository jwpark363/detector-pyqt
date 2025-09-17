from PyQt5.QtWidgets import (
    QApplication, QLabel, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QFileDialog
)
class Test(QVBoxLayout):
    def __init__(self, name, age):
      self.name = name
      self.age = age