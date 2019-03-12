
from ui1 import Ui_MainWindow

from PySide import QtCore, QtGui
from PySide.QtGui import *
from PySide.QtWebKit import *
from PySide.QtCore import *

import sys
import time
import threading
import random
import datetime
from ctypes import *
import win32api
import win32gui
import win32con
import json

class wow():
    def __init__(self, wd=None, gcd=0.8, sound_pos=None,trigger=None):
        if wd == None:
            self.wd = u'魔兽世界'
        else:
            self.wd = wd

        if sound_pos == None:
            self.sound_pos = (0,0)
        else:
            self.sound_pos = sound_pos

        self.hwnd = win32gui.FindWindow(None, self.wd)
        self.rect = win32gui.GetWindowRect(self.hwnd)
        a = win32gui.GetForegroundWindow()
        print(self.hwnd)
        print(a)
        self.cd_trim = 0.1
        self.gcd = gcd
        self.time1 = 0
        self.time2 = 0
        self.time3 = 0
        self.movekey_H = {'1': 65,  # A
                          '2': 68,  # D
                          '3': 68,  # D
                          '4': 65,  # A
                          }

        self.xpos = int(self.rect[2] / 2)
        self.ypos = int(self.rect[3] / 2)
        self.gdi32 = windll.gdi32
        self.user32 = windll.user32
        self.hdc = self.user32.GetDC(None)

        self.msg = trigger


    def sleep(self, x, s):
        if x < 0:
            x = 0
        stime = random.uniform(x, s)
        time.sleep(stime)
        self.time1 += stime
        self.time2 += stime
        self.time3 += stime
        return stime

    def press_key(self, key, cd=0):
        win32api.keybd_event(key, 0, 0, 0)
        win32api.keybd_event(key, 0, win32con.KEYEVENTF_KEYUP, 0)
        press_time = self.sleep(cd - self.cd_trim, cd + self.cd_trim)
        return press_time

    def press_keydown(self, key, cd):
        win32api.keybd_event(key, 0, 0, 0)
        self.sleep(cd, cd)
        win32api.keybd_event(key, 0, win32con.KEYEVENTF_KEYUP, 0)

    def press_random_click(self, ctime=20):
        for i in range(0, ctime):
            win32api.SetCursorPos((self.xpos + random.randint(-100, 100), self.ypos + random.randint(-50, -20)))
            win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0)
            self.sleep(0.05, 0.05)
            win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0)
            self.sleep(0.05, 0.05)

    def check_fished(self,sound_pos):
        fished = True
        c1 = ''
        c2 = ''
        i = 0

        win32api.SetCursorPos(sound_pos)  # 光标定位
        while fished == True:
            c2 = c1
            a = win32gui.GetCursorInfo()
            c1 = self.gdi32.GetPixel(self.hdc,a[2][0],a[2][1])
            i += 1
            if c1 != c2 and c2 != '':
                fished = False
            if i == 1000:
                fished = False

    def create_emit_json(self,num,text):
        c = {}
        c['num'] = str(num)
        c['text'] = str(text)
        json_str = json.dumps(c)
        return json_str

    def DY(self, pickup=False, move=False):
        self.sleep(5, 5)
        self.time1 = 1800
        self.time2 = 600
        self.time3 = 0
        start_time = datetime.datetime.now()
        self.msg.emit(self.create_emit_json(0,'开始吃巨型鱼鳔.'))
        self.press_key(50)
        self.sleep(6, 6)

        sg = 1

        while True:
            end_time = datetime.datetime.now()
            self.time1 = int((end_time - start_time).seconds)
            cw = win32gui.GetForegroundWindow()

            if cw != self.hwnd:
                print(cw,self.hwnd)
                self.sleep(5,5)
                continue

            if self.time1 > 1700:  # 1500秒 吃巨型鱼漂
                self.time1 = 0
                start_time = datetime.datetime.now()
                win32api.SetCursorPos((self.xpos, self.ypos))
                self.msg.emit(self.create_emit_json(0, '开始吃巨型鱼鳔.'))
                self.press_key(50)
                self.sleep(6, 6)

            #            if self.time2 > 550:  # 550 秒 吃珠子
            #                self.time2 = 0
            #                win32api.PostMessage(self.hwnd, win32con.WM_KEYDOWN, 51, 0)  # 发送3键
            #                win32api.PostMessage(self.hwnd, win32con.WM_KEYUP, 51, 0)
            #                self.sleep(6, 6)

            msg = '第' + str(sg) + '次甩杆...'
            self.msg.emit(self.create_emit_json(sg, msg))
            sg += 1

            self.press_key(49)
            self.sleep(2, 2)
            self.check_fished(self.sound_pos)
            self.sleep(0.5, 0.8)
            cw = win32gui.GetForegroundWindow()

            for i in range(1, 15):
                if cw == self.hwnd:
                    win32api.SetCursorPos(
                        (self.xpos + random.randint(-200, 200), self.ypos + random.randint(-150, -120)))  # 光标定位
                    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
                    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
                    self.sleep(0.2, 0.2)


class myMainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(myMainWindow, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.process_start1)
        self.ui.pushButton_2.clicked.connect(self.process_stop)
        self.pics = ['d1.jpeg','d2.jpg','d3.jpg','d4.jpg']
        self.image = QtGui.QImage(self.pics[0])
        self.ui.label.setPixmap(QtGui.QPixmap.fromImage(self.image))
        self.ui.label.adjustSize()
        self.ui.comboBox_2.addItem('钓鱼', 'DY')
        self.ui.horizontalSlider.setTickPosition(QtGui.QSlider.TicksBelow)
        self.ui.horizontalSlider.setMaximum(3)
        self.ui.horizontalSlider.valueChanged[int].connect(self.change_pic)

    def process_start1(self):
        self.thread = MyThread_l(self)  # 创建线程
        self.thread.trigger.connect(self.update_text)  # 连接信号！
        self.thread.start()  # 启动线程

    def process_stop(self):
        self.thread.terminate()
        self.thread.wait()

    def update_text(self, msg):
        msg = json.loads(msg)
        self.ui.textBrowser.append(msg['text'])
        self.ui.textBrowser.append('-------------------------')
        self.ui.textBrowser.showMaximized()
        self.ui.lcdNumber.display(int(msg['num']))
        self.change_pic(random.randint(0,3))

    def change_pic(self,value):
        self.image = QtGui.QImage(self.pics[value])
        self.ui.label.setPixmap(QtGui.QPixmap.fromImage(self.image))

class MyThread_l(QThread):
    trigger = Signal(str)  # trigger传输的内容是字符串

    def __init__(self, parent=None):
        super(MyThread_l, self).__init__(parent)

    def run(self):  # 很多时候都必重写run方法, 线程start后自动运行
        mywow = wow(trigger=self.trigger)
        mywow.DY()


myApp = QApplication(sys.argv)
myWindow = myMainWindow()
myWindow.show()
myApp.exec_()
sys.exit(0)
