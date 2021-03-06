import socket
import select
import threading
import Server
import time
from datetime import datetime
# Simple test for NeoPixels on Raspberry Pi
import argparse
import time
import board
import neopixel
import os
import threading
import socket
from adafruit_led_animation.animation.comet import Comet # sudo pip3 install adafruit-circuitpython-led-animation
from adafruit_led_animation.animation.chase import Chase
from adafruit_led_animation.animation.pulse import Pulse
from adafruit_led_animation.animation.sparkle import Sparkle
from adafruit_led_animation.animation.solid import Solid
from adafruit_led_animation.animation.colorcycle import ColorCycle
from adafruit_led_animation.animation.blink import Blink
from adafruit_led_animation.animation.sparklepulse import SparklePulse
from adafruit_led_animation.animation.rainbow import Rainbow
from adafruit_led_animation.animation.customcolorchase import CustomColorChase
from adafruit_led_animation.animation.rainbowchase import RainbowChase
from adafruit_led_animation.animation.rainbowsparkle import RainbowSparkle
from adafruit_led_animation.animation.rainbowcomet import RainbowComet
from adafruit_led_animation.sequence import AnimationSequence
from adafruit_led_animation.color import AMBER, AQUA, BLACK,BLUE,CYAN,GOLD,GREEN
from adafruit_led_animation.color import JADE,MAGENTA,OLD_LACE,ORANGE,PINK,PURPLE,RAINBOW,RED,RGBW_WHITE_RGB
from adafruit_led_animation.color import RGBW_WHITE_RGBW,RGBW_WHITE_W,TEAL,WHITE,YELLOW
#Recorder for beat detection
#from recorder import *
from Cosmo_guirlande_rpi import Cosmo_guirlande_rpi
import sys
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QLabel, QApplication, QWidget, QDesktopWidget, QCheckBox, QMessageBox, QSlider, QPushButton, QInputDialog, QLineEdit, QComboBox

############################################
# GUI
############################################
class MainWin(QWidget):

    def __init__(self, cosmo_guirlande, pixels):
        #Init parent
        super().__init__()

        #Window configuration
        self.setFixedSize(740, 720)
        self.setWindowTitle("Cosmo Guirlandes RPi GUI")
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topRight())
        self.cosmo_guirlande = cosmo_guirlande
        self.pixels = pixels

        #Start GUI configuration
        self.initUI()
        #self.cosmo_guirlande.run()

    def initUI(self):
        #########################################################################################################Strip 1
        #Entree adresse IP
        # Create textbox
        self.textbox_IP = QLineEdit(self)
        self.textbox_IP.setGeometry(10, 10, 50, 20)
        # Create a button in the window
        self.button_IP= QPushButton('VNC', self)
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
        self.button_strombo= QPushButton('Manual control', self)
        self.button_strombo.setGeometry(150, 450, 100, 20)
        # connect button to function on_click
        self.button_strombo.clicked.connect(self.on_click_manual_control)


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

        # --------------------------------------------------------------------

        # Bouton Dancing Pi Sroll 2
        self.button_dancingPiScroll_2 = QPushButton('dancingPiSroll', self)
        self.button_dancingPiScroll_2.setToolTip('dancingPiSroll')
        self.button_dancingPiScroll_2.setGeometry(310, 510, 100, 25)
        self.button_dancingPiScroll_2.clicked.connect(self.dancingPiScroll_demand_1)

        # Bouton stop_Dancing Pi Sroll 2
        self.button_stop_dancingPiScroll_2 = QPushButton('stop_dancingPiSroll', self)
        self.button_stop_dancingPiScroll_2.setToolTip('stop_dancingPiSroll')
        self.button_stop_dancingPiScroll_2.setGeometry(410, 510, 100, 25)
        self.button_stop_dancingPiScroll_2.clicked.connect(self.stop_dancingPiScroll_demand_1)
        # --------------------------------------------------------------------

        # Bouton Dancing Pi Spectrum 2
        self.button_dancingPiSpectrum_2 = QPushButton('dancingPiSpectrum', self)
        self.button_dancingPiSpectrum_2.setToolTip('dancingPiSpectrum')
        self.button_dancingPiSpectrum_2.setGeometry(310, 540, 100, 25)
        self.button_dancingPiSpectrum_2.clicked.connect(self.dancingPiSpectrum_demand_1)

        # Bouton stop_Dancing Pi Spectrum 2
        self.button_stop_dancingPiSpectrum_2 = QPushButton('stop_dancingPiSpectrum', self)
        self.button_stop_dancingPiSpectrum_2.setToolTip('stop_dancingPiSpectrum')
        self.button_stop_dancingPiSpectrum_2.setGeometry(410, 540, 100, 25)
        self.button_stop_dancingPiSpectrum_2.clicked.connect(self.stop_dancingPiSpectrum_demand_1)
        # --------------------------------------------------------------------

        # Bouton Dancing Pi Energy 2
        self.button_dancingPiEnergy_2 = QPushButton('dancingPiEnergy', self)
        self.button_dancingPiEnergy_2.setToolTip('dancingPiEnergy')
        self.button_dancingPiEnergy_2.setGeometry(310, 570, 100, 25)
        self.button_dancingPiEnergy_2.clicked.connect(self.dancingPiEnergy_demand_1)

        # Bouton stop_Dancing Pi Energy 2
        self.button_stop_dancingPiEnergy_2 = QPushButton('stop_dancingPiEnergy', self)
        self.button_stop_dancingPiEnergy_2.setToolTip('stop_dancingPiEnergy')
        self.button_stop_dancingPiEnergy_2.setGeometry(410, 570, 100, 25)
        self.button_stop_dancingPiEnergy_2.clicked.connect(self.stop_dancingPiEnergy_demand_1)
        # --------------------------------------------------------------------

        # Bouton Cosmo Ball 2
        self.button_cosmoBall_2 = QPushButton('cosmoBall', self)
        self.button_cosmoBall_2.setToolTip('cosmoBall')
        self.button_cosmoBall_2.setGeometry(310, 600, 100, 25)
        # self.button_dancingPi.clicked.connect(self.cosmoBall_demand_2)

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


    def on_click_manual_control(self):
        self.cosmo_guirlande.controle_manuel = not(self.cosmo_guirlande.controle_manuel)

    def restart_demand(self):
        self.cosmo_guirlande.msg1 = 'cosmoguirlande,restart'

    def strombo_demand(self):
        self.cosmo_guirlande.stromboscope(self.cosmo_guirlande.color1, 0.05)
        time.sleep(0.3)

    def color1_change_demand1(self):
        if self.type_color11.currentText() == 'AMBER':
            self.cosmo_guirlande.changeColor1String(AMBER)
        elif self.type_color11.currentText() == 'AQUA':
            self.cosmo_guirlande.changeColor1String(AQUA)
        elif self.type_color11.currentText() == 'YELLOW':
            self.cosmo_guirlande.changeColor1String(YELLOW)
        elif self.type_color11.currentText() == 'WHITE':
            self.cosmo_guirlande.changeColor1String(WHITE)
        elif self.type_color11.currentText() == 'TEAL':
            self.cosmo_guirlande.changeColor1String(TEAL)
        elif self.type_color11.currentText() == 'RGBW_WHITE_W':
            self.cosmo_guirlande.changeColor1String(RGBW_WHITE_W)
        elif self.type_color11.currentText() == 'RGBW_WHITE_RGBW':
            self.cosmo_guirlande.changeColor1String(RGBW_WHITE_RGBW)
        elif self.type_color11.currentText() == 'RGBW_WHITE_RGB':
            self.cosmo_guirlande.changeColor1String(RGBW_WHITE_RGB)
        elif self.type_color11.currentText() == 'RED':
            self.cosmo_guirlande.changeColor1String(RED)
        elif self.type_color11.currentText() == 'PURPLE':
            self.cosmo_guirlande.changeColor1String(PURPLE)
        elif self.type_color11.currentText() == 'PINK':
            self.cosmo_guirlande.changeColor1String(PINK)
        elif self.type_color11.currentText() == 'ORANGE':
            self.cosmo_guirlande.changeColor1String(ORANGE)
        elif self.type_color11.currentText() == 'OLD_LACE':
            self.cosmo_guirlande.changeColor1String(OLD_LACE)
        elif self.type_color11.currentText() == 'MAGENTA':
            self.cosmo_guirlande.changeColor1String(MAGENTA)
        elif self.type_color11.currentText() == 'JADE':
            self.cosmo_guirlande.changeColor1String(JADE)
        elif self.type_color11.currentText() == 'GREEN':
            self.cosmo_guirlande.changeColor1String(GREEN)
        elif self.type_color11.currentText() == 'GOLD':
            self.cosmo_guirlande.changeColor1String(GOLD)
        elif self.type_color11.currentText() == 'CYAN':
            self.cosmo_guirlande.changeColor1String(CYAN)
        elif self.type_color11.currentText() == 'BLUE':
            self.cosmo_guirlande.changeColor1String(BLUE)
        elif self.type_color11.currentText() == 'BLACK':
            self.cosmo_guirlande.changeColor1String(BLACK)

    def color2_change_demand1(self):
        if self.type_color21.currentText() == 'AMBER':
            self.cosmo_guirlande.changeColor2String(AMBER)
        elif self.type_color21.currentText() == 'AQUA':
            self.cosmo_guirlande.changeColor2String(AQUA)
        elif self.type_color21.currentText() == 'YELLOW':
            self.cosmo_guirlande.changeColor2String(YELLOW)
        elif self.type_color21.currentText() == 'WHITE':
            self.cosmo_guirlande.changeColor2String(WHITE)
        elif self.type_color21.currentText() == 'TEAL':
            self.cosmo_guirlande.changeColor2String(TEAL)
        elif self.type_color21.currentText() == 'RGBW_WHITE_W':
            self.cosmo_guirlande.changeColor2String(RGBW_WHITE_W)
        elif self.type_color21.currentText() == 'RGBW_WHITE_RGBW':
            self.cosmo_guirlande.changeColor2String(RGBW_WHITE_RGBW)
        elif self.type_color21.currentText() == 'RGBW_WHITE_RGB':
            self.cosmo_guirlande.changeColor2String(RGBW_WHITE_RGB)
        elif self.type_color21.currentText() == 'RED':
            self.cosmo_guirlande.changeColor2String(RED)
        elif self.type_color21.currentText() == 'PURPLE':
            self.cosmo_guirlande.changeColor2String(PURPLE)
        elif self.type_color21.currentText() == 'PINK':
            self.cosmo_guirlande.changeColor2String(PINK)
        elif self.type_color21.currentText() == 'ORANGE':
            self.cosmo_guirlande.changeColor2String(ORANGE)
        elif self.type_color21.currentText() == 'OLD_LACE':
            self.cosmo_guirlande.changeColor2String(OLD_LACE)
        elif self.type_color21.currentText() == 'MAGENTA':
            self.cosmo_guirlande.changeColor2String(MAGENTA)
        elif self.type_color21.currentText() == 'JADE':
            self.cosmo_guirlande.changeColor2String(JADE)
        elif self.type_color21.currentText() == 'GREEN':
            self.cosmo_guirlande.changeColor2String(GREEN)
        elif self.type_color21.currentText() == 'GOLD':
            self.cosmo_guirlande.changeColor2String(GOLD)
        elif self.type_color21.currentText() == 'CYAN':
            self.cosmo_guirlande.changeColor2String(CYAN)
        elif self.type_color21.currentText() == 'BLUE':
            self.cosmo_guirlande.changeColor2String(BLUE)
        elif self.type_color21.currentText() == 'BLACK':
            self.cosmo_guirlande.changeColor2String(BLACK)

    def blackout_demand(self):
        self.cosmo_guirlande.blackout()

    def rainbow_demand(self):
        for j in range(2):
            self.cosmo_guirlande.rainbow_cycle(0.01)

    def strombo_demand(self):
        self.cosmo_guirlande.stromboscope(self.cosmo_guirlande.color1, 0.05)
        time.sleep(0.3)

    def chase_demand_1(self):
        self.cosmo_guirlande.chase()

    def comet_demand_1(self):
        self.cosmo_guirlande.comet()

    def sparkle_demand_1(self):
        self.cosmo_guirlande.sparkle()

    def pulse_demand_1(self):
        self.cosmo_guirlande.pulse()

    def solid_demand_1(self):
        self.cosmo_guirlande.solid()
        time.sleep(0.5)

    def colorcycle_demand_1(self):
        self.cosmo_guirlande.colorcycle()

    def dancingPiScroll_demand_1(self):
        self.cosmo_guirlande.blackout()
        self.cosmo_guirlande.dancingPiScroll()

    def dancingPiEnergy_demand_1(self):
        self.cosmo_guirlande.blackout()
        self.cosmo_guirlande.dancingPiEnergy()

    def dancingPiSpectrum_demand_1(self):
        self.cosmo_guirlande.blackout()
        self.cosmo_guirlande.dancingPiSpectrum()

    def stop_dancingPiEnergy_demand_1(self):
        self.cosmo_guirlande.stop_dancingPiScroll()

    def stop_dancingPiSpectrum_demand_1(self):
        self.cosmo_guirlande.stop_dancingPiSpectrum()

    def stop_dancingPiScroll_demand_1(self):
        self.cosmo_guirlande.changeColor(self.sl_R1.value(), self.sl_G1.value(), self.sl_B1.value(), self.sl_W1.value())

    # Slider Buttons functions
    def slider_R1(self):
        self.cosmo_guirlande.changeColor(self.sl_R1.value(), self.sl_G1.value(), self.sl_B1.value(), self.sl_W1.value())
        time.sleep(0.5)

    def slider_G1(self):
        self.cosmo_guirlande.changeColor(self.sl_R1.value(), self.sl_G1.value(), self.sl_B1.value(), self.sl_W1.value())
        time.sleep(0.5)

    def slider_B1(self):
        self.cosmo_guirlande.changeColor(self.sl_R1.value(), self.sl_G1.value(), self.sl_B1.value(), self.sl_W1.value())
        time.sleep(0.5)

    def slider_W1(self):
        self.cosmo_guirlande.changeColor(self.sl_R1.value(), self.sl_G1.value(), self.sl_B1.value(), self.sl_W1.value())
        time.sleep(0.5)

    def on_click_ip(self):
        self.IPValue = self.textbox_IP.text()

    def on_click_port(self):
        PortValue = self.textbox_port.text()

    def on_click_strombo_frequency(self):
        Strombo_frequency = self.textbox_port.text()


if __name__ == '__main__':
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    parser.add_argument('guirlande_number', metavar='guirlande_number', type=int, help='Cosmo Guirlande NUmber')
    parser.add_argument('num_pixel', metavar='num_pixel', type=int, help='Number of pixel')
    parser.add_argument('server_tcp_ip', metavar='server_tcp_ip', type=str, help='Server IP')
    parser.add_argument('tcp_port', metavar='tcp_port', type=int, help='Tcp Port')
    parser.add_argument('buffer_size', metavar='buffer_size', type=int, help='Buffer Size')
    parser.add_argument('RGB', metavar='RGB', type=str, help='RGB or RGBW Size')

    args = parser.parse_args()

    # Configuration des LED
    if args.RGB.startswith("RGBW"):
        pixels = neopixel.NeoPixel(
            board.D18, args.num_pixel, brightness=0.99, auto_write=False, pixel_order=neopixel.GRBW
        )

    elif args.RGB.startswith("RGB"):
        pixels = neopixel.NeoPixel(
            board.D18, args.num_pixel, brightness=0.99, auto_write=False, pixel_order=neopixel.GRB
        )

    print('Press Ctrl-C to quit.')

    # Run ex: sudo python3 Desktop/Cosmo_guirlande_rpi.py 1 30 192.168.0.17 50001 1024 RGB
    # Run ex: sudo python3 gui_rpi.py 3 30 192.168.43.144 50003 1024 RGBW

    cosmo_guirlande = Cosmo_guirlande_rpi(pixels, args.guirlande_number, args.num_pixel, args.server_tcp_ip, args.tcp_port, args.buffer_size , args.RGB)

    cosmo_guirlande.start()
    app = QApplication(sys.argv)
    win = MainWin(cosmo_guirlande, pixels)
    win.show()
    sys.exit(app.exec_())


