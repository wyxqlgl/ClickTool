import csv
import datetime
import time

import pyautogui
from PyQt5.QtWidgets import QMessageBox
#图片执行脚本
class pictureScriptRecording():
    def pictureRunRecord(self,path,picturePath):
       QMessageBox.about(None, "提示!!!", "请2秒内放入执行位置开始执行脚本")
       self.mainwind.hide()
       time.sleep(2)
       with open(path, 'r') as f:
           self.content = csv.reader(f)
           for das in self.content:
               if das[2]=='scroll':
                   button7location = pyautogui.locateOnScreen(picturePath, confidence=0.6)
                   button7point = pyautogui.center(button7location)
                   pyautogui.moveTo(button7point[0], button7point[1])
                   self.pictureRunScroll(das,button7point[0], button7point[1])
               elif das[2]=='press':
                   button7location = pyautogui.locateOnScreen(picturePath, confidence=0.6)
                   button7point = pyautogui.center(button7location)
                   pyautogui.moveTo(button7point[0], button7point[1])
                   self.pictureRunPress(das)
               elif das[2] == 'release':
                   button7location = pyautogui.locateOnScreen(picturePath, confidence=0.6)
                   button7point = pyautogui.center(button7location)
                   pyautogui.moveTo(button7point[0], button7point[1])
                   self.pictureRunRelease(das)
               elif das[2] == 'click':
                   button7location = pyautogui.locateOnScreen(picturePath, confidence=0.6)
                   button7point = pyautogui.center(button7location)
                   pyautogui.moveTo(button7point[0], button7point[1])
                   self.pictureRunClick(das,button7point[0], button7point[1])
       self.mainwind.show()
       self.click.statusbar.clearMessage()
       self.click.statusbar.showMessage("执行脚本成功!!")

    def pictureRunScroll(self,das,xt,yt):
        pyautogui.FAILSAFE = False
        count = datetime.datetime.now().time().second
        sc=int(das[7])
        while True:
          pyautogui.scroll(sc*50,x=xt, y=yt)
          end = datetime.datetime.now().time().second
          if end-count >=int(das[8])/1000:
              break
    def pictureRunPress(self,das):
        pyautogui.keyDown(str(das[1]).replace("'",""))
    def pictureRunRelease(self,das):
        pyautogui.keyUp(str(das[1]).replace("'",""))
    def pictureRunClick(self,das,xt,yt):
        pyautogui.click(x=xt, y=yt, clicks=1, interval=0.0, button=str(das[1]).replace("Button.",""), duration=0.0, tween=pyautogui.linear)
