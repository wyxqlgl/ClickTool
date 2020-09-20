import configparser
import os
from threading import Thread
from StartRecord import startRecord
class scriptRecording(startRecord):
    def scriptRecord(self):
        self.mainwind.close()
        f= open('script.csv', 'w',encoding='utf-8',newline='')
        parent = os.path.dirname(os.path.realpath(__file__))
        self.saveConfigRecording(parent+ "/script.csv")
        self.click.lineEdit_9.setText(parent + "/script.csv")
        self.scriptReport()
    def scriptReport(self):
        self.mainwind.close()
        self.monitoring.show()
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





