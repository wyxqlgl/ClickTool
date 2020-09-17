import csv
import datetime
import os
import sqlite3
import time
from threading import Thread

from pynput import keyboard, mouse
from pynput.keyboard import Key

#图片录制脚本
class pictureMonitoring():
    def __init__(self):
        self.content
    def pictureScriptRecord(self):
        parent = os.path.dirname(os.path.realpath(__file__))
        self.timeStamp = int(time.mktime(datetime.datetime.now().timetuple()))
        self.dateCount = int(time.mktime(datetime.datetime.now().timetuple()) * 1000)
        conn = sqlite3.connect('pricture.db')
        c = conn.cursor()
        cursors = c.execute("SELECT *  from pricture where isstart=1")
        if len(cursors.fetchall()) > 0:
            conn.close()
            conn = sqlite3.connect('pricture.db')
            c = conn.cursor()
            cursor = c.execute("SELECT picturename,isstart  from pricture ORDER BY createtime DESC")
            self.mainwind.showMinimized()
            f = open('pictureScript' + str(self.timeStamp) + '.csv', 'w', encoding='utf-8', newline='')
            t = Thread(target=self.clickPictureMouthList)
            t.start()
            t2 = Thread(target=self.passkeybocksLister)
            t2.start()
            t.join()
            t2.join()
            self.mainwind.showNormal()
            for en in cursor:
                for et in range(0, 2):
                    if en[1] == 1 and et == 0:
                        self.saveScript(parent + '/pictureScript' + str(self.timeStamp) + '.csv', en[0])
        conn.close()
        self.loadDb()
    def clickPictureMouthList(self):
        with mouse.Listener(on_move=None, on_click=self.picture_on_click,
                            on_scroll=self.picture_on_scroll) as self.mouset:
            self.mouset.join()

    def passkeybocksLister(self):
        with keyboard.Listener(on_press=self.picture_on_press, on_release=self.picture_on_release) as self.keybocks:
            self.keybocks.join()

    def picture_on_click(self, x, y, button, pressed):
        end = int(time.mktime(datetime.datetime.now().timetuple()) * 1000)
        values = [
            (self.count, button, 'click', x, y, pressed, '', '', end - self.dateCount),
        ]
        self.dateCount = end
        self.savePictureData(values)
        self.count = self.count + 1

    def picture_on_scroll(self, x, y, dx, dy):
        end = int(time.mktime(datetime.datetime.now().timetuple()) * 1000)
        values = [
            (self.count, 'scroll', 'scroll', x, y, '', dx, dy, end - self.dateCount),
        ]
        self.dateCount = end
        self.savePictureData(values)
        self.count = self.count + 1

    def picture_on_press(self, key):
        if key == Key.f10:
            return;
        end = int(time.mktime(datetime.datetime.now().timetuple()) * 1000)
        values = [
            (self.count, key, 'press', '', '', '', '', '', end - self.dateCount),
        ]
        self.dateCount = end
        self.savePictureData(values)
        self.count = self.count + 1

    def picture_on_release(self, key):
        if key == Key.f10:
            self.keybocks.stop()
            self.mouset.stop()
            return;
        end = int(time.mktime(datetime.datetime.now().timetuple()) * 1000)
        values = [
            (self.count, key, 'release', '', '', '', '', '', end - self.dateCount),
        ]
        self.dateCount = end
        self.savePictureData(values)
        self.count = self.count + 1

    def savePictureData(self, values):
        with open('pictureScript' + str(self.timeStamp) + '.csv', 'a+', encoding='utf-8', newline='') as fp:
            writer = csv.writer(fp)  # 获取文件“写笔”
            writer.writerows(values)

    def saveScript(self, path,picturename):
        conn = sqlite3.connect('pricture.db')
        c = conn.cursor()
        c.execute(
            "UPDATE pricture set 'script'='"+path+"' where picturename= '" + str(picturename) + "'")
        conn.commit()
        conn.close()