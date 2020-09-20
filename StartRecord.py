import csv
import time
import datetime
import pyautogui
from PyQt5.QtWidgets import QMessageBox
class startRecord():
    def __init__(self):
        self.content
    def runRecord(self):
       QMessageBox.about(None, "提示!!!", "请2秒内放入执行位置开始执行脚本")
       self.mainwind.hide()
       time.sleep(2)
       with open('script.csv', 'r') as f:
           self.content = csv.reader(f)
           for das in self.content:
               if das[2]=='scroll':
                   self.runScroll(das)
               elif das[2]=='press':
                   self.runPress(das)
               elif das[2] == 'release':
                   self.runRelease(das)
               elif das[2] == 'click':
                   self.runClick(das)
               elif das[2] == 'move':
                   self.runMove(das)
       self.mainwind.show()
       self.click.statusbar.clearMessage()
       self.click.statusbar.showMessage("执行脚本成功!!")
    def runScroll(self,das):
        pyautogui.FAILSAFE = False
        count = datetime.datetime.now().time().second
        sc=int(das[7])
        while True:
          pyautogui.scroll(sc*50,x=int(das[3]), y=int(das[4]))
          end = datetime.datetime.now().time().second
          if end-count >=int(das[6])/1000:
              break
    def runPress(self,das):
        time.sleep(int(das[6])/1000)
        pyautogui.keyDown(str(das[1]).replace("'",""))
    def runRelease(self,das):
        time.sleep(int(das[6])/1000)
        pyautogui.keyUp(str(das[1]).replace("'",""))
    def runClick(self,das):
        time.sleep(int(das[6])/1000)
        pyautogui.click(x=int(das[3]), y=int(das[4]), clicks=1, interval=0.0, button=str(das[1]).replace("Button.",""), duration=0.0, tween=pyautogui.linear)
    def runMove(self,das):
        time.sleep(int(das[6])/1000)
        pyautogui.moveTo(int(das[3]), int(das[4]))


