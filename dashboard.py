# -*- coding: utf-8 -*-

import sys
import ctypes
import psutil
import threading
from time import sleep, time
from PyQt5.QtWidgets import QApplication, QWidget, QLabel,  QToolTip,  QMenu
from PyQt5.QtGui import QPalette, QColor, QFont, QCursor
from PyQt5.QtCore import Qt

class Dashboard_window(QWidget):
    def __init__(self):
        super().__init__()
        self.m_flag=False
        self.setWindowFlags(Qt.FramelessWindowHint|Qt.Tool|Qt.WindowStaysOnTopHint)
        palette1 = QPalette()
        palette1.setColor(self.backgroundRole(), QColor(0,0,0))   # 设置背景颜色
        self.setPalette(palette1)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.rightMenuShow)
        self.setWindowOpacity(0.85)
        self.setMouseTracking(True)
        self.resize(225,80)
        self.move(pos_x,pos_y)
        self.initUI()
        QToolTip.setFont(QFont('SansSerif', 10))
        self.show()
  
    def initUI(self):
        textcolot=QColor(255,255,255)
        margin=10
        width=100
        height=40
        global Battery_width
        Battery_width=6
        palette2 = QPalette()
        # 初始化
        label0=QLabel("",self)
        label1=QLabel("↑1000KB/s",self)
        label2=QLabel("↓1000KB/s",self)
        label3=QLabel(" CPU 99%",self)
        label4=QLabel("内存 99%",self)
        label5=QLabel("",self)
        # 修改字体
        label1.setFont(QFont("Roman times",10.5))
        label2.setFont(QFont("Roman times",10.5))
        label3.setFont(QFont("Roman times",10.5))
        label4.setFont(QFont("Roman times",10.5))
        # 对齐方式
        label1.setAlignment(Qt.AlignVCenter|Qt.AlignLeft)
        label2.setAlignment(Qt.AlignVCenter|Qt.AlignLeft)
        label3.setAlignment(Qt.AlignVCenter|Qt.AlignLeft)
        label4.setAlignment(Qt.AlignVCenter|Qt.AlignLeft)
        # 调整大小 横,纵
        label0.resize(Battery_width,80)
        label1.resize(width,height)
        label2.resize(width,height)
        label3.resize(width,height)
        label4.resize(width,height)
        label5.resize(Battery_width,80)
        # 调整位置 横,纵
        label0.move(0,0)
        label1.move(Battery_width+margin,0)
        label2.move(Battery_width+margin,height)
        label3.move(Battery_width+margin+width+margin,0)
        label4.move(Battery_width+margin+width+margin,height)
        label5.move(0,0)
        # 设置颜色
        palette2.setColor(QPalette.WindowText, textcolot)
        label1.setPalette(palette2)
        label2.setPalette(palette2)
        label3.setPalette(palette2)
        label4.setPalette(palette2)
        #开启监控
        t = threading.Thread(target=Dashboard_hook,args=(label0,label1,label2,label3,label4,label5))
        t.setDaemon(True)
        t.start()
        
    def mousePressEvent(self, event):
        if event.button()==Qt.LeftButton:
            self.m_flag=True
            self.m_Position=event.globalPos()-self.pos() #获取鼠标相对窗口的位置
            event.accept()
        else:
            self.m_flag=False
            
    def mouseMoveEvent(self, QMouseEvent):
        global h, focused
        #focused=True
        if Qt.LeftButton and self.m_flag:  
            self.move(QMouseEvent.globalPos()-self.m_Position)#更改窗口位置
            if self.x()>(QApplication.desktop().width()-265):
                self.setWindowOpacity(0.5)
                h=True
            else:
                self.setWindowOpacity(1)
                h=False
            QMouseEvent.accept()
            
    def enterEvent (self, event):
        global  focused
        focused=True
        
    def leaveEvent (self, event):
        global  focused
        focused=False
        
    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag=False
        global pos_x, pos_y
        pos_x=self.x()
        pos_y=self.y()
        if h:
            while self.x()<QApplication.desktop().width():
                self.move(self.x()+20,self.y())
                sleep(0.01)
            pos_x=QApplication.desktop().width()-265
            w.hide()
            r.show(self.y())
        with open('pos.conf', 'w') as f:
            f.write('{},{}'.format(pos_x, pos_y))

    def rightMenuShow(self):
        try:
            self.contextMenu = QMenu()
            self.actionA = self.contextMenu.addAction(u'退出')
            self.contextMenu.popup(QCursor.pos())  # 菜单显示的位置
            self.actionA.triggered.connect(sys.exit)
            self.contextMenu.show()
        except Exception as e:
            print(e)

class Indicator_windows(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint|Qt.Tool|Qt.WindowStaysOnTopHint)
        palette1 = QPalette()
        palette1.setColor(self.backgroundRole(), QColor(0,0,0))   # 设置背景颜色
        self.setMouseTracking(True)
        self.setPalette(palette1)
        self.resize(10,84)
        self.initUI()
    
    def initUI(self):
        label0=QLabel("",self)
        label0.resize(5,80)
        t = threading.Thread(target=Indicator_hook,args=(label0, ))
        t.setDaemon(True)
        t.start()
        
    def show(self,y):
        self.move(QApplication.desktop().width()-10,y)
        super().show()
        
    def mouseMoveEvent(self, QMouseEvent):
        r.hide()
        w.show()
        w.setWindowOpacity(1)
        while w.x()>pos_x:
            w.move(w.x()-20,pos_y)
            sleep(0.01)
            w.repaint()
        tm = threading.Thread(target=Rehide)
        tm.setDaemon(True)
        tm.start()
            
class SYSTEM_POWER_STATUS(ctypes.Structure):
    _fields_=[('ACLineStatus',ctypes.c_byte),
              ('BatteryFlag',ctypes.c_byte),
              ('BatteryLifePercent',ctypes.c_byte),
              ('Reserved1',ctypes.c_byte),
              ('BatteryLifeTime',ctypes.c_int),
              ('BatteryFullLifeTime',ctypes.c_int)
              ]

def Rehide():
    sleep(1)
    while focused:
        pass
    if h:
        while w.x()<QApplication.desktop().width():
            w.move(w.x()+20,w.y())
            sleep(0.01)
            w.repaint()
        w.hide()
        r.show(w.y())

def float_format(f, t):
    if f>99:
        if t=='b':
            return format(f, '.1f')
        return format(f, '.0f')
    elif f>9:
        return format(f, '.1f')
    else:
        return format(f, '.2f')

def Dashboard_hook(label0,label1,label2,label3,label4,label5):
    palette5 = QPalette()
    label5.setAutoFillBackground(True)
    dll = ctypes.CDLL("KERNEL32.dll")
    POWER_STATUS=SYSTEM_POWER_STATUS()
    while True:
        label3.setText('CPU {:.0f}%'.format(psutil.cpu_percent(None)))#cpu使用率
        label4.setText('内存 {:.0f}%'.format(psutil.virtual_memory().percent))#内存使用率
        byteSent1=psutil.net_io_counters().bytes_sent#发送总字节
        byteRecv1 =psutil.net_io_counters().bytes_recv#接收总字节
        t1=time()
        sleep(1)
        byteSent2=psutil.net_io_counters().bytes_sent
        byteRecv2 =psutil.net_io_counters().bytes_recv
        sent = (byteSent2-byteSent1)/(time()-t1)       # 上传字节数
        recv = (byteRecv2-byteRecv1)/(time()-t1)      # 下载字节数
        if sent > 1048576 :             # 字节数达到 m 级别时以 M 作为单位
            label1.setText("↑{}MB/s".format(float_format(sent / 1048576), 'mb'))
        elif sent > 1024:              # 字节数达到 k 级别时以 K 作为单位
            label1.setText("↑{}KB/s".format(float_format(sent / 1024, 'kb')))
        else:
            label1.setText("↑{}B/s".format(float_format(sent, 'b')))
        if recv > 1048576 :             # 字节数达到 m 级别时以 M 作为单位
            label2.setText("↓{}MB/s".format(float_format(recv / 1048576, 'mb')))
        elif recv > 1024:              # 字节数达到 k 级别时以 K 作为单位
            label2.setText("↓{}KB/s".format(float_format(recv / 1024, 'kb')))
        else:
            label2.setText("↓{}B/s".format(float_format(recv, 'b')))
        dll.GetSystemPowerStatus(ctypes.byref(POWER_STATUS))
        if not POWER_STATUS.BatteryFlag==255:    #电池充电状态 1：>66%；0：<66% >33%；2：<33%；4：<5%；8：充电；128：没有电池；225：未知状态 - 无法读取电池标志信息
            Battery_charge_time=POWER_STATUS.BatteryFullLifeTime    #完全充电时电池寿命的秒数，如果电池寿命未知或设备已连接到交流电源，则为-1
            Battery_percent=POWER_STATUS.BatteryLifePercent    #剩余电量的百分比；未知255
            Battery_availability_time=POWER_STATUS.BatteryLifeTime    #剩余电池寿命的秒数，如果剩余秒数未知或设备已连接到交流电源，则为-1
            if Battery_percent>60:
                palette5.setColor(QPalette.Background, QColor(0,255,0))
            elif Battery_percent<20:
                palette5.setColor(QPalette.Background, QColor(255,0,0))
            else:
                palette5.setColor(QPalette.Background, QColor(255,140,0))
            label5.setPalette(palette5)
            label5.move(0, 80-int(0.8*Battery_percent))
            label5.resize(Battery_width,int(0.8*Battery_percent))
            if POWER_STATUS.ACLineStatus==1:#交流电源状态 0：未连接；1：已连接；255：未知状态
                if POWER_STATUS.BatteryFlag==8:
                    label0.setToolTip("电池电量：{0}%\n距充满还需{1}小时{2}分钟".format(Battery_percent,Battery_charge_time//3600, Battery_charge_time//60 - Battery_charge_time//3600*60 ))
                    label5.setToolTip("电池电量：{0}%\n距充满还需{1}小时{2}分钟".format(Battery_percent,Battery_charge_time//3600, Battery_charge_time//60 - Battery_charge_time//3600*60))
                else:
                    label0.setToolTip("电池电量：{0}%\n已连接电源，未充电".format(Battery_percent,Battery_charge_time//3600, Battery_charge_time//60 - Battery_charge_time//3600*60 ))
                    label5.setToolTip("电池电量：{0}%\n已连接电源，未充电".format(Battery_percent,Battery_charge_time//3600, Battery_charge_time//60 - Battery_charge_time//3600*60 ))
            else:
                if POWER_STATUS.BatteryLifeTime==-1:
                    label0.setToolTip("电池剩余：{0}%".format(Battery_percent))
                    label5.setToolTip("电池剩余：{0}%".format(Battery_percent))
                else:
                    label0.setToolTip("电池剩余：{0}%\n可用{1}小时{2}分钟".format(Battery_percent,Battery_availability_time//3600, Battery_availability_time//60 - Battery_availability_time//3600*60 ))
                    label5.setToolTip("电池剩余：{0}%\n可用{1}小时{2}分钟".format(Battery_percent,Battery_availability_time//3600, Battery_availability_time//60 - Battery_availability_time//3600*60 ))

def Indicator_hook(label0):
    label0.setAutoFillBackground(True)
    while True:
        palette = QPalette()
        memory_percent=psutil.virtual_memory().percent
        if memory_percent>80:
            palette.setColor(QPalette.Background, QColor(255,0,0))
        elif memory_percent>60:
            palette.setColor(QPalette.Background, QColor(255,140,0))
        else:
            palette.setColor(QPalette.Background, QColor(0,255,0))
        label0.move(2, 82-int(memory_percent*0.8))
        label0.resize(5,int(memory_percent*0.8))
        label0.setPalette(palette)
        sleep(1)

if __name__ == '__main__':
    with open('pos.conf', 'r') as f:
        pos=eval(f.readline())
    pos_x=pos[0]
    pos_y=pos[1]
    h=False
    app = QApplication(sys.argv)
    w=Dashboard_window()
    r=Indicator_windows()
    sys.exit(app.exec_())
    
    
