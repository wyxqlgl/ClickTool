import sqlite3
from threading import Thread
#图片录制脚本
class pictureMonitoring():
    def pictureScriptRecord(self):
        conn = sqlite3.connect('pricture.db')
        c = conn.cursor()
        cursors = c.execute("SELECT count(*)  from pricture where isstart=1")
        isStart=False
        for en in cursors:
            isStart=True
        conn.close()
        if isStart:
            self.pictureScriptReport()
        self.loadDb()
    def pictureScriptReport(self):
        self.mainwind.close()
        self.monitoring.isPicture= True
        self.monitoring.show()

