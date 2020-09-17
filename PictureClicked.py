
import datetime
import os
import sqlite3

from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import  QMenu
from PyQt5.QtWidgets import  QFileDialog
from PictureMonitoring import pictureMonitoring
from PictureScriptRecording import pictureScriptRecording
from PictureScreenshot import  QTableWidgetItem
#图片的内部操作
class pictureClicked(pictureMonitoring,pictureScriptRecording):
    def clickAction(self):
        conn = sqlite3.connect('pricture.db')
        c = conn.cursor()
        cursor = c.execute("SELECT picturename,pictureurl,createtime,script,isstart  from pricture ORDER BY createtime DESC")
        for en in cursor:
            if en[4] == 1:
                 try :
                     self.pictureRunRecord(en[3],en[1])
                 except Exception as e:
                     print(e)
    def screenshot(self):
        self.mainwind.close()
        self.demo.show()
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
    def getFilePicture(self):
        fileName, filetype = QFileDialog.getOpenFileNames(None, "请选择要发送的文件",
                                                          "c:/",
                                                    "Text Files (*.png)")
        try:
            path = str(fileName[0])
            self.click.lineEdit_11.setText(path)
            pathname=os.path.basename(path)
            conn = sqlite3.connect('pricture.db')
            c = conn.cursor()
            c.execute(
                "INSERT INTO pricture ('picturename','pictureurl','createtime','isstart') VALUES ( '" + pathname + "', '" + path + "', '" + str(
                    datetime.datetime.now()) + "', False )")
            conn.commit()
            conn.close()
            self.loadDb()
        except :
            return

    def handleItemClicked(self, item):
        conn = sqlite3.connect('pricture.db')
        c = conn.cursor()
        if item.checkState() == QtCore.Qt.Checked:
            c.execute(
                "UPDATE pricture set 'isstart'=True where picturename= '"+str(item.text())+"'")
        else:
            c.execute(
                "UPDATE pricture set 'isstart'=FALSE where picturename= '" + str(item.text()) + "'")
        conn.commit()
        conn.close()







