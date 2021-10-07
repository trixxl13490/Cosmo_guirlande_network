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
    # Create Server5 object
    newServer6 = Server.Server('192.168.0.16', 50006, 1024)
    newServer6.start()

    #Create message to communicate with sensors
    msg1 = ''
    msg2 = ''
    msg3 = ''
    msg4 = ''
    msg5 = ''
    msg6 = ''

    #Synchronize message if True
    sync = False

    def __init__(self):
        #Init parent
        super().__init__()

        #Window configuration
        self.setFixedSize(1900, 1000)
        self.setWindowTitle("Cosmo Guirlandes Network GUI")
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

        #Couleur 2
        self.type_color21 = QComboBox(self)
        self.type_color21.setGeometry(60, 110, 100, 20)
        self.type_color21.addItems(["AMBER","AQUA","BLACK","BLUE", "CYAN","GOLD","GREEN","JADE","MAGENTA","OLD_LACE"
                                       ,"ORANGE", "PINK","PURPLE","RAINBOW","RED",
                                    "RGBW_WHITE_RGB" ,"RGBW_WHITE_RGBW","RGBW_WHITE_W", "TEAL", "WHITE","YELLOW" ])
        self.type_color21.currentIndexChanged.connect(self.color2_change_demand1)

        #Bouton Rainbow 1 Loop
        self.button_restart_1 = QPushButton('restart', self)
        self.button_restart_1.setToolTip('button_restart_1')
        self.button_restart_1.setGeometry(10, 140, 100, 25)
        self.button_restart_1.clicked.connect(self.restart_demand)

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

        #--------------------------------------------------------------------

        #Checkbox Stromboscope
        self.cb_strombo_1 = QCheckBox('Strombo_1', self)
        self.cb_strombo_1.setToolTip('Click if you wanna use strombo effect')
        self.cb_strombo_1.stateChanged.connect(self.strombo_demand)
        self.cb_strombo_1.setGeometry(10, 450, 300, 25)

        #--------------------------------------------------------------------

        #Bouton Rainbow 1 Loop
        self.button_rainbow_1 = QPushButton('Rainbow effect', self)
        self.button_rainbow_1.setToolTip('Click if you wanna use rainbow effect')
        self.button_rainbow_1.setGeometry(10, 480, 100, 25)
        self.button_rainbow_1.clicked.connect(self.rainbow_demand)

        #--------------------------------------------------------------------

        #Bouton Blackout 1
        self.button_blackout_1 = QPushButton('Blackout', self)
        self.button_blackout_1.setToolTip('Turn off LEDs')
        self.button_blackout_1.setGeometry(10, 510, 100, 25)
        self.button_blackout_1.clicked.connect(self.blackout_demand)
        #--------------------------------------------------------------------
        # Bouton chase 1
        self.button_chase_1 = QPushButton('chase', self)
        self.button_chase_1.setToolTip('chase')
        self.button_chase_1.setGeometry(10, 540, 100, 25)
        self.button_chase_1.clicked.connect(self.chase_demand_1)

        #Entree chase param speed
        # Create textbox
        self.textbox_chase_speed= QLineEdit(self)
        self.textbox_chase_speed.setGeometry(110, 540, 50, 20)
        # Create a button in the window
        self.button_chase_speed= QPushButton('speed', self)
        self.button_chase_speed.setGeometry(160, 540, 50, 20)
        # connect button to function on_click
        self.button_chase_speed.clicked.connect(self.on_click_ip)

        #Entree chase param size
        # Create textbox
        self.textbox_chase_size= QLineEdit(self)
        self.textbox_chase_size.setGeometry(210, 540, 50, 20)
        # Create a button in the window
        self.button_chase_size= QPushButton('size', self)
        self.button_chase_size.setGeometry(260, 540, 50, 20)
        # connect button to function on_click
        self.button_chase_size.clicked.connect(self.on_click_ip)
        #--------------------------------------------------------------------

        # Bouton comet 1
        self.button_comet_1 = QPushButton('comet', self)
        self.button_comet_1.setToolTip('comet')
        self.button_comet_1.setGeometry(10, 570, 100, 25)
        self.button_comet_1.clicked.connect(self.comet_demand_1)

        #Entree comet param speed
        # Create textbox
        self.textbox_comet_speed= QLineEdit(self)
        self.textbox_comet_speed.setGeometry(110, 570, 50, 20)
        # Create a button in the window
        self.button_comet_speed= QPushButton('speed', self)
        self.button_comet_speed.setGeometry(160, 570, 50, 20)
        # connect button to function on_click
        self.button_comet_speed.clicked.connect(self.on_click_ip)

        #Entree comet param tail
        # Create textbox
        self.textbox_comet_tail= QLineEdit(self)
        self.textbox_comet_tail.setGeometry(210, 570, 50, 20)
        # Create a button in the window
        self.button_comet_tail= QPushButton('tail', self)
        self.button_comet_tail.setGeometry(260, 570, 50, 20)
        # connect button to function on_click
        self.button_comet_tail.clicked.connect(self.on_click_ip)
        #--------------------------------------------------------------------

        # Bouton pulse 1
        self.button_pulse_1 = QPushButton('pulse', self)
        self.button_pulse_1.setToolTip('pulse')
        self.button_pulse_1.setGeometry(10, 600, 100, 25)
        self.button_pulse_1.clicked.connect(self.pulse_demand_1)

        #Entree pulse param speed
        # Create textbox
        self.textbox_pulse_speed= QLineEdit(self)
        self.textbox_pulse_speed.setGeometry(110, 600, 50, 20)
        # Create a button in the window
        self.button_pulse_speed= QPushButton('speed', self)
        self.button_pulse_speed.setGeometry(160, 600, 50, 20)
        # connect button to function on_click
        self.button_pulse_speed.clicked.connect(self.on_click_ip)

        #Entree pulse param period
        # Create textbox
        self.textbox_pulse_period= QLineEdit(self)
        self.textbox_pulse_period.setGeometry(210, 600, 50, 20)
        # Create a button in the window
        self.button_pulse_period= QPushButton('period', self)
        self.button_pulse_period.setGeometry(260, 600, 50, 20)
        # connect button to function on_click
        self.button_pulse_period.clicked.connect(self.on_click_ip)
        #--------------------------------------------------------------------

        # Bouton sparkle 1
        self.button_sparkle_1 = QPushButton('sparkle', self)
        self.button_sparkle_1.setToolTip('sparkle')
        self.button_sparkle_1.setGeometry(10, 630, 100, 25)
        self.button_sparkle_1.clicked.connect(self.sparkle_demand_1)

        #Entree sparkle param speed
        # Create textbox
        self.textbox_sparkle_speed= QLineEdit(self)
        self.textbox_sparkle_speed.setGeometry(110, 630, 50, 20)
        # Create a button in the window
        self.button_sparkle_speed= QPushButton('speed', self)
        self.button_sparkle_speed.setGeometry(160, 630, 50, 20)
        # connect button to function on_click
        self.button_sparkle_speed.clicked.connect(self.on_click_ip)

        #Entree sparkle param num_sparkles
        # Create textbox
        self.textbox_sparkle_num_sparkles= QLineEdit(self)
        self.textbox_sparkle_num_sparkles.setGeometry(210, 630, 50, 20)
        # Create a button in the window
        self.button_sparkle_num_sparkles= QPushButton('num_sparkles', self)
        self.button_sparkle_num_sparkles.setGeometry(260, 630, 50, 20)
        # connect button to function on_click
        self.button_sparkle_num_sparkles.clicked.connect(self.on_click_ip)
        #--------------------------------------------------------------------

        # Bouton solid 1
        self.button_solid_1 = QPushButton('solid', self)
        self.button_solid_1.setToolTip('solid')
        self.button_solid_1.setGeometry(10, 660, 100, 25)
        self.button_solid_1.clicked.connect(self.solid_demand_1)
        #--------------------------------------------------------------------

        # Bouton colorcycle 1
        self.button_colorcycle_1 = QPushButton('colorcycle', self)
        self.button_colorcycle_1.setToolTip('colorcycle')
        self.button_colorcycle_1.setGeometry(10, 690, 100, 25)
        self.button_colorcycle_1.clicked.connect(self.colorcycle_demand_1)

        #Entree color_cycle param speed
        # Create textbox
        self.textbox_color_cycle_speed= QLineEdit(self)
        self.textbox_color_cycle_speed.setGeometry(110, 690, 50, 20)
        # Create a button in the window
        self.button_color_cycle_speed= QPushButton('speed', self)
        self.button_color_cycle_speed.setGeometry(160, 690, 50, 20)
        # connect button to function on_click
        self.button_color_cycle_speed.clicked.connect(self.on_click_ip)

        #--------------------------------------------------------------------

        # Bouton Dancing Pi Sroll 1
        self.button_dancingPiScroll = QPushButton('dancingPiSroll', self)
        self.button_dancingPiScroll.setToolTip('dancingPiSroll')
        self.button_dancingPiScroll.setGeometry(10, 720, 100, 25)
        self.button_dancingPiScroll.clicked.connect(self.dancingPiScroll_demand_1)

        # Bouton stop_Dancing Pi Sroll 1
        self.button_stop_dancingPiScroll = QPushButton('stop_dancingPiSroll', self)
        self.button_stop_dancingPiScroll.setToolTip('stop_dancingPiSroll')
        self.button_stop_dancingPiScroll.setGeometry(110, 720, 100, 25)
        self.button_stop_dancingPiScroll.clicked.connect(self.stop_dancingPiScroll_demand_1)
        #--------------------------------------------------------------------

        # Bouton Dancing Pi Spectrum 1
        self.button_dancingPiSpectrum = QPushButton('dancingPiSpectrum', self)
        self.button_dancingPiSpectrum.setToolTip('dancingPiSpectrum')
        self.button_dancingPiSpectrum.setGeometry(10, 750, 100, 25)
        self.button_dancingPiSpectrum.clicked.connect(self.dancingPiSpectrum_demand_1)

        # Bouton stop_Dancing Pi Spectrum 1
        self.button_stop_dancingPiSpectrum = QPushButton('stop_dancingPiSpectrum', self)
        self.button_stop_dancingPiSpectrum.setToolTip('stop_dancingPiSpectrum')
        self.button_stop_dancingPiSpectrum.setGeometry(110, 750, 100, 25)
        self.button_stop_dancingPiSpectrum.clicked.connect(self.stop_dancingPiSpectrum_demand_1)
        #--------------------------------------------------------------------

        # Bouton Dancing Pi Energy 1
        self.button_dancingPiEnergy = QPushButton('dancingPiEnergy', self)
        self.button_dancingPiEnergy.setToolTip('dancingPiEnergy')
        self.button_dancingPiEnergy.setGeometry(10, 780, 100, 25)
        self.button_dancingPiEnergy.clicked.connect(self.dancingPiEnergy_demand_1)

        # Bouton stop_Dancing Pi Energy 1
        self.button_stop_dancingPiEnergy = QPushButton('stop_dancingPiEnergy', self)
        self.button_stop_dancingPiEnergy.setToolTip('stop_dancingPiEnergy')
        self.button_stop_dancingPiEnergy.setGeometry(110, 780, 100, 25)
        self.button_stop_dancingPiEnergy.clicked.connect(self.stop_dancingPiEnergy_demand_1)
        #--------------------------------------------------------------------

        # Bouton Cosmo Ball 1
        self.button_cosmoBall = QPushButton('cosmoBall', self)
        self.button_cosmoBall.setToolTip('cosmoBall')
        self.button_cosmoBall.setGeometry(10,810, 100, 25)
        #self.button_dancingPi.clicked.connect(self.cosmoBall_demand_1)

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

        # Bouton chase 2
        self.button_chase_2 = QPushButton('chase', self)
        self.button_chase_2.setToolTip('chase')
        self.button_chase_2.setGeometry(310, 540, 100, 25)
        self.button_chase_2.clicked.connect(self.chase_demand_2)

        # Bouton comet 2
        self.button_comet_2 = QPushButton('comet', self)
        self.button_comet_2.setToolTip('comet')
        self.button_comet_2.setGeometry(310, 570, 100, 25)
        self.button_comet_2.clicked.connect(self.comet_demand_2)

        # Bouton pulse 2
        self.button_pulse_2 = QPushButton('pulse', self)
        self.button_pulse_2.setToolTip('pulse')
        self.button_pulse_2.setGeometry(310, 600, 100, 25)
        self.button_pulse_2.clicked.connect(self.pulse_demand_2)

        # Bouton sparkle 2
        self.button_sparkle_2 = QPushButton('sparkle', self)
        self.button_sparkle_2.setToolTip('sparkle')
        self.button_sparkle_2.setGeometry(310, 630, 100, 25)
        self.button_sparkle_2.clicked.connect(self.sparkle_demand_2)


        # Bouton solid
        self.button_solid_2 = QPushButton('solid', self)
        self.button_solid_2.setToolTip('solid')
        self.button_solid_2.setGeometry(310, 660, 100, 25)
        self.button_solid_2.clicked.connect(self.solid_demand_2)

        # Bouton colorcycle 2
        self.button_colorcycle_2 = QPushButton('colorcycle', self)
        self.button_colorcycle_2.setToolTip('colorcycle')
        self.button_colorcycle_2.setGeometry(310, 690, 100, 25)
        self.button_colorcycle_2.clicked.connect(self.colorcycle_demand_2)

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

        # Bouton chase 3
        self.button_chase_3 = QPushButton('chase', self)
        self.button_chase_3.setToolTip('chase')
        self.button_chase_3.setGeometry(610, 540, 100, 25)
        self.button_chase_3.clicked.connect(self.chase_demand_3)

        # Bouton comet 3
        self.button_comet_3 = QPushButton('comet', self)
        self.button_comet_3.setToolTip('comet')
        self.button_comet_3.setGeometry(610, 570, 100, 25)
        self.button_comet_3.clicked.connect(self.comet_demand_3)

        # Bouton pulse 3
        self.button_pulse_3 = QPushButton('pulse', self)
        self.button_pulse_3.setToolTip('pulse')
        self.button_pulse_3.setGeometry(610, 600, 100, 25)
        self.button_pulse_3.clicked.connect(self.pulse_demand_3)

        # Bouton sparkle 3
        self.button_sparkle_3 = QPushButton('sparkle', self)
        self.button_sparkle_3.setToolTip('sparkle')
        self.button_sparkle_3.setGeometry(610, 630, 100, 25)
        self.button_sparkle_3.clicked.connect(self.sparkle_demand_3)


        # Bouton solid 3
        self.button_solid_3 = QPushButton('solid', self)
        self.button_solid_3.setToolTip('solid')
        self.button_solid_3.setGeometry(610, 660, 100, 25)
        self.button_solid_3.clicked.connect(self.solid_demand_3)

        # Bouton colorcycle 1
        self.button_colorcycle_3 = QPushButton('colorcycle', self)
        self.button_colorcycle_3.setToolTip('colorcycle')
        self.button_colorcycle_3.setGeometry(610, 690, 100, 25)
        self.button_colorcycle_3.clicked.connect(self.colorcycle_demand_3)

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
        #########################################################################################################Strip 4
        #Entree Frequence Strombo 4
        # Create textbox
        self.textbox_strombo_4 = QLineEdit(self)
        self.textbox_strombo_4.setGeometry(1000, 450, 50, 20)
        # Create a button in the window
        self.button_strombo_4= QPushButton('Strombo Frequency', self)
        self.button_strombo_4.setGeometry(1050, 450, 100, 20)
        # connect button to function on_click
        self.button_strombo_4.clicked.connect(self.on_click_strombo_4_frequency)

        #Checkbox Stromboscope 4
        self.cb_strombo_4 = QCheckBox('Strombo_4', self)
        self.cb_strombo_4.setToolTip('Click if you wanna use strombo effect')
        self.cb_strombo_4.stateChanged.connect(self.strombo_demand_4)
        self.cb_strombo_4.setGeometry(910, 450, 400, 25)


        #Bouton effet rainbow 4 Loop
        self.button_rainbow_4 = QPushButton('Rainbow effect', self)
        self.button_rainbow_4.setToolTip('Click if you wanna use rainbow effect')
        self.button_rainbow_4.setGeometry(910, 480, 100, 25)
        self.button_rainbow_4.clicked.connect(self.rainbow_demand_4)


        #Bouton Blackout 4
        self.button_blackout_4 = QPushButton('Blackout', self)
        self.button_blackout_4.setToolTip('Turn off LEDs')
        self.button_blackout_4.setGeometry(910, 510, 100, 25)
        self.button_blackout_4.clicked.connect(self.blackout_demand_4)

        # Bouton chase 4
        self.button_chase_4 = QPushButton('chase', self)
        self.button_chase_4.setToolTip('chase')
        self.button_chase_4.setGeometry(910, 540, 100, 25)
        self.button_chase_4.clicked.connect(self.chase_demand_4)

        # Bouton comet 4
        self.button_comet_4 = QPushButton('comet', self)
        self.button_comet_4.setToolTip('comet')
        self.button_comet_4.setGeometry(910, 570, 100, 25)
        self.button_comet_4.clicked.connect(self.comet_demand_4)

        # Bouton pulse 4
        self.button_pulse_4 = QPushButton('pulse', self)
        self.button_pulse_4.setToolTip('pulse')
        self.button_pulse_4.setGeometry(910, 600, 100, 25)
        self.button_pulse_4.clicked.connect(self.pulse_demand_4)

        # Bouton sparkle 4
        self.button_sparkle_4 = QPushButton('sparkle', self)
        self.button_sparkle_4.setToolTip('sparkle')
        self.button_sparkle_4.setGeometry(910, 630, 100, 25)
        self.button_sparkle_4.clicked.connect(self.sparkle_demand_4)


        # Bouton solid 4
        self.button_solid_4 = QPushButton('solid', self)
        self.button_solid_4.setToolTip('solid')
        self.button_solid_4.setGeometry(910, 660, 100, 25)
        self.button_solid_4.clicked.connect(self.solid_demand_4)

        # Bouton colorcycle 1
        self.button_colorcycle_4 = QPushButton('colorcycle', self)
        self.button_colorcycle_4.setToolTip('colorcycle')
        self.button_colorcycle_4.setGeometry(910, 690, 100, 25)
        self.button_colorcycle_4.clicked.connect(self.colorcycle_demand_4)

        # Slider Red 4
        self.sl_R4 = QSlider(Qt.Vertical, self)
        self.sl_R4.setFocusPolicy(Qt.StrongFocus)
        self.sl_R4.setTickPosition(QSlider.TicksLeft)
        self.sl_R4.setTickInterval(1)
        self.sl_R4.setSingleStep(1)
        self.sl_R4.setGeometry(910, 200, 20, 200)
        self.sl_R4.setMinimum(0)
        self.sl_R4.setMaximum(255)
        self.sl_R4.valueChanged[int].connect(self.slider_R4)


        # Slider Green 4
        self.sl_G4 = QSlider(Qt.Vertical, self)
        self.sl_G4.setFocusPolicy(Qt.StrongFocus)
        self.sl_G4.setTickPosition(QSlider.TicksLeft)
        self.sl_G4.setTickInterval(1)
        self.sl_G4.setSingleStep(1)
        self.sl_G4.setGeometry(960, 200, 20, 200)
        self.sl_G4.setMinimum(0)
        self.sl_G4.setMaximum(255)
        self.sl_G4.valueChanged[int].connect(self.slider_G4)


        # Slider Blue 4
        self.sl_B4 = QSlider(Qt.Vertical, self)
        self.sl_B4.setFocusPolicy(Qt.StrongFocus)
        self.sl_B4.setTickPosition(QSlider.TicksLeft)
        self.sl_B4.setTickInterval(1)
        self.sl_B4.setSingleStep(1)
        self.sl_B4.setGeometry(1010, 200, 20, 200)
        self.sl_B4.setMinimum(0)
        self.sl_B4.setMaximum(255)
        self.sl_B4.valueChanged[int].connect(self.slider_B4)


        # Slider White 4
        self.sl_W4 = QSlider(Qt.Vertical, self)
        self.sl_W4.setFocusPolicy(Qt.StrongFocus)
        self.sl_W4.setTickPosition(QSlider.TicksLeft)
        self.sl_W4.setTickInterval(1)
        self.sl_W4.setSingleStep(1)
        self.sl_W4.setGeometry(1060, 200, 20, 200)
        self.sl_W4.setMinimum(0)
        self.sl_W4.setMaximum(255)
        self.sl_W4.valueChanged[int].connect(self.slider_W4)
        #########################################################################################################Strip 5
        #Entree Frequence Strombo 5
        # Create textbox
        self.textbox_strombo_5 = QLineEdit(self)
        self.textbox_strombo_5.setGeometry(1300, 450, 50, 20)
        # Create a button in the window
        self.button_strombo_5= QPushButton('Strombo Frequency', self)
        self.button_strombo_5.setGeometry(1350, 450, 100, 20)
        # connect button to function on_click
        self.button_strombo_5.clicked.connect(self.on_click_strombo_5_frequency)

        #Checkbox Stromboscope 5
        self.cb_strombo_5 = QCheckBox('Strombo_5', self)
        self.cb_strombo_5.setToolTip('Click if you wanna use strombo effect')
        self.cb_strombo_5.stateChanged.connect(self.strombo_demand_5)
        self.cb_strombo_5.setGeometry(1210, 450, 500, 25)


        #Bouton effet rainbow 5 Loop
        self.button_rainbow_5 = QPushButton('Rainbow effect', self)
        self.button_rainbow_5.setToolTip('Click if you wanna use rainbow effect')
        self.button_rainbow_5.setGeometry(1210, 480, 100, 25)
        self.button_rainbow_5.clicked.connect(self.rainbow_demand_5)


        #Bouton Blackout 5
        self.button_blackout_5 = QPushButton('Blackout', self)
        self.button_blackout_5.setToolTip('Turn off LEDs')
        self.button_blackout_5.setGeometry(1210, 510, 100, 25)
        self.button_blackout_5.clicked.connect(self.blackout_demand_5)

        # Bouton chase 5
        self.button_chase_5 = QPushButton('chase', self)
        self.button_chase_5.setToolTip('chase')
        self.button_chase_5.setGeometry(1210, 540, 100, 25)
        self.button_chase_5.clicked.connect(self.chase_demand_5)

        # Bouton comet 5
        self.button_comet_5 = QPushButton('comet', self)
        self.button_comet_5.setToolTip('comet')
        self.button_comet_5.setGeometry(1210, 570, 100, 25)
        self.button_comet_5.clicked.connect(self.comet_demand_5)

        # Bouton pulse 5
        self.button_pulse_5 = QPushButton('pulse', self)
        self.button_pulse_5.setToolTip('pulse')
        self.button_pulse_5.setGeometry(1210, 600, 100, 25)
        self.button_pulse_5.clicked.connect(self.pulse_demand_5)

        # Bouton sparkle 5
        self.button_sparkle_5 = QPushButton('sparkle', self)
        self.button_sparkle_5.setToolTip('sparkle')
        self.button_sparkle_5.setGeometry(1210, 630, 100, 25)
        self.button_sparkle_5.clicked.connect(self.sparkle_demand_5)


        # Bouton solid 5
        self.button_solid_5 = QPushButton('solid', self)
        self.button_solid_5.setToolTip('solid')
        self.button_solid_5.setGeometry(1210, 660, 100, 25)
        self.button_solid_5.clicked.connect(self.solid_demand_5)

        # Bouton colorcycle 5
        self.button_colorcycle_5 = QPushButton('colorcycle', self)
        self.button_colorcycle_5.setToolTip('colorcycle')
        self.button_colorcycle_5.setGeometry(1210, 690, 100, 25)
        self.button_colorcycle_5.clicked.connect(self.colorcycle_demand_5)

        # Slider Red 5
        self.sl_R5 = QSlider(Qt.Vertical, self)
        self.sl_R5.setFocusPolicy(Qt.StrongFocus)
        self.sl_R5.setTickPosition(QSlider.TicksLeft)
        self.sl_R5.setTickInterval(1)
        self.sl_R5.setSingleStep(1)
        self.sl_R5.setGeometry(1210, 200, 20, 200)
        self.sl_R5.setMinimum(0)
        self.sl_R5.setMaximum(255)
        self.sl_R5.valueChanged[int].connect(self.slider_R5)


        # Slider Green 5
        self.sl_G5 = QSlider(Qt.Vertical, self)
        self.sl_G5.setFocusPolicy(Qt.StrongFocus)
        self.sl_G5.setTickPosition(QSlider.TicksLeft)
        self.sl_G5.setTickInterval(1)
        self.sl_G5.setSingleStep(1)
        self.sl_G5.setGeometry(1260, 200, 20, 200)
        self.sl_G5.setMinimum(0)
        self.sl_G5.setMaximum(255)
        self.sl_G5.valueChanged[int].connect(self.slider_G5)


        # Slider Blue 5
        self.sl_B5 = QSlider(Qt.Vertical, self)
        self.sl_B5.setFocusPolicy(Qt.StrongFocus)
        self.sl_B5.setTickPosition(QSlider.TicksLeft)
        self.sl_B5.setTickInterval(1)
        self.sl_B5.setSingleStep(1)
        self.sl_B5.setGeometry(1310, 200, 20, 200)
        self.sl_B5.setMinimum(0)
        self.sl_B5.setMaximum(255)
        self.sl_B5.valueChanged[int].connect(self.slider_B5)


        # Slider White 5
        self.sl_W5 = QSlider(Qt.Vertical, self)
        self.sl_W5.setFocusPolicy(Qt.StrongFocus)
        self.sl_W5.setTickPosition(QSlider.TicksLeft)
        self.sl_W5.setTickInterval(1)
        self.sl_W5.setSingleStep(1)
        self.sl_W5.setGeometry(1360, 200, 20, 200)
        self.sl_W5.setMinimum(0)
        self.sl_W5.setMaximum(255)
        self.sl_W5.valueChanged[int].connect(self.slider_W5)

        #########################################################################################################Strip 6
        #Entree Frequence Strombo 6
        # Create textbox
        self.textbox_strombo_6 = QLineEdit(self)
        self.textbox_strombo_6.setGeometry(1600, 450, 50, 20)
        # Create a button in the window
        self.button_strombo_6= QPushButton('Strombo Frequency', self)
        self.button_strombo_6.setGeometry(1650, 450, 100, 20)
        # connect button to function on_click
        self.button_strombo_6.clicked.connect(self.on_click_strombo_6_frequency)

        #Checkbox Stromboscope 6
        self.cb_strombo_6 = QCheckBox('Strombo_6', self)
        self.cb_strombo_6.setToolTip('Click if you wanna use strombo effect')
        self.cb_strombo_6.stateChanged.connect(self.strombo_demand_6)
        self.cb_strombo_6.setGeometry(1510, 450, 500, 25)


        #Bouton effet rainbow 6 Loop
        self.button_rainbow_6 = QPushButton('Rainbow effect', self)
        self.button_rainbow_6.setToolTip('Click if you wanna use rainbow effect')
        self.button_rainbow_6.setGeometry(1510, 480, 100, 25)
        self.button_rainbow_6.clicked.connect(self.rainbow_demand_6)


        #Bouton Blackout 6
        self.button_blackout_6 = QPushButton('Blackout', self)
        self.button_blackout_6.setToolTip('Turn off LEDs')
        self.button_blackout_6.setGeometry(1510, 510, 100, 25)
        self.button_blackout_6.clicked.connect(self.blackout_demand_6)

        # Bouton chase 6
        self.button_chase_6 = QPushButton('chase', self)
        self.button_chase_6.setToolTip('chase')
        self.button_chase_6.setGeometry(1510, 540, 100, 25)
        self.button_chase_6.clicked.connect(self.chase_demand_6)

        # Bouton comet 6
        self.button_comet_6 = QPushButton('comet', self)
        self.button_comet_6.setToolTip('comet')
        self.button_comet_6.setGeometry(1510, 570, 100, 25)
        self.button_comet_6.clicked.connect(self.comet_demand_6)

        # Bouton pulse 6
        self.button_pulse_6 = QPushButton('pulse', self)
        self.button_pulse_6.setToolTip('pulse')
        self.button_pulse_6.setGeometry(1510, 600, 100, 25)
        self.button_pulse_6.clicked.connect(self.pulse_demand_6)

        # Bouton sparkle 6
        self.button_sparkle_6 = QPushButton('sparkle', self)
        self.button_sparkle_6.setToolTip('sparkle')
        self.button_sparkle_6.setGeometry(1510, 630, 100, 25)
        self.button_sparkle_6.clicked.connect(self.sparkle_demand_6)


        # Bouton solid 6
        self.button_solid_6 = QPushButton('solid', self)
        self.button_solid_6.setToolTip('solid')
        self.button_solid_6.setGeometry(1510, 660, 100, 25)
        self.button_solid_6.clicked.connect(self.solid_demand_6)

        # Bouton colorcycle 6
        self.button_colorcycle_6 = QPushButton('colorcycle', self)
        self.button_colorcycle_6.setToolTip('colorcycle')
        self.button_colorcycle_6.setGeometry(1510, 690, 100, 25)
        self.button_colorcycle_6.clicked.connect(self.colorcycle_demand_6)

        # Slider Red 6
        self.sl_R6 = QSlider(Qt.Vertical, self)
        self.sl_R6.setFocusPolicy(Qt.StrongFocus)
        self.sl_R6.setTickPosition(QSlider.TicksLeft)
        self.sl_R6.setTickInterval(1)
        self.sl_R6.setSingleStep(1)
        self.sl_R6.setGeometry(1510, 200, 20, 200)
        self.sl_R6.setMinimum(0)
        self.sl_R6.setMaximum(255)
        self.sl_R6.valueChanged[int].connect(self.slider_R6)


        # Slider Green 6
        self.sl_G6 = QSlider(Qt.Vertical, self)
        self.sl_G6.setFocusPolicy(Qt.StrongFocus)
        self.sl_G6.setTickPosition(QSlider.TicksLeft)
        self.sl_G6.setTickInterval(1)
        self.sl_G6.setSingleStep(1)
        self.sl_G6.setGeometry(1560, 200, 20, 200)
        self.sl_G6.setMinimum(0)
        self.sl_G6.setMaximum(255)
        self.sl_G6.valueChanged[int].connect(self.slider_G6)


        # Slider Blue 6
        self.sl_B6 = QSlider(Qt.Vertical, self)
        self.sl_B6.setFocusPolicy(Qt.StrongFocus)
        self.sl_B6.setTickPosition(QSlider.TicksLeft)
        self.sl_B6.setTickInterval(1)
        self.sl_B6.setSingleStep(1)
        self.sl_B6.setGeometry(1610, 200, 20, 200)
        self.sl_B6.setMinimum(0)
        self.sl_B6.setMaximum(255)
        self.sl_B6.valueChanged[int].connect(self.slider_B6)


        # Slider White 6
        self.sl_W6 = QSlider(Qt.Vertical, self)
        self.sl_W6.setFocusPolicy(Qt.StrongFocus)
        self.sl_W6.setTickPosition(QSlider.TicksLeft)
        self.sl_W6.setTickInterval(1)
        self.sl_W6.setSingleStep(1)
        self.sl_W6.setGeometry(1660, 200, 20, 200)
        self.sl_W6.setMinimum(0)
        self.sl_W6.setMaximum(255)
        self.sl_W6.valueChanged[int].connect(self.slider_W6)

    #########################################################################################################Strip 1

    def restart_demand(self):
        self.msg1 = 'cosmoguirlande,restart'
        if self.sync:
            self.newServer2.to_send = self.msg1
            self.newServer3.to_send = self.msg1
            self.newServer4.to_send = self.msg1
            self.newServer5.to_send = self.msg1
            self.newServer6.to_send = self.msg1

    def color1_change_demand1(self):
        print("selection changed ", self.type_color11.currentText())
        self.msg1 = 'cosmoguirlande,color1,' + str(( self.type_color11.currentText()))
        self.newServer1.to_send = self.msg1
        self.newServer2.to_send = self.msg1
        self.newServer3.to_send = self.msg1
        self.newServer4.to_send = self.msg1
        self.newServer5.to_send = self.msg1
        self.newServer6.to_send = self.msg1

    def color2_change_demand1(self):
        print("selection changed ", self.type_color21.currentText())
        self.msg1 = 'cosmoguirlande,color2,' + str(( self.type_color21.currentText()))
        self.newServer1.to_send = self.msg1
        self.newServer2.to_send = self.msg1
        self.newServer3.to_send = self.msg1
        self.newServer4.to_send = self.msg1
        self.newServer5.to_send = self.msg1
        self.newServer6.to_send = self.msg1


    def blackout_demand(self):
        self.msg1 = 'cosmoguirlande,blackout'
        self.newServer1.to_send = self.msg1
        if self.sync:
            self.newServer2.to_send = self.msg1
            self.newServer3.to_send = self.msg1
            self.newServer4.to_send = self.msg1
            self.newServer5.to_send = self.msg1
            self.newServer6.to_send = self.msg1

    def rainbow_demand(self):
        self.msg1 = 'cosmoguirlande,rainbow'
        self.newServer1.to_send = self.msg1
        if self.sync:
            self.newServer2.to_send = self.msg1
            self.newServer3.to_send = self.msg1
            self.newServer4.to_send = self.msg1
            self.newServer5.to_send = self.msg1
            self.newServer6.to_send = self.msg1

    def strombo_demand(self):
        self.msg1 = 'cosmoguirlande,strombo'
        self.newServer1.to_send = self.msg1
        if self.sync:
            self.newServer2.to_send = self.msg1
            self.newServer3.to_send = self.msg1
            self.newServer4.to_send = self.msg1
            self.newServer5.to_send = self.msg1
            self.newServer6.to_send = self.msg1

    def chase_demand_1(self):
        self.msg1 = 'cosmoguirlande,chase,' + self.textbox_chase_speed.text() + ',' + self.textbox_chase_size.text()
        self.newServer1.to_send = self.msg1
        if self.sync:
            self.newServer2.to_send = self.msg1
            self.newServer3.to_send = self.msg1
            self.newServer4.to_send = self.msg1
            self.newServer5.to_send = self.msg1
            self.newServer6.to_send = self.msg1

    def comet_demand_1(self):
        self.msg1 = 'cosmoguirlande,comet,' + self.textbox_comet_speed.text() + ',' + self.textbox_comet_tail.text()
        self.newServer1.to_send = self.msg1
        if self.sync:
            self.newServer2.to_send = self.msg1
            self.newServer3.to_send = self.msg1
            self.newServer4.to_send = self.msg1
            self.newServer5.to_send = self.msg1
            self.newServer6.to_send = self.msg1

    def sparkle_demand_1(self):
        self.msg1 = 'cosmoguirlande,sparkle,' + self.textbox_sparkle_speed.text() + ',' + self.textbox_sparkle_num_sparkles.text()
        self.newServer1.to_send = self.msg1
        if self.sync:
            self.newServer2.to_send = self.msg1
            self.newServer3.to_send = self.msg1
            self.newServer4.to_send = self.msg1
            self.newServer5.to_send = self.msg1
            self.newServer6.to_send = self.msg1

    def pulse_demand_1(self):
        self.msg1 = 'cosmoguirlande,pulse,'+ self.textbox_pulse_period.text() + ',' + self.textbox_pulse_speed.text()
        self.newServer1.to_send = self.msg1
        if self.sync:
            self.newServer2.to_send = self.msg1
            self.newServer3.to_send = self.msg1
            self.newServer4.to_send = self.msg1
            self.newServer5.to_send = self.msg1
            self.newServer6.to_send = self.msg1

    def solid_demand_1(self):
        self.msg1 = 'cosmoguirlande,solid'
        self.newServer1.to_send = self.msg1
        if self.sync:
            self.newServer2.to_send = self.msg1
            self.newServer3.to_send = self.msg1
            self.newServer4.to_send = self.msg1
            self.newServer5.to_send = self.msg1
            self.newServer6.to_send = self.msg1

    def colorcycle_demand_1(self):
        self.msg1 = 'cosmoguirlande,colorcycle,'++ self.textbox_color_cycle_speed.text()
        self.newServer1.to_send = self.msg1
        if self.sync:
            self.newServer2.to_send = self.msg1
            self.newServer3.to_send = self.msg1
            self.newServer4.to_send = self.msg1
            self.newServer5.to_send = self.msg1
            self.newServer6.to_send = self.msg1

    def sync_demand(self, state):
        self.sync = not self.sync
        if self.sync:
            self.newServer2.to_send = self.msg1
            self.newServer3.to_send = self.msg1
            self.newServer4.to_send = self.msg1
            self.newServer5.to_send = self.msg1
            self.newServer6.to_send = self.msg1


    def dancingPiScroll_demand_1(self):
        self.msg1 = 'cosmoguirlande,dancingPiScroll'
        self.newServer1.to_send = self.msg1
        if self.sync:
            self.newServer2.to_send = self.msg1
            self.newServer3.to_send = self.msg1
            self.newServer4.to_send = self.msg1
            self.newServer5.to_send = self.msg1
            self.newServer6.to_send = self.msg1


    def dancingPiEnergy_demand_1(self):
        self.msg1 = 'cosmoguirlande,dancingPiEnergy'
        self.newServer1.to_send = self.msg1
        if self.sync:
            self.newServer2.to_send = self.msg1
            self.newServer3.to_send = self.msg1
            self.newServer4.to_send = self.msg1
            self.newServer5.to_send = self.msg1
            self.newServer6.to_send = self.msg1


    def dancingPiSpectrum_demand_1(self):
        self.msg1 = 'cosmoguirlande,dancingPiSpectrum'
        self.newServer1.to_send = self.msg1
        if self.sync:
            self.newServer2.to_send = self.msg1
            self.newServer3.to_send = self.msg1
            self.newServer4.to_send = self.msg1
            self.newServer5.to_send = self.msg1
            self.newServer6.to_send = self.msg1

    def stop_dancingPiEnergy_demand_1(self):
        self.msg1 = 'cosmoguirlande,stop_dancingPiEnergy'
        self.newServer1.to_send = self.msg1
        if self.sync:
            self.newServer2.to_send = self.msg1
            self.newServer3.to_send = self.msg1
            self.newServer4.to_send = self.msg1
            self.newServer5.to_send = self.msg1
            self.newServer6.to_send = self.msg1

    def stop_dancingPiSpectrum_demand_1(self):
        self.msg1 = 'cosmoguirlande,stop_dancingPiSpectrum'
        self.newServer1.to_send = self.msg1
        if self.sync:
            self.newServer2.to_send = self.msg1
            self.newServer3.to_send = self.msg1
            self.newServer4.to_send = self.msg1
            self.newServer5.to_send = self.msg1
            self.newServer6.to_send = self.msg1

    def stop_dancingPiScroll_demand_1(self):
        self.msg1 = 'cosmoguirlande,stop_dancingPiScroll'
        self.newServer1.to_send = self.msg1
        if self.sync:
            self.newServer2.to_send = self.msg1
            self.newServer3.to_send = self.msg1
            self.newServer4.to_send = self.msg1
            self.newServer5.to_send = self.msg1
            self.newServer6.to_send = self.msg1

    # Slider Buttons functions
    def slider_R1(self, R1):
        self.msg1 = 'cosmoguirlande,R,' + str((R1))
        self.newServer1.to_send = self.msg1
        if self.sync:
            self.newServer2.to_send = self.msg1
            self.newServer3.to_send = self.msg1
            self.newServer4.to_send = self.msg1
            self.newServer5.to_send = self.msg1
            self.newServer6.to_send = self.msg1

    def slider_G1(self, G1):
        self.msg1 = 'cosmoguirlande,G,' + str((G1))
        self.newServer1.to_send = self.msg1
        if self.sync:
            self.newServer2.to_send = self.msg1
            self.newServer3.to_send = self.msg1
            self.newServer4.to_send = self.msg1
            self.newServer5.to_send = self.msg1
            self.newServer6.to_send = self.msg1

    def slider_B1(self, B1):
        self.msg1 = 'cosmoguirlande,B,' + str((B1))
        self.newServer1.to_send = self.msg1
        if self.sync:
            self.newServer2.to_send = self.msg1
            self.newServer3.to_send = self.msg1
            self.newServer4.to_send = self.msg1
            self.newServer5.to_send = self.msg1
            self.newServer6.to_send = self.msg1

    def slider_W1(self, W1):
        self.msg1 = 'cosmoguirlande,W,' + str((W1))
        self.newServer1.to_send = self.msg1
        if self.sync:
            self.newServer2.to_send = self.msg1
            self.newServer3.to_send = self.msg1
            self.newServer4.to_send = self.msg1
            self.newServer5.to_send = self.msg1
            self.newServer6.to_send = self.msg1

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

    def chase_demand_2(self):
        self.msg2 = 'cosmoguirlande,chase'
        self.newServer2.to_send = self.msg2

    def comet_demand_2(self):
        self.msg2 = 'cosmoguirlande,comet'
        self.newServer2.to_send = self.msg2

    def sparkle_demand_2(self):
        self.msg2 = 'cosmoguirlande,sparkle'
        self.newServer2.to_send = self.msg2

    def pulse_demand_2(self):
        self.msg2 = 'cosmoguirlande,pulse'   
        self.newServer2.to_send = self.msg2

    def solid_demand_2(self):
        self.msg2 = 'cosmoguirlande,solid'
        self.newServer2.to_send = self.msg2

    def colorcycle_demand_2(self):
        self.msg2 = 'cosmoguirlande,colorcycle'
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

    def strombo_demand_3(self):
       self.msg3 = 'cosmoguirlande,strombo'
       self.newServer3.to_send = self.msg3
    
    def chase_demand_3(self):
       self.msg3 = 'cosmoguirlande,chase'
       self.newServer3.to_send = self.msg3              
    
    def comet_demand_3(self):
       self.msg3 = 'cosmoguirlande,comet'
       self.newServer3.to_send = self.msg3
    
    def sparkle_demand_3(self):
       self.msg3 = 'cosmoguirlande,sparkle'
       self.newServer3.to_send = self.msg3
    
    def pulse_demand_3(self):
       self.msg3 = 'cosmoguirlande,pulse'
       self.newServer3.to_send = self.msg3
    
    def solid_demand_3(self):
       self.msg3 = 'cosmoguirlande,solid'
       self.newServer3.to_send = self.msg3
    
    def colorcycle_demand_3(self):
       self.msg3 = 'cosmoguirlande,colorcycle'
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

    #########################################################################################################Strip 4

    def on_click_strombo_4_frequency(self):
        Strombo_frequency = self.textbox_port.text()
        QMessageBox.question(self, 'Message - pythonspot.com', "You typed: " + Strombo_frequency, QMessageBox.Ok,
                             QMessageBox.Ok)
        self.textbox.setText("")

    def blackout_demand_4(self):
        self.msg4 = 'cosmoguirlande,blackout'
        self.newServer4.to_send = self.msg4

    def rainbow_demand_4(self):
        self.msg4 = 'cosmoguirlande,rainbow'
        self.newServer4.to_send = self.msg4

    def strombo_demand_4(self):
        self.msg4 = 'cosmoguirlande,strombo'
        self.newServer4.to_send = self.msg4

    def theaterChase_demand_4(self):
        self.msg4 = 'cosmoguirlande,theaterChase'
        self.newServer4.to_send = self.msg4

    def theaterChaseRainbow_demand_4(self):
        self.msg4 = 'cosmoguirlande,theaterChaseRainbow'
        self.newServer4.to_send = self.msg4

    def multiColorWipe_demand_4(self):
        self.msg4 = 'cosmoguirlande,multiColorWipe'
        self.newServer4.to_send = self.msg4

    def sync_demand_4(self):
        self.msg4 = 'cosmoguirlande,sync'
        self.newServer4.to_send = self.msg4

    def strombo_demand_4(self):
        self.msg4 = 'cosmoguirlande,strombo'
        self.newServer4.to_send = self.msg4

    def chase_demand_4(self):
        self.msg4 = 'cosmoguirlande,chase'
        self.newServer4.to_send = self.msg4

    def comet_demand_4(self):
        self.msg4 = 'cosmoguirlande,comet'
        self.newServer4.to_send = self.msg4

    def sparkle_demand_4(self):
        self.msg4 = 'cosmoguirlande,sparkle'
        self.newServer4.to_send = self.msg4

    def pulse_demand_4(self):
        self.msg4 = 'cosmoguirlande,pulse'
        self.newServer4.to_send = self.msg4

    def solid_demand_4(self):
        self.msg4 = 'cosmoguirlande,solid'
        self.newServer4.to_send = self.msg4

    def colorcycle_demand_4(self):
        self.msg4 = 'cosmoguirlande,colorcycle'
        self.newServer4.to_send = self.msg4

    # Slider Buttons functions
    def slider_R4(self, R4):
        self.msg4 = 'cosmoguirlande,R,' + str((R4))
        self.newServer4.to_send = self.msg4

    def slider_G4(self, G4):
        self.msg4 = 'cosmoguirlande,G,' + str((G4))
        self.newServer4.to_send = self.msg4

    def slider_B4(self, B4):
        self.msg4 = 'cosmoguirlande,B,' + str((B4))
        self.newServer4.to_send = self.msg4

    def slider_W4(self, W4):
        self.msg4 = 'cosmoguirlande,W,' + str((W4))
        self.newServer4.to_send = self.msg4

    #########################################################################################################Strip 5

    def on_click_strombo_5_frequency(self):
        Strombo_frequency = self.textbox_port.text()
        QMessageBox.question(self, 'Message - pythonspot.com', "You typed: " + Strombo_frequency, QMessageBox.Ok,
                             QMessageBox.Ok)
        self.textbox.setText("")

    def blackout_demand_5(self):
        self.msg5 = 'cosmoguirlande,blackout'
        self.newServer5.to_send = self.msg5

    def rainbow_demand_5(self):
        self.msg5 = 'cosmoguirlande,rainbow'
        self.newServer5.to_send = self.msg5

    def strombo_demand_5(self):
        self.msg5 = 'cosmoguirlande,strombo'
        self.newServer5.to_send = self.msg5

    def theaterChase_demand_5(self):
        self.msg5 = 'cosmoguirlande,theaterChase'
        self.newServer5.to_send = self.msg5

    def theaterChaseRainbow_demand_5(self):
        self.msg5 = 'cosmoguirlande,theaterChaseRainbow'
        self.newServer5.to_send = self.msg5

    def multiColorWipe_demand_5(self):
        self.msg5 = 'cosmoguirlande,multiColorWipe'
        self.newServer5.to_send = self.msg5

    def sync_demand_5(self):
        self.msg5 = 'cosmoguirlande,sync'
        self.newServer5.to_send = self.msg5

    def strombo_demand_5(self):
        self.msg5 = 'cosmoguirlande,strombo'
        self.newServer5.to_send = self.msg5

    def chase_demand_5(self):
        self.msg5 = 'cosmoguirlande,chase'
        self.newServer5.to_send = self.msg5

    def comet_demand_5(self):
        self.msg5 = 'cosmoguirlande,comet'
        self.newServer5.to_send = self.msg5

    def sparkle_demand_5(self):
        self.msg5 = 'cosmoguirlande,sparkle'
        self.newServer5.to_send = self.msg5

    def pulse_demand_5(self):
        self.msg5 = 'cosmoguirlande,pulse'
        self.newServer5.to_send = self.msg5

    def solid_demand_5(self):
        self.msg5 = 'cosmoguirlande,solid'
        self.newServer5.to_send = self.msg5

    def colorcycle_demand_5(self):
        self.msg5 = 'cosmoguirlande,colorcycle'
        self.newServer5.to_send = self.msg5

    # Slider Buttons functions
    def slider_R5(self, R5):
        self.msg5 = 'cosmoguirlande,R,' + str((R5))
        self.newServer5.to_send = self.msg5

    def slider_G5(self, G5):
        self.msg5 = 'cosmoguirlande,G,' + str((G5))
        self.newServer5.to_send = self.msg5

    def slider_B5(self, B5):
        self.msg5 = 'cosmoguirlande,B,' + str((B5))
        self.newServer5.to_send = self.msg3

    def slider_W5(self, W5):
        self.msg5 = 'cosmoguirlande,W,' + str((W5))
        self.newServer5.to_send = self.msg5

    #########################################################################################################Strip 6

    def on_click_strombo_6_frequency(self):
        Strombo_frequency = self.textbox_port.text()
        QMessageBox.question(self, 'Message - pythonspot.com', "You typed: " + Strombo_frequency, QMessageBox.Ok,
                             QMessageBox.Ok)
        self.textbox.setText("")

    def blackout_demand_6(self):
        self.msg6 = 'cosmoguirlande,blackout'
        self.newServer6.to_send = self.msg6

    def rainbow_demand_6(self):
        self.msg6 = 'cosmoguirlande,rainbow'
        self.newServer6.to_send = self.msg6

    def strombo_demand_6(self):
        self.msg6 = 'cosmoguirlande,strombo'
        self.newServer6.to_send = self.msg6

    def theaterChase_demand_6(self):
        self.msg6 = 'cosmoguirlande,theaterChase'
        self.newServer6.to_send = self.msg6

    def theaterChaseRainbow_demand_6(self):
        self.msg6 = 'cosmoguirlande,theaterChaseRainbow'
        self.newServer6.to_send = self.msg6

    def multiColorWipe_demand_6(self):
        self.msg6 = 'cosmoguirlande,multiColorWipe'
        self.newServer6.to_send = self.msg6

    def sync_demand_6(self):
        self.msg6 = 'cosmoguirlande,sync'
        self.newServer6.to_send = self.msg6

    def strombo_demand_6(self):
        self.msg6 = 'cosmoguirlande,strombo'
        self.newServer6.to_send = self.msg6

    def chase_demand_6(self):
        self.msg6 = 'cosmoguirlande,chase'
        self.newServer6.to_send = self.msg6

    def comet_demand_6(self):
        self.msg6 = 'cosmoguirlande,comet'
        self.newServer6.to_send = self.msg6

    def sparkle_demand_6(self):
        self.msg6 = 'cosmoguirlande,sparkle'
        self.newServer6.to_send = self.msg6

    def pulse_demand_6(self):
        self.msg6 = 'cosmoguirlande,pulse'
        self.newServer6.to_send = self.msg6

    def solid_demand_6(self):
        self.msg6 = 'cosmoguirlande,solid'
        self.newServer6.to_send = self.msg6

    def colorcycle_demand_6(self):
        self.msg6 = 'cosmoguirlande,colorcycle'
        self.newServer6.to_send = self.msg6

    # Slider Buttons functions
    def slider_R6(self, R6):
        self.msg6 = 'cosmoguirlande,R,' + str((R6))
        self.newServer6.to_send = self.msg6

    def slider_G6(self, G6):
        self.msg6 = 'cosmoguirlande,G,' + str((G6))
        self.newServer6.to_send = self.msg6

    def slider_B6(self, B6):
        self.msg6 = 'cosmoguirlande,B,' + str((B6))
        self.newServer6.to_send = self.msg6

    def slider_W6(self, W6):
        self.msg6 = 'cosmoguirlande,W,' + str((W6))
        self.newServer6.to_send = self.msg6


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWin()
    win.show()
    sys.exit(app.exec_())