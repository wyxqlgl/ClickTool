import configparser
import datetime
import os
import time
from ctypes import windll, byref
from ctypes.wintypes import POINT
import pyautogui
from PyQt5.QtWidgets import  QFileDialog, QMessageBox

import json
class MouthKeyMethod():
    def clickMothed(self):
        if self.click.checkBox_5.isChecked():
            self.saveConfig()
        if self.click.checkBox.isChecked(): #右键
            self.clickRightMouse(self.click.lineEdit.text(),self.click.lineEdit_7.text())
        if self.click.checkBox_2.isChecked(): #左键
            self.clickLeftMouse(self.click.lineEdit.text(),self.click.lineEdit_8.text())
        if self.click.checkBox_3.isChecked(): #滑轮
            self.pulley()
        if self.click.checkBox_4.isChecked():#键盘
            self.getContent(self.click.lineEdit_10.text())

    def saveConfig(self):
        config = configparser.ConfigParser()
        if self.click.checkBox_5.isChecked():
            config["DEFAULT"] = {
                "leftMouse": self.click.lineEdit_3.text(),
                "leftMouseTime":self.click.lineEdit_8.text(),
                "leftMouseRember":self.click.checkBox_2.isChecked(),
                "rightMouse": self.click.lineEdit.text(),
                "rightMouseTime":self.click.lineEdit_7.text(),
                "rightMouseRember": self.click.checkBox.isChecked(),
                "wheels": self.click.timeEdit.text(),
                "wheelsDirection":self.click.comboBox.currentText(),
                "wheelsRember": self.click.checkBox_3.isChecked(),
                "keyboard": self.click.lineEdit_4.text(),
                "keyboardTime":self.click.lineEdit_10.text(),
                "keyboardUrl": self.click.lineEdit_5.text(),
                "keyboardRember": self.click.checkBox_4.isChecked(),
                "remberAll":True,
                "coordinate1":self.click.lineEdit_2.text(),
                "coordinate2": self.click.lineEdit_6.text(),
                "scriptPaths": self.click.lineEdit_9.text()

            }
        else:
            config["DEFAULT"] = {
                "leftMouse": "",
                "leftMouseTime": "",
                "leftMouseRember": False,
                "rightMouse": "",
                "rightMouseTime": "",
                "rightMouseRember": False,
                "wheels": "",
                "wheelsDirection":"",
                "wheelsRember": False,
                "keyboard": "",
                "keyboardTime": "",
                "keyboardUrl": "",
                "keyboardRember": False,
                "remberAll":False,
                "coordinate":"",
                "coordinate2":"",
                "scriptPaths": ""
            }
        with open('user.ini', 'w')as configfile:
            config.write((configfile))
    def load_config(self):
        config = configparser.ConfigParser()
        file = config.read('user.ini')
        if file:
            config_dict = config.defaults()
            if len(config_dict) != 0:
                try :
                    leftMouse = config_dict['leftmouse']
                    self.click.lineEdit_3.setText(leftMouse)
                    if config_dict['leftmouserember'] == 'True':
                        self.click.checkBox_2.setChecked(True)
                    else:
                        self.click.checkBox_2.setChecked(False)
                    rightMouse = config_dict['rightmouse']
                    self.click.lineEdit.setText(rightMouse)
                    if config_dict['rightmouserember'] == 'True':
                        self.click.checkBox.setChecked(True)
                    else:
                        self.click.checkBox.setChecked(False)
                    wheels = config_dict['wheels']
                    wheelsTime= datetime.datetime.strptime("2000-01-01 "+wheels, '%Y-%m-%d %H:%M:%S').time()
                    self.click.timeEdit.setTime(wheelsTime)

                    if config_dict['wheelsdirection']=='向上':
                        self.click.comboBox.setCurrentIndex(1)
                    elif config_dict['wheelsdirection']=='向下':
                        self.click.comboBox.setCurrentIndex(1)
                    else:
                        self.click.comboBox.setCurrentIndex(0)
                    if config_dict['wheelsrember'] == 'True':
                        self.click.checkBox_3.setChecked(True)
                    else:
                        self.click.checkBox_3.setChecked(False)
                    keyboard = config_dict['keyboard']
                    self.click.lineEdit_4.setText(keyboard)
                    keyboardUrl = config_dict['keyboardurl']
                    self.click.lineEdit_5.setText(keyboardUrl)
                    if config_dict['keyboardrember'] == 'True':
                        self.click.checkBox_4.setChecked(True)
                    else:
                        self.click.checkBox_4.setChecked(False)
                    if config_dict['remberall'] == 'True':
                        self.click.checkBox_5.setChecked(True)
                    else:
                        self.click.checkBox_5.setChecked(False)
                    if self.contends == "" and self.click.lineEdit_5.text() != "":
                        self.get_contends()
                    coordinate1 = config_dict['coordinate1']
                    self.click.lineEdit_2.setText(coordinate1)
                    coordinate2 = config_dict['coordinate2']
                    self.click.lineEdit_6.setText(coordinate2)
                    leftMouseTime = config_dict['leftmousetime']
                    rightMouseTime = config_dict['rightmousetime']
                    keyboardTime = config_dict['keyboardtime']
                    self.click.lineEdit_7.setText(rightMouseTime)
                    self.click.lineEdit_8.setText(leftMouseTime)
                    self.click.lineEdit_10.setText(keyboardTime)

                except Exception as e:
                    config["DEFAULT"] = {
                        "leftMouse": "",
                        "leftMouseTime": "",
                        "leftMouseRember": False,
                        "rightMouse": "",
                        "rightMouseTime": "",
                        "rightMouseRember": False,
                        "wheels": "",
                        "wheelsDirection": "",
                        "wheelsRember": False,
                        "keyboard": "",
                        "keyboardTime": "",
                        "keyboardUrl": "",
                        "keyboardRember": False,
                        "remberAll": False,
                        "coordinate": "",
                        "coordinate2": ""
                    }
            try:
                scriptpaths = config.get("SCRIPTDEFAULT","scriptpaths")
                if os.path.exists(scriptpaths):
                  self.click.lineEdit_9.setText(scriptpaths)
                else:
                  self.click.lineEdit_9.setText("")
            except Exception as e:
                config["SCRIPTDEFAULT"] = {"scriptpaths":""}
                with open('user.ini', 'w')as configfile:
                   config.write((configfile))
        else:
            t=open('user.ini', 'w')
    def get_contends(self):
        with open(self.click.lineEdit_5.text(), 'r', encoding='utf-8') as file_object:
            self.contends = file_object.read()
    def getFile(self):
            fileName, filetype = QFileDialog.getOpenFileNames(None, "请选择要发送的文件",
                                                              "c:/",
                                                              "Text Files (*.txt)")
            self.path=str(fileName[0])
            self.click.lineEdit_5.setText(self.path)
            self.get_contends()
    def getCoordinate(self,whos):
        pyautogui.FAILSAFE = False
        try:
            QMessageBox.about(None, "提示!!!", "放到鼠标点击位置2秒钟")
            self.mainwind.hide()
            time.sleep(2)
            po = POINT()
            windll.user32.GetCursorPos(byref(po))
            if whos==1:
                self.y1=int(po.y)
                self.x1 = int(po.x)
                self.click.lineEdit_2.setText(str(self.x1)+":"+str(self.y1))
            elif whos==2:
                self.y2 = int(po.y)
                self.x2 = int(po.x)
                self.click.lineEdit_6.setText(str(self.x2) + ":" + str(self.y2))
        except KeyboardInterrupt as e:
            print('有异常请确定'+e)
        self.mainwind.show()
    def clickRightMouse(self,count,times):
        pyautogui.FAILSAFE = False
        if self.click.lineEdit_2.text() is None or self.click.lineEdit_2.text() == "":
            QMessageBox.critical(None, "警告!!!", "先选择右键鼠标位置");
            return;
        if times is None or times == "":
            QMessageBox.critical(None, "警告!!!", "先选择右键鼠标延迟时间")
            return;
        if int(times) < 0:
            QMessageBox.critical(None, "警告!!!", "延迟时间大于零")
            return;
        x,y= self.click.lineEdit_2.text().split(":")
        time.sleep(int(times))
        pyautogui.moveTo(int(x), int(y))
        a=int(count)
        self.mainwind.hide()
        for ast in range(0,a):
            time.sleep(int(times))
            pyautogui.rightClick()
        self.mainwind.show()
        self.showMassage("点击鼠标右键执行成功!")
    def clickLeftMouse(self, count,times):
        pyautogui.FAILSAFE = False
        if (self.click.lineEdit_6.text() is None or self.click.lineEdit_6.text()==""):
            QMessageBox.critical(None, "警告!!!", "先选择左键鼠标位置")
            return;
        if times is None or times=="":
            QMessageBox.critical(None, "警告!!!", "先选择左键鼠标延迟时间")
            return;
        if int(times)<0:
            QMessageBox.critical(None, "警告!!!", "延迟时间大于零")
            return;
        self.mainwind.hide()
        x, y = self.click.lineEdit_6.text().split(":")
        time.sleep(int(times))
        pyautogui.moveTo(int(x), int(y))
        a = int(count)
        for ast in range(0, a):
            time.sleep(int(times))
            pyautogui.leftClick()
        self.mainwind.show()
        self.showMassage("点击鼠标左键执行成功!")
    def pulley(self):
        pyautogui.FAILSAFE = False
        wheelsTime = datetime.datetime.strptime("2000-01-01 " + self.click.timeEdit.text(), '%Y-%m-%d %H:%M:%S').time().second
        begin =  datetime.datetime.now().time().second
        QMessageBox.about(None, "提示!!!", "放到滚轮运行的地方");
        time.sleep(2)
        self.mainwind.hide()
        if self.click.comboBox.currentText() =="向下":
            while True:
                time.sleep(0.1)
                pyautogui.scroll(-10)
                end = datetime.datetime.now().time().second
                if end - begin-wheelsTime>=0:
                     break;
        elif self.click.comboBox.currentText() =="向上":
            while True:
                time.sleep(0.1)
                pyautogui.scroll(10)
                end = datetime.datetime.now().time().second
                if end-begin-wheelsTime >= 0:
                     break;

        else:
            return;
        self.mainwind.show()
        self.showMassage("滚轮执行成功!")
    def getContent(self,times):
        pyautogui.FAILSAFE = False
        if self.click.lineEdit_4.text()=="" or self.click.lineEdit_4.text() is None:
          QMessageBox.critical(None, "警告!!!", "先填按键盘次数")
          return;
        if times is None or times == "":
            QMessageBox.critical(None, "警告!!!", "先选择按键盘延迟时间")
            return;
        if int(times) < 0:
            QMessageBox.critical(None, "警告!!!", "延迟时间大于零")
            return;
        QMessageBox.about(None, "提示!!!", "放到键盘运行的地方");
        self.mainwind.hide()
        time.sleep(2)
        time.sleep(int(times))
        json_str = json.dumps(self.contends,indent=4)
        user_dic = json.loads(json_str)
        data = eval(user_dic)
        key=data["data"]
        count=int(self.click.lineEdit_4.text())
        for es in range(0,count):
            for et in key:
                if et.find("+") >= 0:
                    ents=str(et).split("+")
                    if len(ents)==2:
                        pyautogui.hotkey(ents[0],ents[1])
                    elif len(ents)==3:
                        pyautogui.hotkey(ents[0], ents[1],ents[2])
                    elif len(ents) == 4:
                        pyautogui.hotkey(ents[0], ents[1], ents[2], ents[3])
                    elif len(ents) == 5:
                        pyautogui.hotkey(ents[0], ents[1], ents[2], ents[3], ents[4])
                    else:
                        QMessageBox.critical(None, "警告!!!", "本系统暂支持5键同时按")
                else:
                    pyautogui.press(et)
                time.sleep(int(times))
        self.mainwind.show()
        self.showMassage("键盘按钮运行成功!")
    def showMassage(self,content):
        self.click.statusbar.clearMessage()
        self.click.statusbar.showMessage(content)





