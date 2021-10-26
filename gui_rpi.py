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
from PyQt5.QtWidgets import QLabel, QApplication, QWidget, QDesktopWidget, QCheckBox, QMessageBox, QSlider, QPushButton, QInputDialog, QLineEdit, QComboBox

############################################
# GUI
############################################

class MainWin(QWidget):

    def __init__(self):
        #Init parent
        super().__init__()

        #Window configuration
        self.setFixedSize(1280, 720)
        self.setWindowTitle("Cosmo Guirlandes RPi GUI")
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

        #Start GUI configuration
        self.initUI()


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
        self.button_port.setGeometry(60, 60, 50, 20)
        # connect button to function on_click
        self.button_port.clicked.connect(self.on_click_port)

        #Couleur 1
        self.type_color11 = QComboBox(self)
        self.type_color11.setGeometry(10, 110, 100, 20)
        self.type_color11.addItems(["AMBER","AQUA","BLACK","BLUE", "CYAN","GOLD","GREEN","JADE","MAGENTA","OLD_LACE"
                                       ,"ORANGE", "PINK","PURPLE","RAINBOW","RED",
                                    "RGBW_WHITE_RGB" ,"RGBW_WHITE_RGBW","RGBW_WHITE_W", "TEAL", "WHITE","YELLOW" ])
        self.type_color11.currentIndexChanged.connect(self.color1_change_demand1)

    def on_click_ip(self):
        IPValue = self.textbox_IP.text()

    def on_click_port(self):
        PortValue = self.textbox_port.text()

    def color1_change_demand1(self):
        print("selection changed ", self.type_color11.currentText())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWin()
    win.show()
    sys.exit(app.exec_())