import sys
import cv2
import numpy as np
from PyQt5.QtCore import Qt, QUrl, QTimer
from PyQt5.QtGui import QIcon, QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QAction, QSlider, QLabel, QToolBar, QMenuBar, QPushButton


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUI()
        self.timer = QTimer(self)
        self.timer.setInterval(20)
        self.timer.timeout.connect(self.displayFrame)

    def setupUI(self):
        # 创建菜单栏
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu("&File")
        openAction = QAction(QIcon(), "&Open", self)
        openAction.setShortcut("Ctrl+O")
        openAction.triggered.connect(self.openFile)
        fileMenu.addAction(openAction)

        # 创建工具栏
        toolBar = self.addToolBar("ToolBar")
        toolBar.addAction(openAction)

        # 创建打开文件按钮
        self.openBtn = QPushButton("Open", self)
        self.openBtn.setGeometry(10, self.height() - 50, 80, 30)
        self.openBtn.clicked.connect(self.openFile)

        # 创建QSlider组件
        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.setRange(0, 0)
        self.slider.sliderMoved.connect(self.setPosition)
        self.slider.setEnabled(False)
        self.slider.setGeometry(100, self.height() - 50, self.width() - 100, 50)

        # 创建QLabel组件用于显示视频帧
        self.videoWidget = QLabel(self)
        self.videoWidget.setGeometry(0, 0, self.width(), self.height() - 50)
        self.videoWidget.setAlignment(Qt.AlignCenter)

        # 设置窗口属性
        self.setWindowTitle("Video Player")
        self.setGeometry(100, 100, 800, 600)

    def openFile(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Video",
                                                  "", "Video Files (*.mp4 *.avi)")
        if fileName != '':
            self.playVideo(fileName)

    def setPosition(self, position):
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, position)

    def displayFrame(self):
        ret, frame = self.cap.read()
        if ret:
            # 将BGR格式的图像转换为RGB格式
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # 将numpy数组转换为QImage对象
            qImg = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
            # 将QImage对象转换为QPixmap对象
            pixmap = QPixmap.fromImage(qImg)
            # 将QPixmap对象显示在QLabel组件中
            self.videoWidget.setPixmap(pixmap)
            # 更新进度条
            position = self.cap.get(cv2.CAP_PROP_POS_FRAMES)
            self.slider.setValue(int(position))

    def playVideo(self, fileName):
        self.cap = cv2.VideoCapture(fileName)
        # 获取视频帧数和帧率
        numFrames = self.cap.get(cv2.CAP_PROP_FRAME_COUNT)
        fps = self.cap.get(cv2.CAP_PROP_FPS)
        # 设置进度条的范围
        self.slider.setRange(0, int(numFrames))
        # 开始播放视频
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        self.timer.start()
        self.slider.setEnabled(True)

    def closeEvent(self, event):
        self.timer.stop()
        self.cap.release()
        event.accept()

    def start(self):
        # 显示窗口
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.start()
    sys.exit(app.exec_())