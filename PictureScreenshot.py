import datetime
import os
import sqlite3
import time

import pyautogui
from PyQt5 import QtCore

from PyQt5.QtCore import QDir, Qt
from PyQt5.QtGui import QPainter, QBrush, QColor, QPen
from PyQt5.QtWidgets import QWidget, QFileDialog, QTableWidgetItem, QPushButton, QMenu


class pictureScreenshot(QWidget):
    def __init__(self, parent=None,mainwind=None,click=None):
        super(pictureScreenshot, self).__init__(parent)
        self.rect = None
        self.xstart=None
        self.mainwind = mainwind
        self.ystart = None
        self.xend=None
        self.yend=None
        self.path=""
        self.clicks=click



    # 重写绘制函数
    def paintEvent(self, event):
        # 初始化绘图工具
        qp = QPainter()
        # 开始在窗口绘制
        qp.begin(self)
        # 自定义画点方法
        if self.rect:
            self.drawRect(qp)
        # 结束在窗口的绘制


        qp.end()

    def drawRect(self, qp):
        # 创建红色，宽度为4像素的画笔
        pen = QPen()
        pen.setWidth(4)
        pen.setColor(Qt.red)
        pen.setStyle(Qt.SolidLine)
        pen.setCapStyle(Qt.FlatCap)
        pen.setJoinStyle(Qt.BevelJoin)
        qp.setPen(pen)


        qp.setRenderHint(QPainter.Antialiasing)
        qp.setRenderHint(QPainter.TextAntialiasing)
        brush = QBrush()
        qc=QColor()
        qc.lighter()
        brush.setColor(qc.lighter(1))
        brush.setStyle(Qt.SolidPattern)
        qp.setBrush(brush)
        qp.drawRect(*self.rect)
    # 重写三个时间处理
    def mousePressEvent(self, event):

        self.rect = (event.x(), event.y(), 0, 0)
        poit=event.pos()
        self.xstart=poit.x()
        self.ystart=poit.y()
        # self.xstart,self.ystart=self.rect

    def getFile(self):
        curdir=QDir.currentPath()
        adir=QFileDialog.getExistingDirectory(self,"选择一个目录",curdir,QFileDialog.ShowDirsOnly)
        self.path=adir

    def mouseReleaseEvent(self, event):
        poit = event.pos()
        self.xend = poit.x()
        self.yend = poit.y()
        self.close()
        img = pyautogui.screenshot(region=[self.xstart, self.ystart, self.xend - self.xstart, self.yend - self.ystart])  # x,y,w,h
        self.show()
        self.getFile()
        timeStamp = int(time.mktime(datetime.datetime.now().timetuple()))
        paths=self.path + '/screenshot' + str(timeStamp) + '.png'
        name='screenshot' + str(timeStamp) + '.png'
        img.save(paths)
        self.saveConfigRecording(paths,name)
        self.mainwind.show()
        self.close()



    def mouseMoveEvent(self, event):
        start_x, start_y = self.rect[0:2]
        self.rect = (start_x, start_y, event.x() - start_x, event.y() - start_y)
        self.update()


    def saveConfigRecording(self, path,name):
        conn = sqlite3.connect('pricture.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS pricture
               (
               'picturename' TEXT ,
               'pictureurl' TEXT ,
               'script' TEXT ,
               'createtime' DATETIME,
               'isstart' BOOLEAN );''')
        c.execute("INSERT INTO pricture ('picturename','pictureurl','createtime','isstart') VALUES ( '"+name+"', '"+path+"', '"+str(datetime.datetime.now())+"', False )")
        conn.commit()
        conn.close()
        self.loadDb()

    def loadDb(self):
        self.clicks.tableWidget.clearContents()
        self.clicks.tableWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.clicks.tableWidget.customContextMenuRequested.connect(self.generateMenus)
        self.clicks.tableWidget.setRowCount(0)
        conn = sqlite3.connect('pricture.db')
        c = conn.cursor()
        try:
            cursor = c.execute(
                "SELECT picturename,pictureurl,createtime,script,isstart from pricture ORDER BY createtime DESC")
            count = 0
            for en in cursor:
                ets = self.clicks.tableWidget.rowCount() + 1;
                self.clicks.tableWidget.setRowCount(ets)

                for et in range(0, 6):
                    check = QTableWidgetItem(en[0])
                    check.setCheckState(Qt.Unchecked)
                    if count % 2:
                        check.setFlags(QtCore.Qt.ItemIsUserCheckable |
                                       QtCore.Qt.ItemIsEnabled)
                        check.setCheckState(QtCore.Qt.Unchecked)
                    temp_data = ""
                    try:
                        temp_data = en[et]
                        if en[et] is None:
                            temp_data = ""
                    except:
                        temp_data = ""
                    # 转换后可插入表格
                    data = QTableWidgetItem(str(temp_data))
                    if et == 0:
                        if en[4] == 1:
                            check.setCheckState(Qt.Checked)
                        self.clicks.tableWidget.setItem(count, et, check)
                    else:
                        self.clicks.tableWidget.setItem(count, et, data)

                count = count + 1
            self.clicks.tableWidget.itemClicked.connect(self.handleItemClicked)
        except Exception as e:
            c.execute('''CREATE TABLE IF NOT EXISTS pricture
                             (
                             'picturename' TEXT ,
                             'pictureurl' TEXT ,
                             'script' TEXT ,
                             'createtime' DATETIME,
                             'isstart' BOOLEAN );''')
            conn.commit()
            print(e)
            return;
        conn.close()
    def handleItemClicked(self, item):
        if item.checkState() == QtCore.Qt.Checked:
            conn = sqlite3.connect('pricture.db')
            c = conn.cursor()
            c.execute(
                "UPDATE pricture set 'isstart'=True where picturename= '"+str(item.text())+"'")
            conn.commit()
            conn.close()

    def generateMenus(self, pos):
        row_num = -1
        for i in self.clicks.tableWidget.selectionModel().selection().indexes():
            row_num = i.row()
        if row_num >= 0:
            menu = QMenu()
            item1 = menu.addAction(u"删除")
            action = menu.exec_(self.clicks.tableWidget.mapToGlobal(pos))
            if action == item1:
                conn = sqlite3.connect('pricture.db')
                c = conn.cursor()
                sql = "DELETE from pricture where picturename='" + self.clicks.tableWidget.item(row_num, 0).text() + "';"
                c.execute(sql)
                conn.commit()
                conn.close()
                if os.path.exists(self.clicks.tableWidget.item(row_num, 1).text()):  # 如果文件存在
                    # 删除文件，可使用以下两种方法。
                    os.remove(self.clicks.tableWidget.item(row_num, 1).text())
                    # os.unlink(path)
                self.loadDb()
                menu.clear()
                return;
            else:
                menu.clear()
                return;
            menu.clear()
