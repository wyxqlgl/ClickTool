import os
import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QHeaderView, QAbstractItemView, QTableWidget
from qtpy import QtCore

from PictureClicked import pictureClicked #动图定位识别
from MouthKeyMethod import MouthKeyMethod #键盘鼠标设置
from ScriptRecording import scriptRecording #录制及执行脚本
from click import Ui_MainWindow #主页面
from PictureScreenshot import pictureScreenshot
class mainWind(MouthKeyMethod,scriptRecording,pictureClicked):
    def __init__(self):
        self.contends = ""
        self.path = ""
        self.y1 = 0
        self.x1 = 0
        self.y2 = 0
        self.x2 = 0
        self.count = 0
        self.dateCount=0
        self.picturename = None
        self.timeStamp=0
        self.app = QApplication(sys.argv)
        self.mainwind = QMainWindow()
        self.app.setWindowIcon(QIcon('mouth.png'))
        self.click=Ui_MainWindow()
        self.click.setupUi(self.mainwind)
        self.demo = pictureScreenshot(None, self.mainwind,self.click)
        self.demo.setWindowFlags(QtCore.Qt.CustomizeWindowHint)
        self.demo.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.demo.setWindowFlags(QtCore.Qt.WindowStaysOnBottomHint)
        self.demo.setWindowState(QtCore.Qt.WindowMaximized)
        self.demo.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.demo.setWindowOpacity(0.3)
        self.load_config()
        self.loadDb()
        self.click.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.click.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.click.tableWidget.setAlternatingRowColors(1)
        self.click.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.click.tableWidget.setStyleSheet("selection-background-color: #0000FF");
        self.click.tableWidget.setStyleSheet("QTableView::Item{background-color:#00FF00}");
        self.click.timeEdit.setDisplayFormat("HH:mm:ss")
        self.click.pushButton.clicked.connect(self.clickMothed)
        self.click.toolButton.clicked.connect(self.getFile)
        self.click.toolButton_2.clicked.connect(lambda:self.getCoordinate(1))
        self.click.toolButton_3.clicked.connect(lambda:self.getCoordinate(2))
        self.click.toolButton_4.clicked.connect(self.scriptRecord)
        self.click.toolButton_5.clicked.connect(self.runRecord)
        self.click.toolButton_6.clicked.connect(lambda: os.startfile(self.click.lineEdit_9.text()))
        self.click.toolButton_7.clicked.connect(lambda: os.startfile(os.path.dirname(self.click.lineEdit_9.text())))
        self.click.toolButton_9.clicked.connect(self.screenshot)
        self.click.toolButton_8.clicked.connect(self.getFilePicture)
        self.click.toolButton_10.clicked.connect(self.pictureScriptRecord)
        self.click.toolButton_11.clicked.connect(self.clickAction)
        self.mainwind.show()
        self.app.exit(self.app.exec_())