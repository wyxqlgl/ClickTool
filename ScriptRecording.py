import configparser
import csv
import datetime
import os
import time
from threading import Thread
from pynput import mouse, keyboard
from pynput.keyboard import Key
from StartRecord import startRecord


class scriptRecording(startRecord):
    def __init__(self):
        self.keybocks
        self.mouset
    def scriptRecord(self):
        self.mainwind.showMinimized()
        f= open('script.csv', 'w',encoding='utf-8',newline='')
        parent = os.path.dirname(os.path.realpath(__file__))
        self.saveConfigRecording(parent+ "/script.csv")
        self.click.lineEdit_9.setText(parent + "/script.csv")
        self.dateCount=int(time.mktime(datetime.datetime.now().timetuple())*1000)
        t = Thread(target=self.mouthLister)
        t.start()
        t2 = Thread(target=self.keybocksLister)
        t2.start()
        t.join()
        t2.join()
        self.mainwind.showNormal()
    def on_move(self,x,y):
        end =int(time.mktime(datetime.datetime.now().timetuple())*1000)
        values = [
            (self.count, 'move', 'move',x,y,'','','',end-self.dateCount),
        ]
        self.dateCount = end
        self.saveData(values)
        self.count = self.count + 1
    def on_click(self,x,y,button,pressed):
        end =int(time.mktime(datetime.datetime.now().timetuple())*1000)
        values = [
            (self.count, button, 'click',x,y,pressed,'','',end-self.dateCount),
        ]
        self.dateCount = end
        self.saveData(values)
        self.count = self.count + 1
    def on_scroll(self,x,y,dx,dy):
        end =int(time.mktime(datetime.datetime.now().timetuple())*1000)
        values = [
            (self.count, 'scroll', 'scroll', x, y, '',dx,dy,end-self.dateCount),
        ]
        self.dateCount = end
        self.saveData(values)
        self.count = self.count + 1
    def on_press(self,key):
        if key == Key.f10:
            return;
        end =int(time.mktime(datetime.datetime.now().timetuple())*1000)
        values = [
            (self.count, key, 'press', '', '', '', '', '',end-self.dateCount),
        ]
        self.dateCount = end
        self.saveData(values)
        self.count=self.count+1
    def on_release(self,key):
        if key==Key.f10:
            self.keybocks.stop()
            self.mouset.stop()
            return;
        end =int(time.mktime(datetime.datetime.now().timetuple())*1000)
        values = [
            (self.count, key, 'release', '', '', '', '', '',end-self.dateCount),
        ]
        self.dateCount = end
        self.saveData(values)
        self.count = self.count + 1
    def saveData(self,values):
        with open('script.csv', 'a+', encoding='utf-8', newline='') as fp:
            writer = csv.writer(fp)  # 获取文件“写笔”
            writer.writerows(values)
    def mouthLister(self):
        with mouse.Listener(on_move=self.on_move, on_click=self.on_click, on_scroll=self.on_scroll) as self.mouset:
            self.mouset.join()
    def keybocksLister(self):
        with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as self.keybocks:
            self.keybocks.join()
    def saveConfigRecording(self,path):
        config = configparser.ConfigParser()
        try :
            config["SCRIPTDEFAULT"].clear()
            config["SCRIPTDEFAULT"] = {
                "scriptpaths": path
            }
        except Exception as e:
            config["SCRIPTDEFAULT"] = {
                "scriptpaths": path
            }
        with open('user.ini', 'r+')as configfile:
            config.write((configfile))





