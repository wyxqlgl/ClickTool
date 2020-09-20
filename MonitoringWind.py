import csv
import datetime
import os
import sqlite3
import time

from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QMenu


class monitoringWind(QWidget):
    def __init__(self, parent=None, mainwind=None, click=None,isPicture=None):
        super(monitoringWind, self).__init__(parent)
        self.mainwind=mainwind
        self.click=click
        self.count = 0
        self.isPicture=isPicture
        self.timeStamp = int(time.mktime(datetime.datetime.now().timetuple()))
        self.dateCount = int(time.mktime(datetime.datetime.now().timetuple()) * 1000)
    def mousePressEvent(self, event):
        pt = event.pos()
        end = int(time.mktime(datetime.datetime.now().timetuple()) * 1000)
        if event.button() == Qt.LeftButton:
            values = [
                (self.count, 'LeftButton', 'clickPress', pt.x(), pt.y(), '', end - self.dateCount),
            ]
        elif event.button()==Qt.RightButton:
            values = [
                (self.count, 'RightButton', 'clickPress', pt.x(), pt.y(), '', end - self.dateCount),
            ]
        self.dateCount = end
        self.saveData(values)
        self.count = self.count + 1
    def mouseReleaseEvent(self, event):
        pt = event.pos()
        end = int(time.mktime(datetime.datetime.now().timetuple()) * 1000)
        if event.button() == Qt.LeftButton:
            values = [
                (self.count, 'LeftButton', 'clickRelease', pt.x(), pt.y(), '', end - self.dateCount),
            ]
        elif event.button() == Qt.RightButton:
            values = [
                (self.count, 'RightButton', 'clickRelease', pt.x(), pt.y(), '', end - self.dateCount),
            ]
        self.dateCount = end
        self.saveData(values)
        self.count = self.count + 1
    def mouseDoubleClickEvent(self, event):
        pt=event.pos()
        end = int(time.mktime(datetime.datetime.now().timetuple()) * 1000)
        if event.button()==Qt.LeftButton:
            values = [
                (self.count, 'DoubleLeftButton', 'click', pt.x(), pt.y(),'', end - self.dateCount),
            ]
        elif event.button()==Qt.RightButton:
            values = [
                (self.count, 'DoubleRightButton', 'click', pt.x(), pt.y(), '', end - self.dateCount),
            ]
        self.dateCount = end
        self.saveData(values)
        self.count = self.count + 1
    def wheelEvent(self, event):
        point=event.pos()
        end = int(time.mktime(datetime.datetime.now().timetuple()) * 1000)
        values = [
            (self.count, 'scroll', 'scroll', point.x(), point.y(), '', end - self.dateCount),
        ]
        self.dateCount = end
        self.saveData(values)
        self.count = self.count + 1

    def keyPressEvent(self, event):
        keys = event.key()
        if keys == Qt.Key_F10:
            return;
        end = int(time.mktime(datetime.datetime.now().timetuple()) * 1000)
        values = [
            (self.count, keys, 'press', '', '', '',  end - self.dateCount),
        ]
        self.dateCount = end
        self.saveData(values)
        self.count = self.count + 1

    def keyReleaseEvent(self, event):
        keys=event.key()
        if keys == Qt.Key_F10:
            if self.isPicture:
                self.saveReport()
            self.close()
            self.mainwind.show()
            return;
        end = int(time.mktime(datetime.datetime.now().timetuple()) * 1000)
        values = [
            (self.count, keys, 'release', '', '', '',  end - self.dateCount),
        ]
        self.dateCount = end
        self.saveData(values)
        self.count = self.count + 1
    def mouseMoveEvent(self, event):
        if self.isPicture:
            return
        point=event.pos()
        end = int(time.mktime(datetime.datetime.now().timetuple()) * 1000)
        values = [
            (self.count, 'move', 'move', point.x(), point.y(), '',  end - self.dateCount),
        ]
        self.dateCount = end
        self.saveData(values)
        self.count = self.count + 1
    def saveData(self,values):
        if self.isPicture:
            with open('pictureScript' + str(self.timeStamp) + '.csv', 'a+', encoding='utf-8', newline='') as fp:
                writer = csv.writer(fp)  # 获取文件“写笔”
                writer.writerows(values)
        else:
            with open('script.csv', 'a+', encoding='utf-8', newline='') as fp:
                writer = csv.writer(fp)  # 获取文件“写笔”
                writer.writerows(values)
    def saveReport(self):
        parent = os.path.dirname(os.path.realpath(__file__))
        conn = sqlite3.connect('pricture.db')
        c = conn.cursor()
        cursor = c.execute("SELECT picturename,isstart  from pricture ORDER BY createtime DESC")
        for en in cursor:
            for et in range(0, 2):
                if en[1] == 1 and et == 0:
                    self.saveScript(parent + '/pictureScript' + str(self.timeStamp) + '.csv', en[0],c)
                    conn.commit()
        conn.close()
        self.loadDb()

    def saveScript(self, path, picturename,c):
        c.execute(
            "UPDATE pricture set 'script'='" + path + "' where picturename= '" + str(picturename) + "'")

    def loadDb(self):
        self.click.tableWidget.clearContents()
        self.click.tableWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.click.tableWidget.customContextMenuRequested.connect(self.generateMenu)
        self.click.tableWidget.setRowCount(0)

        conn = sqlite3.connect('pricture.db')
        c = conn.cursor()
        try :
            cursor = c.execute("SELECT picturename,pictureurl,createtime,script,isstart  from pricture ORDER BY createtime DESC")
            count=0
            for en in cursor:
                ets = self.click.tableWidget.rowCount() + 1;
                self.click.tableWidget.setRowCount(ets)

                for et in range(0,6):
                    check = QTableWidgetItem(en[0])
                    check.setCheckState(Qt.Unchecked)
                    if count % 2:
                        check.setFlags(QtCore.Qt.ItemIsUserCheckable |
                                      QtCore.Qt.ItemIsEnabled)
                        check.setCheckState(QtCore.Qt.Unchecked)
                    temp_data =""
                    try:
                        temp_data = en[et]
                        if en[et] is None:
                            temp_data =""
                    except:
                        temp_data = ""
                    # 转换后可插入表格
                    data = QTableWidgetItem(str(temp_data))
                    if et==0:
                        if en[4]==1:
                            check.setCheckState(Qt.Checked)
                        self.click.tableWidget.setItem(count, et, check)
                    else:
                        self.click.tableWidget.setItem(count, et, data)

                count=count+1
            self.click.tableWidget.itemClicked.connect(self.handleItemClicked)
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
    def generateMenu(self, pos):
        row_num = -1
        for i in self.click.tableWidget.selectionModel().selection().indexes():
            row_num = i.row()
        if row_num >=0:
            menu = QMenu()
            item1 = menu.addAction(u"删除")
            action = menu.exec_(self.click.tableWidget.mapToGlobal(pos))
            if action == item1:
                conn = sqlite3.connect('pricture.db')
                c = conn.cursor()
                sql="DELETE from pricture where picturename='"+self.click.tableWidget.item(row_num, 0).text()+"';"
                c.execute(sql)
                conn.commit()
                conn.close()

                if os.path.exists(self.click.tableWidget.item(row_num, 1).text()):  # 如果文件存在
                    # 删除文件，可使用以下两种方法。
                    os.remove(self.click.tableWidget.item(row_num, 1).text())
                if os.path.exists(self.click.tableWidget.item(row_num, 3).text()):  # 如果文件存在
                    # 删除文件，可使用以下两种方法。
                    os.remove(self.click.tableWidget.item(row_num, 3).text())
                    # os.unlink(path)
                self.loadDb()
                menu.clear()
                return
            else:
                menu.clear()
                return

    def handleItemClicked(self, item):
        conn = sqlite3.connect('pricture.db')
        c = conn.cursor()
        if item.checkState() == QtCore.Qt.Checked:
            c.execute(
                "UPDATE pricture set 'isstart'=True where picturename= '" + str(item.text()) + "'")
        else:
            c.execute(
                "UPDATE pricture set 'isstart'=FALSE where picturename= '" + str(item.text()) + "'")
        conn.commit()
        conn.close()


