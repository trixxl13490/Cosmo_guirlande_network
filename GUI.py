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
# GUI
############################################

class MainWin(QWidget):

    # Create Server1 object
    newServer1 = Server.Server('192.168.0.16', 50001, 1024)
    newServer1.start()
    # Create Server2 object
    newServer2 = Server.Server('192.168.0.16', 50002, 1024)
    newServer2.start()
    # Create Server3 object
    newServer3 = Server.Server('192.168.0.16', 50003, 1024)
    newServer3.start()
    # Create Server4 object
    newServer4 = Server.Server('192.168.0.16', 50004, 1024)
    newServer4.start()
    # Create Server5 object
    newServer5 = Server.Server('192.168.0.16', 50005, 1024)
    newServer5.start()
    #Sync Thread
    timer = QtCore.QTimer()
    timer.setInterval(100)
    timer.start()

    #Create message to communicate with sensors
    msg1 = ''
    msg2 = ''
    msg3 = ''
    msg4 = ''
    msg5 = ''

    def __init__(self):
        #Init parent
        super().__init__()

        #Window configuration
        self.setFixedSize(1900, 920)
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

        #Start GUI configuration
        self.initUI()


    def initUI(self):
        #########################################################################################################Strip 1
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

        #Entree Frequence Strombo
        # Create textbox
        self.textbox_strombo = QLineEdit(self)
        self.textbox_strombo.setGeometry(100, 450, 50, 20)
        # Create a button in the window
        self.button_strombo= QPushButton('Strombo Frequency', self)
        self.button_strombo.setGeometry(150, 450, 100, 20)
        # connect button to function on_click
        self.button_strombo.clicked.connect(self.on_click_strombo_frequency)


        #Checkbox de synchronisation
        self.cb_sync = QCheckBox('Sync Commands', self)
        self.cb_sync.setToolTip('Click if you wanna sync colors / effects')
        self.cb_sync.stateChanged.connect(self.sync_demand)
        self.cb_sync.setGeometry(10, 420, 300, 25)


        #Checkbox Stromboscope
        self.cb_strombo_1 = QCheckBox('Strombo_1', self)
        self.cb_strombo_1.setToolTip('Click if you wanna use strombo effect')
        self.cb_strombo_1.stateChanged.connect(self.strombo_demand)
        self.cb_strombo_1.setGeometry(10, 450, 300, 25)


        #Bouton effet rainbow 1 Loop
        self.button_rainbow_1 = QPushButton('Rainbow effect', self)
        self.button_rainbow_1.setToolTip('Click if you wanna use rainbow effect')
        self.button_rainbow_1.setGeometry(10, 480, 100, 25)
        self.button_rainbow_1.clicked.connect(self.rainbow_demand)


        #Bouton Blackout 1
        self.button_blackout_1 = QPushButton('Blackout', self)
        self.button_blackout_1.setToolTip('Turn off LEDs')
        self.button_blackout_1.setGeometry(10, 510, 100, 25)
        self.button_blackout_1.clicked.connect(self.blackout_demand)

        # Bouton theaterChase 1
        self.button_theaterChase_1 = QPushButton('theaterChase', self)
        self.button_theaterChase_1.setToolTip('theaterChase')
        self.button_theaterChase_1.setGeometry(10, 540, 100, 25)
        self.button_theaterChase_1.clicked.connect(self.theaterChase_demand_1)

        # Bouton theaterChaseRainbow 1
        self.button_theaterChaseRainbow_1 = QPushButton('theaterChaseRainbow', self)
        self.button_theaterChaseRainbow_1.setToolTip('theaterChaseRainbow')
        self.button_theaterChaseRainbow_1.setGeometry(10, 570, 100, 25)
        self.button_theaterChaseRainbow_1.clicked.connect(self.theaterChaseRainbow_demand_1)

        # Bouton multiColorWipe 1
        self.button_multiColorWipe_1 = QPushButton('multiColorWipe', self)
        self.button_multiColorWipe_1.setToolTip('multiColorWipe')
        self.button_multiColorWipe_1.setGeometry(10, 600, 100, 25)
        self.button_multiColorWipe_1.clicked.connect(self.multiColorWipe_demand_1)

        # Slider Red 1
        self.sl_R1 = QSlider(Qt.Vertical, self)
        self.sl_R1.setFocusPolicy(Qt.StrongFocus)
        self.sl_R1.setTickPosition(QSlider.TicksLeft)
        self.sl_R1.setTickInterval(1)
        self.sl_R1.setSingleStep(1)
        self.sl_R1.setGeometry(10, 200, 20, 200)
        self.sl_R1.setMinimum(0)
        self.sl_R1.setMaximum(255)
        self.sl_R1.valueChanged[int].connect(self.slider_R1)


        # Slider Green 1
        self.sl_G1 = QSlider(Qt.Vertical, self)
        self.sl_G1.setFocusPolicy(Qt.StrongFocus)
        self.sl_G1.setTickPosition(QSlider.TicksLeft)
        self.sl_G1.setTickInterval(1)
        self.sl_G1.setSingleStep(1)
        self.sl_G1.setGeometry(60, 200, 20, 200)
        self.sl_G1.setMinimum(0)
        self.sl_G1.setMaximum(255)
        self.sl_G1.valueChanged[int].connect(self.slider_G1)


        # Slider Blue 1
        self.sl_B1 = QSlider(Qt.Vertical, self)
        self.sl_B1.setFocusPolicy(Qt.StrongFocus)
        self.sl_B1.setTickPosition(QSlider.TicksLeft)
        self.sl_B1.setTickInterval(1)
        self.sl_B1.setSingleStep(1)
        self.sl_B1.setGeometry(110, 200, 20, 200)
        self.sl_B1.setMinimum(0)
        self.sl_B1.setMaximum(255)
        self.sl_B1.valueChanged[int].connect(self.slider_B1)


        # Slider White 1
        self.sl_W1 = QSlider(Qt.Vertical, self)
        self.sl_W1.setFocusPolicy(Qt.StrongFocus)
        self.sl_W1.setTickPosition(QSlider.TicksLeft)
        self.sl_W1.setTickInterval(1)
        self.sl_W1.setSingleStep(1)
        self.sl_W1.setGeometry(160, 200, 20, 200)
        self.sl_W1.setMinimum(0)
        self.sl_W1.setMaximum(255)
        self.sl_W1.valueChanged[int].connect(self.slider_W1)
        #########################################################################################################Strip 2
        #Entree Frequence Strombo 2
        # Create textbox
        self.textbox_strombo_2 = QLineEdit(self)
        self.textbox_strombo_2.setGeometry(400, 450, 50, 20)
        # Create a button in the window
        self.button_strombo_2= QPushButton('Strombo Frequency', self)
        self.button_strombo_2.setGeometry(450, 450, 100, 20)
        # connect button to function on_click
        self.button_strombo_2.clicked.connect(self.on_click_strombo_2_frequency)

        #Checkbox Stromboscope 2
        self.cb_strombo_2 = QCheckBox('Strombo_2', self)
        self.cb_strombo_2.setToolTip('Click if you wanna use strombo effect')
        self.cb_strombo_2.stateChanged.connect(self.strombo_demand_2)
        self.cb_strombo_2.setGeometry(310, 450, 300, 25)


        #Bouton effet rainbow 2 Loop
        self.button_rainbow_2 = QPushButton('Rainbow effect', self)
        self.button_rainbow_2.setToolTip('Click if you wanna use rainbow effect')
        self.button_rainbow_2.setGeometry(310, 480, 100, 25)
        self.button_rainbow_2.clicked.connect(self.rainbow_demand_2)


        #Bouton Blackout 2
        self.button_blackout_2 = QPushButton('Blackout', self)
        self.button_blackout_2.setToolTip('Turn off LEDs')
        self.button_blackout_2.setGeometry(310, 510, 100, 25)
        self.button_blackout_2.clicked.connect(self.blackout_demand_2)

        #Bouton theaterChase 2
        self.button_theaterChase_2 = QPushButton('theaterChase', self)
        self.button_theaterChase_2.setToolTip('theaterChase')
        self.button_theaterChase_2.setGeometry(310, 540, 100, 25)
        self.button_theaterChase_2.clicked.connect(self.theaterChase_demand_2)

        #Bouton theaterChaseRainbow 2
        self.button_theaterChaseRainbow_2 = QPushButton('theaterChaseRainbow', self)
        self.button_theaterChaseRainbow_2.setToolTip('theaterChaseRainbow')
        self.button_theaterChaseRainbow_2.setGeometry(310, 570, 100, 25)
        self.button_theaterChaseRainbow_2.clicked.connect(self.theaterChaseRainbow_demand_2)

        #Bouton multiColorWipe 2
        self.button_multiColorWipe_2 = QPushButton('multiColorWipe', self)
        self.button_multiColorWipe_2.setToolTip('multiColorWipe')
        self.button_multiColorWipe_2.setGeometry(310, 600, 100, 25)
        self.button_multiColorWipe_2.clicked.connect(self.multiColorWipe_demand_2)


        # Slider Red 2
        self.sl_R2 = QSlider(Qt.Vertical, self)
        self.sl_R2.setFocusPolicy(Qt.StrongFocus)
        self.sl_R2.setTickPosition(QSlider.TicksLeft)
        self.sl_R2.setTickInterval(1)
        self.sl_R2.setSingleStep(1)
        self.sl_R2.setGeometry(310, 200, 20, 200)
        self.sl_R2.setMinimum(0)
        self.sl_R2.setMaximum(255)
        self.sl_R2.valueChanged[int].connect(self.slider_R2)


        # Slider Green 2
        self.sl_G2 = QSlider(Qt.Vertical, self)
        self.sl_G2.setFocusPolicy(Qt.StrongFocus)
        self.sl_G2.setTickPosition(QSlider.TicksLeft)
        self.sl_G2.setTickInterval(1)
        self.sl_G2.setSingleStep(1)
        self.sl_G2.setGeometry(360, 200, 20, 200)
        self.sl_G2.setMinimum(0)
        self.sl_G2.setMaximum(255)
        self.sl_G2.valueChanged[int].connect(self.slider_G2)


        # Slider Blue 2
        self.sl_B2 = QSlider(Qt.Vertical, self)
        self.sl_B2.setFocusPolicy(Qt.StrongFocus)
        self.sl_B2.setTickPosition(QSlider.TicksLeft)
        self.sl_B2.setTickInterval(1)
        self.sl_B2.setSingleStep(1)
        self.sl_B2.setGeometry(410, 200, 20, 200)
        self.sl_B2.setMinimum(0)
        self.sl_B2.setMaximum(255)
        self.sl_B2.valueChanged[int].connect(self.slider_B2)


        # Slider White 2
        self.sl_W2 = QSlider(Qt.Vertical, self)
        self.sl_W2.setFocusPolicy(Qt.StrongFocus)
        self.sl_W2.setTickPosition(QSlider.TicksLeft)
        self.sl_W2.setTickInterval(1)
        self.sl_W2.setSingleStep(1)
        self.sl_W2.setGeometry(460, 200, 20, 200)
        self.sl_W2.setMinimum(0)
        self.sl_W2.setMaximum(255)
        self.sl_W2.valueChanged[int].connect(self.slider_W2)


        #########################################################################################################Strip 3
        #Entree Frequence Strombo 3
        # Create textbox
        self.textbox_strombo_3 = QLineEdit(self)
        self.textbox_strombo_3.setGeometry(700, 450, 50, 20)
        # Create a button in the window
        self.button_strombo_3= QPushButton('Strombo Frequency', self)
        self.button_strombo_3.setGeometry(750, 450, 100, 20)
        # connect button to function on_click
        self.button_strombo_3.clicked.connect(self.on_click_strombo_3_frequency)

        #Checkbox Stromboscope 3
        self.cb_strombo_3 = QCheckBox('Strombo_3', self)
        self.cb_strombo_3.setToolTip('Click if you wanna use strombo effect')
        self.cb_strombo_3.stateChanged.connect(self.strombo_demand_3)
        self.cb_strombo_3.setGeometry(610, 450, 300, 25)


        #Bouton effet rainbow 3 Loop
        self.button_rainbow_3 = QPushButton('Rainbow effect', self)
        self.button_rainbow_3.setToolTip('Click if you wanna use rainbow effect')
        self.button_rainbow_3.setGeometry(610, 480, 100, 25)
        self.button_rainbow_3.clicked.connect(self.rainbow_demand_3)


        #Bouton Blackout 3
        self.button_blackout_3 = QPushButton('Blackout', self)
        self.button_blackout_3.setToolTip('Turn off LEDs')
        self.button_blackout_3.setGeometry(610, 510, 100, 25)
        self.button_blackout_3.clicked.connect(self.blackout_demand_3)

        #Bouton theaterChase 3
        self.button_theaterChase_3 = QPushButton('theaterChase', self)
        self.button_theaterChase_3.setToolTip('theaterChase')
        self.button_theaterChase_3.setGeometry(610, 540, 100, 25)
        self.button_theaterChase_3.clicked.connect(self.theaterChase_demand_3)

        #Bouton theaterChaseRainbow 3
        self.button_theaterChaseRainbow_3 = QPushButton('theaterChaseRainbow', self)
        self.button_theaterChaseRainbow_3.setToolTip('theaterChaseRainbow')
        self.button_theaterChaseRainbow_3.setGeometry(610, 570, 100, 25)
        self.button_theaterChaseRainbow_3.clicked.connect(self.theaterChaseRainbow_demand_3)

        #Bouton multiColorWipe 3
        self.button_multiColorWipe_3 = QPushButton('multiColorWipe', self)
        self.button_multiColorWipe_3.setToolTip('multiColorWipe')
        self.button_multiColorWipe_3.setGeometry(610, 600, 100, 25)
        self.button_multiColorWipe_3.clicked.connect(self.multiColorWipe_demand_3)


        # Slider Red 3
        self.sl_R3 = QSlider(Qt.Vertical, self)
        self.sl_R3.setFocusPolicy(Qt.StrongFocus)
        self.sl_R3.setTickPosition(QSlider.TicksLeft)
        self.sl_R3.setTickInterval(1)
        self.sl_R3.setSingleStep(1)
        self.sl_R3.setGeometry(610, 200, 20, 200)
        self.sl_R3.setMinimum(0)
        self.sl_R3.setMaximum(255)
        self.sl_R3.valueChanged[int].connect(self.slider_R3)


        # Slider Green 3
        self.sl_G3 = QSlider(Qt.Vertical, self)
        self.sl_G3.setFocusPolicy(Qt.StrongFocus)
        self.sl_G3.setTickPosition(QSlider.TicksLeft)
        self.sl_G3.setTickInterval(1)
        self.sl_G3.setSingleStep(1)
        self.sl_G3.setGeometry(660, 200, 20, 200)
        self.sl_G3.setMinimum(0)
        self.sl_G3.setMaximum(255)
        self.sl_G3.valueChanged[int].connect(self.slider_G3)


        # Slider Blue 3
        self.sl_B3 = QSlider(Qt.Vertical, self)
        self.sl_B3.setFocusPolicy(Qt.StrongFocus)
        self.sl_B3.setTickPosition(QSlider.TicksLeft)
        self.sl_B3.setTickInterval(1)
        self.sl_B3.setSingleStep(1)
        self.sl_B3.setGeometry(710, 200, 20, 200)
        self.sl_B3.setMinimum(0)
        self.sl_B3.setMaximum(255)
        self.sl_B3.valueChanged[int].connect(self.slider_B3)


        # Slider White 3
        self.sl_W3 = QSlider(Qt.Vertical, self)
        self.sl_W3.setFocusPolicy(Qt.StrongFocus)
        self.sl_W3.setTickPosition(QSlider.TicksLeft)
        self.sl_W3.setTickInterval(1)
        self.sl_W3.setSingleStep(1)
        self.sl_W3.setGeometry(760, 200, 20, 200)
        self.sl_W3.setMinimum(0)
        self.sl_W3.setMaximum(255)
        self.sl_W3.valueChanged[int].connect(self.slider_W3)
        #########################################################################################################Strip 4

        #########################################################################################################Strip 5

    #########################################################################################################Strip 1

    def blackout_demand(self):
        self.msg1 = 'cosmoguirlande,blackout'
        self.newServer1.to_send = self.msg1

    def rainbow_demand(self):
        self.msg1 = 'cosmoguirlande,rainbow'
        self.newServer1.to_send = self.msg1

    def strombo_demand(self):
        self.msg1 = 'cosmoguirlande,strombo'
        self.newServer1.to_send = self.msg1

    def theaterChase_demand_1(self):
        self.msg1 = 'cosmoguirlande,theaterChase'
        self.newServer1.to_send = self.msg1

    def theaterChaseRainbow_demand_1(self):
        self.msg1 = 'cosmoguirlande,theaterChaseRainbow'
        self.newServer1.to_send = self.msg1

    def multiColorWipe_demand_1(self):
        self.msg1 = 'cosmoguirlande,multiColorWipe'
        self.newServer1.to_send = self.msg1

    def sync_demand(self, state):
        if self.cb_sync.isEnabled():
            self.newServer1.to_send = self.newServer2.to_send = 'cosmoguirlande,blackout'

            self.newServer1.to_send = self.newServer2.to_send = self.msg1

    # Slider Buttons functions
    def slider_R1(self, R1):
        self.msg1 = 'cosmoguirlande,R,' + str((R1))
        self.newServer1.to_send = self.msg1

    def slider_G1(self, G1):
        self.msg1 = 'cosmoguirlande,G,' + str((G1))
        self.newServer1.to_send = self.msg1

    def slider_B1(self, B1):
        self.msg1 = 'cosmoguirlande,B,' + str((B1))
        self.newServer1.to_send = self.msg1

    def slider_W1(self, W1):
        self.msg1 = 'cosmoguirlande,W,' + str((W1))
        self.newServer1.to_send = self.msg1

    def on_click_ip(self):
        IPValue = self.textbox_IP.text()
        QMessageBox.question(self, 'Message - pythonspot.com', "You typed: " + IPValue, QMessageBox.Ok, QMessageBox.Ok)
        self.textbox.setText("")

    def on_click_port(self):
        PortValue = self.textbox_port.text()
        QMessageBox.question(self, 'Message - pythonspot.com', "You typed: " + PortValue, QMessageBox.Ok,
                             QMessageBox.Ok)
        self.textbox.setText("")

    def on_click_strombo_frequency(self):
        Strombo_frequency = self.textbox_port.text()
        QMessageBox.question(self, 'Message - pythonspot.com', "You typed: " + Strombo_frequency, QMessageBox.Ok,
                             QMessageBox.Ok)
        self.textbox.setText("")
    #########################################################################################################Strip 2

    def on_click_strombo_2_frequency(self):
        Strombo_frequency = self.textbox_port.text()
        QMessageBox.question(self, 'Message - pythonspot.com', "You typed: " + Strombo_frequency, QMessageBox.Ok,
                             QMessageBox.Ok)
        self.textbox.setText("")


    def blackout_demand_2(self):
        self.msg2 ='cosmoguirlande,blackout'
        self.newServer2.to_send = self.msg2

    def rainbow_demand_2(self):
        self.msg2 = 'cosmoguirlande,rainbow'
        self.newServer2.to_send = self.msg2

    def strombo_demand_2(self):
        self.msg2 = 'cosmoguirlande,strombo'
        self.newServer2.to_send = self.msg2

    def theaterChase_demand_2(self):
        self.msg2 = 'cosmoguirlande,theaterChase'
        self.newServer2.to_send = self.msg2

    def theaterChaseRainbow_demand_2(self):
        self.msg2 = 'cosmoguirlande,theaterChaseRainbow'
        self.newServer2.to_send = self.msg2

    def multiColorWipe_demand_2(self):
        self.msg2 = 'cosmoguirlande,multiColorWipe'
        self.newServer2.to_send = self.msg2

    def sync_demand_2(self):
        self.msg2 = 'cosmoguirlande,sync'
        self.newServer2.to_send = self.msg2

    # Slider Buttons functions
    def slider_R2(self, R2):
        self.msg2 = 'cosmoguirlande,R,' + str((R2))
        self.newServer2.to_send =self.msg2

    def slider_G2(self, G2):
        self.msg2 = 'cosmoguirlande,G,' + str((G2))
        self.newServer2.to_send = self.msg2

    def slider_B2(self, B2):
        self.msg2 = 'cosmoguirlande,B,' + str((B2))
        self.newServer2.to_send = self.msg2

    def slider_W2(self, W2):
        self.msg2 = 'cosmoguirlande,W,' + str((W2))
        self.newServer2.to_send = self.msg2
    #########################################################################################################Strip 3

    def on_click_strombo_3_frequency(self):
        Strombo_frequency = self.textbox_port.text()
        QMessageBox.question(self, 'Message - pythonspot.com', "You typed: " + Strombo_frequency, QMessageBox.Ok,
                             QMessageBox.Ok)
        self.textbox.setText("")

    def blackout_demand_3(self):
        self.msg3 ='cosmoguirlande,blackout'
        self.newServer3.to_send = self.msg3

    def rainbow_demand_3(self):
        self.msg3 = 'cosmoguirlande,rainbow'
        self.newServer3.to_send = self.msg3

    def strombo_demand_3(self):
        self.msg3 = 'cosmoguirlande,strombo'
        self.newServer3.to_send = self.msg3

    def theaterChase_demand_3(self):
        self.msg3 = 'cosmoguirlande,theaterChase'
        self.newServer3.to_send = self.msg3

    def theaterChaseRainbow_demand_3(self):
        self.msg3 = 'cosmoguirlande,theaterChaseRainbow'
        self.newServer3.to_send = self.msg3

    def multiColorWipe_demand_3(self):
        self.msg3 = 'cosmoguirlande,multiColorWipe'
        self.newServer3.to_send = self.msg3

    def sync_demand_3(self):
        self.msg3 = 'cosmoguirlande,sync'
        self.newServer3.to_send = self.msg3

    # Slider Buttons functions
    def slider_R3(self, R3):
        self.msg3 = 'cosmoguirlande,R,' + str((R3))
        self.newServer3.to_send =self.msg3

    def slider_G3(self, G3):
        self.msg3 = 'cosmoguirlande,G,' + str((G3))
        self.newServer3.to_send = self.msg3

    def slider_B3(self, B3):
        self.msg3 = 'cosmoguirlande,B,' + str((B3))
        self.newServer3.to_send = self.msg3

    def slider_W3(self, W3):
        self.msg3 = 'cosmoguirlande,W,' + str((W3))
        self.newServer3.to_send = self.msg3

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWin()
    win.show()
    sys.exit(app.exec_())