import socket
import select
import threading
import Server
import time
from datetime import datetime
import sys
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QLabel, QApplication, QWidget, QDesktopWidget, QCheckBox, QMessageBox, QSlider, QPushButton



############################################
# GUI avec Sequenceur
############################################

class MainWin(QWidget):

    def __init__(self):
        #Init parent
        super().__init__()
        #Window configuration

        self.setFixedSize(1000, 500)
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

        #Sequenceur
        '''self.ticks = 200
        self.timer = QtCore.QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.recurring_timer)
        self.timer.start()'''

        #Start GUI configuration
        self.initUI()
        # Create Server1 object
        newServer1 = Server.Server('192.168.1.16', 50001, 1024)
        newServer1.start()
        # Create Server2 object
        newServer2 = Server.Server('192.168.1.16', 50002, 1024)
        newServer2.start()
        # Create Server3 object
        newServer3 = Server.Server('192.168.1.16', 50003, 1024)
        newServer3.start()
        # Create Server4 object
        newServer4 = Server.Server('192.168.1.16', 50004, 1024)
        newServer4.start()
        # Create Server5 object
        newServer5 = Server.Server('192.168.1.16', 50005, 1024)
        newServer5.start()


    def initUI(self):
        self.cb = QCheckBox('Auto Exposure', self)
        #self.cb.stateChanged.connect(self.changeAutoExposure)
        ##
        self.cb1 = QCheckBox('Auto Focus', self)
        #self.cb1.stateChanged.connect(self.changeAutoFocus)
        self.cb1.setGeometry(150, 0, 300, 25)
        ##
        self.button = QPushButton('Capture', self)
        self.button.setToolTip('Capture')
        self.button.setGeometry(300, 0, 100, 25)
        #self.button.clicked.connect(self.capture_demand)
        ##
        self.button1 = QPushButton('AutofocusCal', self)
        self.button1.setToolTip('Capture')
        self.button1.setGeometry(400, 0, 100, 25)
        #self.button1.clicked.connect(self.autofocus_calib_demand)
        ##
        self.sl = QSlider(Qt.Horizontal, self)
        self.sl.setFocusPolicy(Qt.StrongFocus)
        self.sl.setTickPosition(QSlider.TicksBothSides)
        self.sl.setTickInterval(25)
        self.sl.setSingleStep(1)
        self.sl.setGeometry(650, 0, 300, 25)
        self.sl.setMinimum(0)
        self.sl.setMaximum(854)
        # self.sl.setValue()
        #self.sl.valueChanged[int].connect(self.changeAbsoluteAutoFocus)
        ##
        self.label = QLabel(self)
        self.label.setScaledContents(True)
        self.label.move(0, 30)
        self.label.resize(self.geometry().width(), self.geometry().height())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWin()
    win.show()
    sys.exit(app.exec_())