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
from PyQt5.QtWidgets import QLabel, QApplication, QWidget, QDesktopWidget, QCheckBox, QMessageBox, QSlider, QPushButton, QInputDialog, QLineEdit



############################################
# GUI avec Sequenceur
############################################

class MainWin(QWidget):

    def __init__(self):
        #Init parent
        super().__init__()
        #Window configuration

        self.setFixedSize(1900, 920)
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

        #Entree adresse IP
        # Create textbox
        self.textbox_IP = QLineEdit(self)
        self.textbox_IP.setGeometry(10, 10, 50, 20)
        # Create a button in the window
        self.button_IP= QPushButton('IP', self)
        self.button_IP.setGeometry(60, 10, 50, 20)
        # connect button to function on_click
        self.button_IP.clicked.connect(self.on_click_ip)

        #Entree Port
        # Create textbox
        self.textbox_port = QLineEdit(self)
        self.textbox_port.setGeometry(10, 60, 50, 20)
        # Create a button in the window
        self.button_port = QPushButton('Port', self)
        self.button_port.setGeometry(60, 50, 50, 20)
        # connect button to function on_click
        self.button_port.clicked.connect(self.on_click_port)

        #Checkbox de synchronisation
        self.cb_sync = QCheckBox('Sync Commands', self)
        self.cb_sync.setToolTip('Click if you wanna sync colors / effects')
        #self.cb_sync.stateChanged.connect(self.changeAutoExposure)
        self.cb_sync.setGeometry(10, 420, 300, 25)

        #Checkbox Stromboscope
        self.cb_strombo_1 = QCheckBox('Strombo_1', self)
        self.cb_strombo_1.setToolTip('Click if you wannause strombo effect')
        #self.cb_strombo_1.stateChanged.connect(self.changeAutoFocus)
        self.cb_strombo_1.setGeometry(10, 450, 300, 25)

        #Entree Frequence Strombo
        # Create textbox
        self.textbox_strombo = QLineEdit(self)
        self.textbox_strombo.setGeometry(100, 450, 50, 20)
        # Create a button in the window
        self.button_strombo= QPushButton('Strombo Frequency', self)
        self.button_strombo.setGeometry(150, 450, 100, 20)
        # connect button to function on_click
        self.button_strombo.clicked.connect(self.on_click_strombo_frequency)

        #Bouton effet rainbow 1 Loop
        self.button_rainbow_1 = QPushButton('Rainbow effect', self)
        self.button_rainbow_1.setToolTip('Click if you wanna use rainbow effect')
        self.button_rainbow_1.setGeometry(10, 480, 100, 25)
        #self.button_rainbow_1.clicked.connect(self.capture_demand)

        #Bouton Blackout
        self.button_blackout_1 = QPushButton('Blackout', self)
        self.button_blackout_1.setToolTip('Turn off LEDs')
        self.button_blackout_1.setGeometry(10, 510, 100, 25)
        #self.button_blackout_1.clicked.connect(self.autofocus_calib_demand)

        # Slider Red 1
        self.sl_R1 = QSlider(Qt.Vertical, self)
        self.sl_R1.setFocusPolicy(Qt.StrongFocus)
        self.sl_R1.setTickPosition(QSlider.TicksBothSides)
        self.sl_R1.setTickInterval(25)
        self.sl_R1.setSingleStep(1)
        self.sl_R1.setGeometry(10, 200, 20, 200)
        self.sl_R1.setMinimum(0)
        self.sl_R1.setMaximum(255)

        # Slider Green 1
        self.sl_G1 = QSlider(Qt.Vertical, self)
        self.sl_G1.setFocusPolicy(Qt.StrongFocus)
        self.sl_G1.setTickPosition(QSlider.TicksBothSides)
        self.sl_G1.setTickInterval(25)
        self.sl_G1.setSingleStep(1)
        self.sl_G1.setGeometry(60, 200, 20, 200)
        self.sl_G1.setMinimum(0)
        self.sl_G1.setMaximum(255)

        # Slider Blue 1
        self.sl_B1 = QSlider(Qt.Vertical, self)
        self.sl_B1.setFocusPolicy(Qt.StrongFocus)
        self.sl_B1.setTickPosition(QSlider.TicksBothSides)
        self.sl_B1.setTickInterval(25)
        self.sl_B1.setSingleStep(1)
        self.sl_B1.setGeometry(110, 200, 20, 200)
        self.sl_B1.setMinimum(0)
        self.sl_B1.setMaximum(255)
        # self.sl.setValue()
        #self.sl.valueChanged[int].connect(self.changeAbsoluteAutoFocus)

        # Slider WHite 1
        self.sl_W1 = QSlider(Qt.Vertical, self)
        self.sl_W1.setFocusPolicy(Qt.StrongFocus)
        self.sl_W1.setTickPosition(QSlider.TicksBothSides)
        self.sl_W1.setTickInterval(25)
        self.sl_W1.setSingleStep(1)
        self.sl_W1.setGeometry(160, 200, 20, 200)
        self.sl_W1.setMinimum(0)
        self.sl_W1.setMaximum(255)
        # self.sl.setValue()
        #self.sl.valueChanged[int].connect(self.changeAbsoluteAutoFocus)
        ##
        self.label = QLabel(self)
        self.label.setScaledContents(True)
        self.label.move(0, 30)
        self.label.resize(self.geometry().width(), self.geometry().height())

        # Buttons functions
        #def slider_R1():
        #def slider_G1():
        #def slider_B1():
        #def slider_W1():

    @pyqtSlot()
    def on_click_ip(self):
        IPValue = self.textbox_IP.text()
        QMessageBox.question(self, 'Message - pythonspot.com', "You typed: " + IPValue, QMessageBox.Ok, QMessageBox.Ok)
        self.textbox.setText("")

    @pyqtSlot()
    def on_click_port(self):
        PortValue = self.textbox_port.text()
        QMessageBox.question(self, 'Message - pythonspot.com', "You typed: " + PortValue, QMessageBox.Ok,
                             QMessageBox.Ok)
        self.textbox.setText("")

    @pyqtSlot()
    def on_click_strombo_frequency(self):
        Strombo_frequency = self.textbox_port.text()
        QMessageBox.question(self, 'Message - pythonspot.com', "You typed: " + Strombo_frequency, QMessageBox.Ok,
                             QMessageBox.Ok)
        self.textbox.setText("")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWin()
    win.show()
    sys.exit(app.exec_())