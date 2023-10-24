import socket
import select
import threading
import os
import Server
import time
from datetime import datetime
import sys
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QLabel, QApplication, QWidget, QDesktopWidget, QCheckBox, QMessageBox, QSlider, QPushButton, QInputDialog, QLineEdit, QComboBox
import paramiko
import subprocess
import paho.mqtt.client as mqtt
import json
from RPi_mqtt_socket import RPi_mqtt_socket

#Load config files with IP, port & LED number
conf_file = open('IP_configuration.json')
strip_configuration = json.load(conf_file)

#print strip configuration file
'''for i in strip_configuration['guirlande']:
    print(i) '''                  

############################################
# GUI
############################################
class VNC_Window(threading.Thread):
    def __init__(self, IP):
        threading.Thread.__init__(self)
        self.IP = IP

    def run(self):
        os.system('cmd /k "vncviewer.exe" ' + str(self.IP))
        '''except :
            pass'''

class MainWin(QWidget):
    h_name = socket.gethostname()
    IP_addres = socket.gethostbyname(h_name)

    #keep IP as attribute
    device = []
    #-----------------------------------------------------Create a list of MQTT client
    
    '''JSON model    
        "guirlande": [
        {
            "name": "cosmoguirlande1",
            "IP": "192.168.0.50",
            "port": 50001,
            "LED_number": 144,
            "color": "RGBW"
        }'''

    i = 0
    j = 0

    for elt in strip_configuration["guirlande"]:
        #get IPs from JSON
        print("IP : ", elt["IP"])
        '''print(elt)
        #get PORT from JSON
        print("port : ", elt["port"])        
        #get LED number from JSON
        print("LED_number : ", elt["LED_number"])
        #get color from JSON
        print("color : ", elt["color"])'''
        objs = [mqtt.Client() for i in range(len(strip_configuration['guirlande']))]

        #get mac address to configure RPis
        

    #for i in range(len(strip_configuration['guirlande'])):
        try:
            objs[i].connect(elt["IP"],1883,60)
            print("publish blackout")
            device.append(elt["IP"])
            objs[i].publish('test1', "cosmoguirlande,blackout")
                        
            
        except:
            print("could not connect to :  ", elt["IP"])
            #====================================================================test
            print("strip_configuration['guirlande'] de j ", strip_configuration["guirlande"][j])
            print("elt['IP']", elt["IP"])
            #del strip_configuration["guirlande"][i]
            objs.remove(objs[i])
            try:
                device.remove(elt["IP"])
            except ValueError:
                pass
            
            #====================================================================fin test
        
        i = i+1
        j = j+1

        for elt in strip_configuration["guirlande"]:
            print(elt)

        for i, elt in enumerate(objs):
            print("À l'indice {} se trouve {}.".format(i, elt))

        for i, elt in enumerate(device):
            print("À l'indice {} se trouve {}.".format(i, elt))

    IPValue = ""
    IPValue_2 = ""
    IPValue_3 = ""
    IPValue_4 = ""
    IPValue_5 = ""
    IPValue_6 = ""
    IPValue_7 = ""


    #Create message to communicate with sensors
    msg1 = ''
    msg2 = ''
    msg3 = ''
    msg4 = ''
    msg5 = ''
    msg6 = ''
    msg7 = ''

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
        self.textbox_IP.setText('192.168.0.1')
        self.textbox_IP.setGeometry(10, 10, 50, 20)
        # Create a button in the window
        self.button_IP= QPushButton('VNC', self)
        self.button_IP.setGeometry(60, 10, 50, 20)
        # connect button to function on_click
        self.button_IP.clicked.connect(self.on_click_ip)

        #Entree Port
        # Create textbox
        self.textbox_port = QLineEdit(self)
        self.textbox_port.setText('50001')
        self.textbox_port.setGeometry(10, 60, 50, 20)
        # Create a button in the window
        self.button_port = QPushButton('Port', self)
        self.button_port.setGeometry(60, 60, 50, 20)
        # connect button to function on_click
        self.button_port.clicked.connect(self.on_click_port)

        #Checkbox de controle manuel
        self.cb_sync = QCheckBox('Manual Control', self)
        self.cb_sync.setToolTip('Click if you wanna manual control ')
        self.cb_sync.stateChanged.connect(self.manual_demand_1)
        self.cb_sync.setGeometry(10, 90, 300, 25)

        #Couleur 1
        self.type_color11 = QComboBox(self)
        self.type_color11.setGeometry(10, 110, 100, 20)
        self.type_color11.addItems(["AMBER","AQUA","BLACK","BLUE", "CYAN","GOLD","GREEN","JADE","MAGENTA","OLD_LACE"
                                       ,"ORANGE", "PINK","PURPLE","RAINBOW","RED",
                                    "RGBW_WHITE_RGB" ,"RGBW_WHITE_RGBW","RGBW_WHITE_W", "TEAL", "WHITE","YELLOW" ])
        self.type_color11.currentIndexChanged.connect(self.color1_change_demand11)

        #Couleur 2
        self.type_color21 = QComboBox(self)
        self.type_color21.setGeometry(60, 110, 100, 20)
        self.type_color21.addItems(["AMBER","AQUA","BLACK","BLUE", "CYAN","GOLD","GREEN","JADE","MAGENTA","OLD_LACE"
                                       ,"ORANGE", "PINK","PURPLE","RAINBOW","RED",
                                    "RGBW_WHITE_RGB" ,"RGBW_WHITE_RGBW","RGBW_WHITE_W", "TEAL", "WHITE","YELLOW" ])
        self.type_color21.currentIndexChanged.connect(self.color2_change_demand12)

        #Bouton restart_demand
        self.button_restart_1 = QPushButton('restart', self)
        self.button_restart_1.setToolTip('button_restart_1')
        self.button_restart_1.setGeometry(10, 140, 100, 25)
        self.button_restart_1.clicked.connect(self.restart_demand)

        #Bouton git_pull_demand
        self.button_git_1 = QPushButton('git pull', self)
        self.button_git_1.setToolTip('button_git_1')
        self.button_git_1.setGeometry(110, 140, 100, 25)
        self.button_git_1.clicked.connect(self.git_pull_demand)

        #Entree Frequence Strombo
        # Create textbox
        self.textbox_strombo = QLineEdit(self)
        self.textbox_strombo.setText('0.1')

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
        self.textbox_chase_speed.setText('0.1')
        self.textbox_chase_speed.setGeometry(110, 540, 50, 20)
        # Create a button in the window
        self.button_chase_speed= QPushButton('speed', self)
        self.button_chase_speed.setGeometry(160, 540, 50, 20)
        # connect button to function on_click
        self.button_chase_speed.clicked.connect(self.on_click_ip)

        #Entree chase param size
        # Create textbox
        self.textbox_chase_size= QLineEdit(self)
        self.textbox_chase_size.setText('5')
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
        self.textbox_comet_speed.setText('0.1')
        self.textbox_comet_speed.setGeometry(110, 570, 50, 20)
        # Create a button in the window
        self.button_comet_speed= QPushButton('speed', self)
        self.button_comet_speed.setGeometry(160, 570, 50, 20)
        # connect button to function on_click
        self.button_comet_speed.clicked.connect(self.on_click_ip)

        #Entree comet param tail
        # Create textbox
        self.textbox_comet_tail= QLineEdit(self)
        self.textbox_comet_tail.setText('5')
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
        self.textbox_pulse_speed.setText('0.1')

        self.textbox_pulse_speed.setGeometry(110, 600, 50, 20)
        # Create a button in the window
        self.button_pulse_speed= QPushButton('speed', self)
        self.button_pulse_speed.setGeometry(160, 600, 50, 20)
        # connect button to function on_click
        self.button_pulse_speed.clicked.connect(self.on_click_ip)

        #Entree pulse param period
        # Create textbox
        self.textbox_pulse_period= QLineEdit(self)
        self.textbox_pulse_period.setText('0.2')

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
        self.textbox_sparkle_speed.setText('0.1')

        self.textbox_sparkle_speed.setGeometry(110, 630, 50, 20)
        # Create a button in the window
        self.button_sparkle_speed= QPushButton('speed', self)
        self.button_sparkle_speed.setGeometry(160, 630, 50, 20)
        # connect button to function on_click
        self.button_sparkle_speed.clicked.connect(self.on_click_ip)

        #Entree sparkle param num_sparkles
        # Create textbox
        self.textbox_sparkle_num_sparkles= QLineEdit(self)
        self.textbox_sparkle_num_sparkles.setText('5')

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
        self.textbox_color_cycle_speed.setText('0.1')

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
        self.button_stop_dancingPiScroll.clicked.connect(self.stop_dancingPiEnergy_demand_1)
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
        self.button_stop_dancingPiSpectrum.clicked.connect(self.stop_dancingPiEnergy_demand_1)
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

        # Bouton colorAll2Color - repere dancingPiScroll_demand_1
        self.button_colorAll2Color = QPushButton('colorAll2Color', self)
        self.button_colorAll2Color.setToolTip('colorAll2Color')
        self.button_colorAll2Color.setGeometry(10,840, 100, 25)
        self.button_colorAll2Color.clicked.connect(self.colorAll2Color_demand_1)

        # Bouton FadeInOut
        self.button_FadeInOut = QPushButton('FadeInOut', self)
        self.button_FadeInOut.setToolTip('FadeInOut')
        self.button_FadeInOut.setGeometry(10,870, 100, 25)
        self.button_FadeInOut.clicked.connect(self.FadeInOut_demand_1)

         # Bouton Strobe
        self.button_Strobe = QPushButton('Strobe', self)
        self.button_Strobe.setToolTip('Strobe')
        self.button_Strobe.setGeometry(10,900, 100, 25)
        self.button_Strobe.clicked.connect(self.Strobe_demand_1)

        # Bouton HalloweenEyes
        self.button_HalloweenEyes = QPushButton('HalloweenEyes', self)
        self.button_HalloweenEyes.setToolTip('HalloweenEyes')
        self.button_HalloweenEyes.setGeometry(10,930, 100, 25)
        self.button_HalloweenEyes.clicked.connect(self.HalloweenEyes_demand_1)

        # Bouton CylonBounce
        self.button_CylonBounce = QPushButton('CylonBounce', self)
        self.button_CylonBounce.setToolTip('CylonBounce')
        self.button_CylonBounce.setGeometry(110,840, 100, 25)
        self.button_CylonBounce.clicked.connect(self.CylonBounce_demand_1)

        # Bouton NewKITT
        self.button_NewKITT = QPushButton('NewKITT', self)
        self.button_NewKITT.setToolTip('NewKITT')
        self.button_NewKITT.setGeometry(110,870, 100, 25)
        self.button_NewKITT.clicked.connect(self.NewKITT_demand_1)

        # Bouton Twinkle
        self.button_Twinkle = QPushButton('Twinkle', self)
        self.button_Twinkle.setToolTip('Twinkle')
        self.button_Twinkle.setGeometry(110,900, 100, 25)
        self.button_Twinkle.clicked.connect(self.Twinkle_demand_1)

        # Bouton TwinkleRandom
        self.button_TwinkleRandom = QPushButton('TwinkleRandom', self)
        self.button_TwinkleRandom.setToolTip('TwinkleRandom')
        self.button_TwinkleRandom.setGeometry(110,930, 100, 25)
        self.button_TwinkleRandom.clicked.connect(self.TwinkleRandom_demand_1)

        # Bouton SnowSparkle
        self.button_SnowSparkle = QPushButton('SnowSparkle', self)
        self.button_SnowSparkle.setToolTip('SnowSparkle')
        self.button_SnowSparkle.setGeometry(210,840, 100, 25)
        self.button_SnowSparkle.clicked.connect(self.SnowSparkle_demand_1)

        # Bouton RunningLights
        self.button_RunningLights = QPushButton('RunningLights', self)
        self.button_RunningLights.setToolTip('RunningLights')
        self.button_RunningLights.setGeometry(210,870, 100, 25)
        self.button_RunningLights.clicked.connect(self.RunningLights_demand_1)

        # Bouton colorWipe
        self.button_colorWipe = QPushButton('colorWipe', self)
        self.button_colorWipe.setToolTip('colorWipe')
        self.button_colorWipe.setGeometry(210,900, 100, 25)
        self.button_colorWipe.clicked.connect(self.colorWipe_demand_1)

        # Bouton theaterChaseRainbow
        self.button_theaterChaseRainbow = QPushButton('theaterChaseRainbow', self)
        self.button_theaterChaseRainbow.setToolTip('theaterChaseRainbow')
        self.button_theaterChaseRainbow.setGeometry(210,930, 100, 25)
        self.button_theaterChaseRainbow.clicked.connect(self.theaterChaseRainbow_demand_1)

        # Bouton Fire
        self.button_Fire = QPushButton('Fire', self)
        self.button_Fire.setToolTip('Fire')
        self.button_Fire.setGeometry(310,840, 100, 25)
        self.button_Fire.clicked.connect(self.Fire_demand_1)

        # Bouton FireCustom
        self.button_FireCustom = QPushButton('FireCustom', self)
        self.button_FireCustom.setToolTip('FireCustom')
        self.button_FireCustom.setGeometry(310,870, 100, 25)
        self.button_FireCustom.clicked.connect(self.FireCustom_demand_1)

        # Bouton meteorRain
        self.button_meteorRain = QPushButton('meteorRain', self)
        self.button_meteorRain.setToolTip('meteorRain')
        self.button_meteorRain.setGeometry(310,900, 100, 25)
        self.button_meteorRain.clicked.connect(self.meteorRain_demand_1)

        # Bouton fadeToBlack
        self.button_fadeToBlack = QPushButton('fadeToBlack', self)
        self.button_fadeToBlack.setToolTip('fadeToBlack')
        self.button_fadeToBlack.setGeometry(310,930, 100, 25)
        self.button_fadeToBlack.clicked.connect(self.fadeToBlack_demand_1)

        # Bouton BouncingBalls
        self.button_BouncingBalls = QPushButton('BouncingBalls', self)
        self.button_BouncingBalls.setToolTip('BouncingBalls')
        self.button_BouncingBalls.setGeometry(410,840, 100, 25)
        self.button_BouncingBalls.clicked.connect(self.BouncingBalls_demand_1)

        # Bouton BouncingColoredBalls
        self.button_BouncingColoredBalls = QPushButton('BouncingColoredBalls', self)
        self.button_BouncingColoredBalls.setToolTip('BouncingColoredBalls')
        self.button_BouncingColoredBalls.setGeometry(410,870, 100, 25)
        self.button_BouncingColoredBalls.clicked.connect(self.BouncingColoredBalls_demand_1)
        
        #----------------------------------------------------------------------------------------
        # Bouton Matrix
        self.button_Matrix = QPushButton('Matrix', self)
        self.button_Matrix.setToolTip('Matrix')
        self.button_Matrix.setGeometry(410,900, 100, 25)
        self.button_Matrix.clicked.connect(self.Matrix_demand_1)

        # Bouton Drain
        self.button_Drain = QPushButton('Drain', self)
        self.button_Drain.setToolTip('Drain')
        self.button_Drain.setGeometry(510,840, 100, 25)
        self.button_Drain.clicked.connect(self.Drain_demand_1)
        #----------------------------------------------------------------------------------------
        # Bouton Pancake
        self.button_Pancake = QPushButton('Pancake', self)
        self.button_Pancake.setToolTip('Pancake')
        self.button_Pancake.setGeometry(510,870, 100, 25)
        self.button_Pancake.clicked.connect(self.Pancake_demand_1)

        # Bouton HeartBeat
        self.button_HeartBeat = QPushButton('HeartBeat', self)
        self.button_HeartBeat.setToolTip('HeartBeat')
        self.button_HeartBeat.setGeometry(510,900, 100, 25)
        self.button_HeartBeat.clicked.connect(self.HeartBeat_demand_1)

        #----------------------------------------------------------------------------------------
        # Bouton rainbowGlitter
        self.button_rainbowGlitter = QPushButton('rainbowGlitter', self)
        self.button_rainbowGlitter.setToolTip('rainbowGlitter')
        self.button_rainbowGlitter.setGeometry(610,840, 100, 25)
        self.button_rainbowGlitter.clicked.connect(self.rainbowGlitter_demand_1)

        # Bouton Confetti
        self.button_Confetti = QPushButton('Confetti', self)
        self.button_Confetti.setToolTip('Confetti')
        self.button_Confetti.setGeometry(610,870, 100, 25)
        self.button_Confetti.clicked.connect(self.Confetti_demand_1)

        #----------------------------------------------------------------------------------------
        # Bouton Sinelon
        self.button_Sinelon = QPushButton('Sinelon', self)
        self.button_Sinelon.setToolTip('Sinelon')
        self.button_Sinelon.setGeometry(610,900, 100, 25)
        self.button_Sinelon.clicked.connect(self.Sinelon_demand_1)

        # Bouton BPM
        self.button_BPM = QPushButton('BPM', self)
        self.button_BPM.setToolTip('BPM')
        self.button_BPM.setGeometry(710,840, 100, 25)
        self.button_BPM.clicked.connect(self.BPM_demand_1)

        #----------------------------------------------------------------------------------------

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
        self.textbox_strombo_2.setText('0.1')

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

        # Entree adresse IP
        # Create textbox
        self.textbox_IP_2 = QLineEdit(self)
        self.textbox_IP_2.setText('192.168.0.1')

        self.textbox_IP_2.setGeometry(310, 10, 50, 20)
        # Create a button in the window
        self.button_IP_2 = QPushButton('VNC', self)
        self.button_IP_2.setGeometry(360, 10, 50, 20)
        # connect button to function on_click
        self.button_IP_2.clicked.connect(self.on_click_ip_2)

        # Entree Port
        # Create textbox
        self.textbox_port_2 = QLineEdit(self)
        self.textbox_port_2.setText('52000')

        self.textbox_port_2.setGeometry(310, 60, 50, 20)
        # Create a button in the window
        self.button_port_2 = QPushButton('Port', self)
        self.button_port_2.setGeometry(360, 60, 50, 20)
        # connect button to function on_click
        self.button_port_2.clicked.connect(self.on_click_port_2)

        # Couleur 2
        self.type_color22 = QComboBox(self)
        self.type_color22.setGeometry(320, 110, 100, 20)
        self.type_color22.addItems(
            ["AMBER", "AQUA", "BLACK", "BLUE", "CYAN", "GOLD", "GREEN", "JADE", "MAGENTA", "OLD_LACE"
                , "ORANGE", "PINK", "PURPLE", "RAINBOW", "RED",
             "RGBW_WHITE_RGB", "RGBW_WHITE_RGBW", "RGBW_WHITE_W", "TEAL", "WHITE", "YELLOW"])
        self.type_color22.currentIndexChanged.connect(self.color2_change_demand21)

        # Couleur 2
        self.type_color22 = QComboBox(self)
        self.type_color22.setGeometry(360, 110, 100, 20)
        self.type_color22.addItems(
            ["AMBER", "AQUA", "BLACK", "BLUE", "CYAN", "GOLD", "GREEN", "JADE", "MAGENTA", "OLD_LACE"
                , "ORANGE", "PINK", "PURPLE", "RAINBOW", "RED",
             "RGBW_WHITE_RGB", "RGBW_WHITE_RGBW", "RGBW_WHITE_W", "TEAL", "WHITE", "YELLOW"])
        self.type_color22.currentIndexChanged.connect(self.color2_change_demand22)


        #Bouton effet rainbow 2 Loop
        self.button_rainbow_2 = QPushButton('Rainbow effect', self)
        self.button_rainbow_2.setToolTip('Click if you wanna use rainbow effect')
        self.button_rainbow_2.setGeometry(310, 480, 100, 25)
        self.button_rainbow_2.clicked.connect(self.rainbow_demand_2)


        #--------------------------------------------------------------------

        #Bouton Blackout 2
        self.button_blackout_2 = QPushButton('Blackout', self)
        self.button_blackout_2.setToolTip('Turn off LEDs')
        self.button_blackout_2.setGeometry(310, 510, 100, 25)
        self.button_blackout_2.clicked.connect(self.blackout_demand)
        #--------------------------------------------------------------------
        # Bouton chase 2
        self.button_chase_2 = QPushButton('chase', self)
        self.button_chase_2.setToolTip('chase')
        self.button_chase_2.setGeometry(310, 540, 100, 25)
        self.button_chase_2.clicked.connect(self.chase_demand_2)

        #Entree chase param speed
        # Create textbox
        self.textbox_chase_speed_2= QLineEdit(self)
        self.textbox_chase_speed_2.setText('0.1')

        self.textbox_chase_speed_2.setGeometry(410, 540, 50, 20)
        # Create a button in the window
        self.button_chase_speed_2= QPushButton('speed', self)
        self.button_chase_speed_2.setGeometry(460, 540, 50, 20)
        # connect button to function on_click
        self.button_chase_speed_2.clicked.connect(self.on_click_ip)

        #Entree chase param size
        # Create textbox
        self.textbox_chase_size_2= QLineEdit(self)
        self.textbox_chase_size_2.setText('5')

        self.textbox_chase_size_2.setGeometry(510, 540, 50, 20)
        # Create a button in the window
        self.button_chase_size_2= QPushButton('size', self)
        self.button_chase_size_2.setGeometry(560, 540, 50, 20)
        # connect button to function on_click
        self.button_chase_size_2.clicked.connect(self.on_click_ip)
        #--------------------------------------------------------------------
        #--------------------------------------------------------------------

        # Bouton comet 2
        self.button_comet_2 = QPushButton('comet', self)
        self.button_comet_2.setToolTip('comet')
        self.button_comet_2.setGeometry(310, 570, 100, 25)
        self.button_comet_2.clicked.connect(self.comet_demand_2)

        #Entree comet param speed
        # Create textbox
        self.textbox_comet_speed_2= QLineEdit(self)
        self.textbox_comet_speed_2.setText('0.1')

        self.textbox_comet_speed_2.setGeometry(410, 570, 50, 20)
        # Create a button in the window
        self.button_comet_speed_2= QPushButton('speed', self)
        self.button_comet_speed_2.setGeometry(460, 570, 50, 20)
        # connect button to function on_click
        self.button_comet_speed_2.clicked.connect(self.on_click_ip)

        #Entree comet param tail
        # Create textbox
        self.textbox_comet_tail_2= QLineEdit(self)
        self.textbox_comet_tail_2.setText('5')
        self.textbox_comet_tail_2.setGeometry(510, 570, 50, 20)
        # Create a button in the window
        self.button_comet_tail_2= QPushButton('tail', self)
        self.button_comet_tail_2.setGeometry(560, 570, 50, 20)
        # connect button to function on_click
        self.button_comet_tail_2.clicked.connect(self.on_click_ip)
        #--------------------------------------------------------------------

        # Bouton pulse 2
        self.button_pulse_2 = QPushButton('pulse', self)
        self.button_pulse_2.setToolTip('pulse')
        self.button_pulse_2.setGeometry(310, 600, 100, 25)
        self.button_pulse_2.clicked.connect(self.pulse_demand_2)

        #Entree pulse param speed
        # Create textbox
        self.textbox_pulse_speed_2= QLineEdit(self)
        self.textbox_pulse_speed_2.setText('0.1')
        self.textbox_pulse_speed_2.setGeometry(410, 600, 50, 20)
        # Create a button in the window
        self.button_pulse_speed_2= QPushButton('speed', self)
        self.button_pulse_speed_2.setGeometry(460, 600, 50, 20)
        # connect button to function on_click
        self.button_pulse_speed_2.clicked.connect(self.on_click_ip)

        #Entree pulse param period
        # Create textbox
        self.textbox_pulse_period_2= QLineEdit(self)
        self.textbox_pulse_period_2.setText('1')
        self.textbox_pulse_period_2.setGeometry(510, 600, 50, 20)
        # Create a button in the window
        self.button_pulse_period_2= QPushButton('period', self)
        self.button_pulse_period_2.setGeometry(560, 600, 50, 20)
        # connect button to function on_click
        self.button_pulse_period_2.clicked.connect(self.on_click_ip)
        #--------------------------------------------------------------------

        # Bouton sparkle 2
        self.button_sparkle_2 = QPushButton('sparkle', self)
        self.button_sparkle_2.setToolTip('sparkle')
        self.button_sparkle_2.setGeometry(310, 630, 100, 25)
        self.button_sparkle_2.clicked.connect(self.sparkle_demand_2)

        #Entree sparkle param speed
        # Create textbox
        self.textbox_sparkle_speed_2= QLineEdit(self)
        self.textbox_sparkle_speed_2.setText('0.1')
        self.textbox_sparkle_speed_2.setGeometry(410, 630, 50, 20)
        # Create a button in the window
        self.button_sparkle_speed_2= QPushButton('speed', self)
        self.button_sparkle_speed_2.setGeometry(460, 630, 50, 20)
        # connect button to function on_click
        self.button_sparkle_speed_2.clicked.connect(self.on_click_ip)

        #Entree sparkle param num_sparkles
        # Create textbox
        self.textbox_sparkle_num_sparkles_2= QLineEdit(self)
        self.textbox_sparkle_num_sparkles_2.setText('5')
        self.textbox_sparkle_num_sparkles_2.setGeometry(510, 630, 50, 20)
        # Create a button in the window
        self.button_sparkle_num_sparkles_2= QPushButton('num_sparkles', self)
        self.button_sparkle_num_sparkles_2.setGeometry(560, 630, 50, 20)
        # connect button to function on_click
        self.button_sparkle_num_sparkles_2.clicked.connect(self.on_click_ip)
        #--------------------------------------------------------------------

        # Bouton solid 2
        self.button_solid_2 = QPushButton('solid', self)
        self.button_solid_2.setToolTip('solid')
        self.button_solid_2.setGeometry(310, 660, 100, 25)
        self.button_solid_2.clicked.connect(self.solid_demand_2)
        #--------------------------------------------------------------------

        # Bouton colorcycle 2
        self.button_colorcycle_2 = QPushButton('colorcycle', self)
        self.button_colorcycle_2.setToolTip('colorcycle')
        self.button_colorcycle_2.setGeometry(310, 690, 100, 25)
        self.button_colorcycle_2.clicked.connect(self.colorcycle_demand_2)

        #Entree color_cycle param speed
        # Create textbox
        self.textbox_color_cycle_speed_2= QLineEdit(self)
        self.textbox_color_cycle_speed_2.setText('0.5')
        self.textbox_color_cycle_speed_2.setGeometry(410, 690, 50, 20)
        # Create a button in the window
        self.button_color_cycle_speed_2= QPushButton('speed', self)
        self.button_color_cycle_speed_2.setGeometry(460, 690, 50, 20)
        # connect button to function on_click
        self.button_color_cycle_speed_2.clicked.connect(self.on_click_ip)

        #--------------------------------------------------------------------

        # Bouton Dancing Pi Sroll 2
        self.button_dancingPiScroll_2 = QPushButton('dancingPiSroll', self)
        self.button_dancingPiScroll_2.setToolTip('dancingPiSroll')
        self.button_dancingPiScroll_2.setGeometry(310, 720, 100, 25)
        self.button_dancingPiScroll_2.clicked.connect(self.dancingPiScroll_demand_2)

        # Bouton stop_Dancing Pi Sroll 2
        self.button_stop_dancingPiScroll_2 = QPushButton('stop_dancingPiSroll', self)
        self.button_stop_dancingPiScroll_2.setToolTip('stop_dancingPiSroll')
        self.button_stop_dancingPiScroll_2.setGeometry(410, 720, 100, 25)
        self.button_stop_dancingPiScroll_2.clicked.connect(self.stop_dancingPiScroll_demand_2)
        #--------------------------------------------------------------------

        # Bouton Dancing Pi Spectrum 2
        self.button_dancingPiSpectrum_2 = QPushButton('dancingPiSpectrum', self)
        self.button_dancingPiSpectrum_2.setToolTip('dancingPiSpectrum')
        self.button_dancingPiSpectrum_2.setGeometry(310, 750, 100, 25)
        self.button_dancingPiSpectrum_2.clicked.connect(self.dancingPiSpectrum_demand_2)

        # Bouton stop_Dancing Pi Spectrum 2
        self.button_stop_dancingPiSpectrum_2 = QPushButton('stop_dancingPiSpectrum', self)
        self.button_stop_dancingPiSpectrum_2.setToolTip('stop_dancingPiSpectrum')
        self.button_stop_dancingPiSpectrum_2.setGeometry(410, 750, 100, 25)
        self.button_stop_dancingPiSpectrum_2.clicked.connect(self.stop_dancingPiSpectrum_demand_2)
        #--------------------------------------------------------------------

        # Bouton Dancing Pi Energy 2
        self.button_dancingPiEnergy_2 = QPushButton('dancingPiEnergy', self)
        self.button_dancingPiEnergy_2.setToolTip('dancingPiEnergy')
        self.button_dancingPiEnergy_2.setGeometry(310, 780, 100, 25)
        self.button_dancingPiEnergy_2.clicked.connect(self.dancingPiEnergy_demand_2)

        # Bouton stop_Dancing Pi Energy 2
        self.button_stop_dancingPiEnergy_2 = QPushButton('stop_dancingPiEnergy', self)
        self.button_stop_dancingPiEnergy_2.setToolTip('stop_dancingPiEnergy')
        self.button_stop_dancingPiEnergy_2.setGeometry(410, 780, 100, 25)
        self.button_stop_dancingPiEnergy_2.clicked.connect(self.stop_dancingPiEnergy_demand_2)
        #--------------------------------------------------------------------

        # Bouton Cosmo Ball 2
        self.button_cosmoBall_2 = QPushButton('cosmoBall', self)
        self.button_cosmoBall_2.setToolTip('cosmoBall')
        self.button_cosmoBall_2.setGeometry(310,810, 100, 25)
        #self.button_dancingPi.clicked.connect(self.cosmoBall_demand_2)
        

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

        # Entree adresse IP
        # Create textbox
        self.textbox_IP_3 = QLineEdit(self)
        self.textbox_IP_3.setText('192.168.0.3')
        self.textbox_IP_3.setGeometry(610, 10, 50, 20)
        # Create a button in the window
        self.button_IP_3 = QPushButton('VNC', self)
        self.button_IP_3.setGeometry(660, 10, 50, 20)
        # connect button to function on_click
        self.button_IP_3.clicked.connect(self.on_click_ip_3)

        # Entree Port
        # Create textbox
        self.textbox_port_3 = QLineEdit(self)
        self.textbox_port_3.setText('50003')
        self.textbox_port_3.setGeometry(610, 60, 50, 20)
        # Create a button in the window
        self.button_port_3 = QPushButton('Port', self)
        self.button_port_3.setGeometry(660, 60, 50, 20)
        # connect button to function on_click
        self.button_port_3.clicked.connect(self.on_click_port_3)

        # Couleur 3
        self.type_color31 = QComboBox(self)
        self.type_color31.setGeometry(610, 110, 100, 20)
        self.type_color31.addItems(
            ["AMBER", "AQUA", "BLACK", "BLUE", "CYAN", "GOLD", "GREEN", "JADE", "MAGENTA", "OLD_LACE"
                , "ORANGE", "PINK", "PURPLE", "RAINBOW", "RED",
             "RGBW_WHITE_RGB", "RGBW_WHITE_RGBW", "RGBW_WHITE_W", "TEAL", "WHITE", "YELLOW"])
        self.type_color31.currentIndexChanged.connect(self.color3_change_demand31)

        # Couleur 3
        self.type_color32 = QComboBox(self)
        self.type_color32.setGeometry(660, 110, 100, 20)
        self.type_color32.addItems(
            ["AMBER", "AQUA", "BLACK", "BLUE", "CYAN", "GOLD", "GREEN", "JADE", "MAGENTA", "OLD_LACE"
                , "ORANGE", "PINK", "PURPLE", "RAINBOW", "RED",
             "RGBW_WHITE_RGB", "RGBW_WHITE_RGBW", "RGBW_WHITE_W", "TEAL", "WHITE", "YELLOW"])
        self.type_color32.currentIndexChanged.connect(self.color3_change_demand32)

        #Entree Frequence Strombo 3
        # Create textbox
        self.textbox_strombo_3 = QLineEdit(self)
        self.textbox_strombo_3.setText('0.1')
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

        #--------------------------------------------------------------------
        # Bouton chase 3
        self.button_chase_3 = QPushButton('chase', self)
        self.button_chase_3.setToolTip('chase')
        self.button_chase_3.setGeometry(610, 540, 100, 25)
        self.button_chase_3.clicked.connect(self.chase_demand_3)

        #Entree chase param speed
        # Create textbox
        self.textbox_chase_speed_3= QLineEdit(self)
        self.textbox_chase_speed_3.setText('0.1')
        self.textbox_chase_speed_3.setGeometry(710, 540, 50, 20)
        # Create a button in the window
        self.button_chase_speed_3= QPushButton('speed', self)
        self.button_chase_speed_3.setGeometry(760, 540, 50, 20)
        # connect button to function on_click
        self.button_chase_speed_3.clicked.connect(self.on_click_ip)

        #Entree chase param size
        # Create textbox
        self.textbox_chase_size_3= QLineEdit(self)
        self.textbox_chase_size_3.setText('5')
        self.textbox_chase_size_3.setGeometry(810, 540, 50, 20)
        # Create a button in the window
        self.button_chase_size_3= QPushButton('size', self)
        self.button_chase_size_3.setGeometry(860, 540, 50, 20)
        # connect button to function on_click
        self.button_chase_size_3.clicked.connect(self.on_click_ip)
        #--------------------------------------------------------------------
        #--------------------------------------------------------------------

        # Bouton comet 3
        self.button_comet_3 = QPushButton('comet', self)
        self.button_comet_3.setToolTip('comet')
        self.button_comet_3.setGeometry(610, 570, 100, 25)
        self.button_comet_3.clicked.connect(self.comet_demand_3)

        #Entree comet param speed
        # Create textbox
        self.textbox_comet_speed_3= QLineEdit(self)
        self.textbox_comet_speed_3.setText('0.1')
        self.textbox_comet_speed_3.setGeometry(710, 570, 50, 20)
        # Create a button in the window
        self.button_comet_speed_3= QPushButton('speed', self)
        self.button_comet_speed_3.setGeometry(760, 570, 50, 20)
        # connect button to function on_click
        self.button_comet_speed_3.clicked.connect(self.on_click_ip)

        #Entree comet param tail
        # Create textbox
        self.textbox_comet_tail_3= QLineEdit(self)
        self.textbox_comet_tail_3.setText('5')
        self.textbox_comet_tail_3.setGeometry(810, 570, 50, 20)
        # Create a button in the window
        self.button_comet_tail_3= QPushButton('tail', self)
        self.button_comet_tail_3.setGeometry(860, 570, 50, 20)
        # connect button to function on_click
        self.button_comet_tail_3.clicked.connect(self.on_click_ip)
        #--------------------------------------------------------------------

        # Bouton pulse 3
        self.button_pulse_3 = QPushButton('pulse', self)
        self.button_pulse_3.setToolTip('pulse')
        self.button_pulse_3.setGeometry(610, 600, 100, 25)
        self.button_pulse_3.clicked.connect(self.pulse_demand_3)

        #Entree pulse param speed
        # Create textbox
        self.textbox_pulse_speed_3= QLineEdit(self)
        self.textbox_pulse_speed_3.setText('0.15')
        self.textbox_pulse_speed_3.setGeometry(710, 600, 50, 20)
        # Create a button in the window
        self.button_pulse_speed_3= QPushButton('speed', self)
        self.button_pulse_speed_3.setGeometry(760, 600, 50, 20)
        # connect button to function on_click
        self.button_pulse_speed_3.clicked.connect(self.on_click_ip)

        #Entree pulse param period
        # Create textbox
        self.textbox_pulse_period_3= QLineEdit(self)
        self.textbox_pulse_period_3.setText('0.1')
        self.textbox_pulse_period_3.setGeometry(810, 600, 50, 20)
        # Create a button in the window
        self.button_pulse_period_3= QPushButton('period', self)
        self.button_pulse_period_3.setGeometry(860, 600, 50, 20)
        # connect button to function on_click
        self.button_pulse_period_3.clicked.connect(self.on_click_ip)
        #--------------------------------------------------------------------

        # Bouton sparkle 3
        self.button_sparkle_3 = QPushButton('sparkle', self)
        self.button_sparkle_3.setToolTip('sparkle')
        self.button_sparkle_3.setGeometry(610, 630, 100, 25)
        self.button_sparkle_3.clicked.connect(self.sparkle_demand_3)

        #Entree sparkle param speed
        # Create textbox
        self.textbox_sparkle_speed_3= QLineEdit(self)
        self.textbox_sparkle_speed_3.setGeometry(710, 630, 50, 20)
        # Create a button in the window
        self.button_sparkle_speed_3= QPushButton('speed', self)
        self.button_sparkle_speed_3.setGeometry(760, 630, 50, 20)
        # connect button to function on_click
        self.button_sparkle_speed_3.clicked.connect(self.on_click_ip)

        #Entree sparkle param num_sparkles
        # Create textbox
        self.textbox_sparkle_num_sparkles_3= QLineEdit(self)
        self.textbox_sparkle_num_sparkles_3.setText('5')
        self.textbox_sparkle_num_sparkles_3.setGeometry(810, 630, 50, 20)
        # Create a button in the window
        self.button_sparkle_num_sparkles_3= QPushButton('num_sparkles', self)
        self.button_sparkle_num_sparkles_3.setGeometry(860, 630, 50, 20)
        # connect button to function on_click
        self.button_sparkle_num_sparkles_3.clicked.connect(self.on_click_ip)
        #--------------------------------------------------------------------

        # Bouton solid 3
        self.button_solid_3 = QPushButton('solid', self)
        self.button_solid_3.setToolTip('solid')
        self.button_solid_3.setGeometry(610, 660, 100, 25)
        self.button_solid_3.clicked.connect(self.solid_demand_3)
        #--------------------------------------------------------------------

        # Bouton colorcycle 3
        self.button_colorcycle_3 = QPushButton('colorcycle', self)
        self.button_colorcycle_3.setToolTip('colorcycle')
        self.button_colorcycle_3.setGeometry(610, 690, 100, 25)
        self.button_colorcycle_3.clicked.connect(self.colorcycle_demand_3)

        #Entree color_cycle param speed
        # Create textbox
        self.textbox_color_cycle_speed_3= QLineEdit(self)
        self.textbox_color_cycle_speed_3.setText('0.1')
        self.textbox_color_cycle_speed_3.setGeometry(710, 690, 50, 20)
        # Create a button in the window
        self.button_color_cycle_speed_3= QPushButton('speed', self)
        self.button_color_cycle_speed_3.setGeometry(760, 690, 50, 20)
        # connect button to function on_click
        self.button_color_cycle_speed_3.clicked.connect(self.on_click_ip)

        #--------------------------------------------------------------------

        # Bouton Dancing Pi Sroll 3
        self.button_dancingPiScroll_3 = QPushButton('dancingPiSroll', self)
        self.button_dancingPiScroll_3.setToolTip('dancingPiSroll')
        self.button_dancingPiScroll_3.setGeometry(610, 720, 100, 25)
        self.button_dancingPiScroll_3.clicked.connect(self.dancingPiScroll_demand_3)

        # Bouton stop_Dancing Pi Sroll 3
        self.button_stop_dancingPiScroll_3 = QPushButton('stop_dancingPiSroll', self)
        self.button_stop_dancingPiScroll_3.setToolTip('stop_dancingPiSroll')
        self.button_stop_dancingPiScroll_3.setGeometry(710, 720, 100, 25)
        self.button_stop_dancingPiScroll_3.clicked.connect(self.stop_dancingPiScroll_demand_3)
        #--------------------------------------------------------------------

        # Bouton Dancing Pi Spectrum 3
        self.button_dancingPiSpectrum_3 = QPushButton('dancingPiSpectrum', self)
        self.button_dancingPiSpectrum_3.setToolTip('dancingPiSpectrum')
        self.button_dancingPiSpectrum_3.setGeometry(610, 750, 100, 25)
        self.button_dancingPiSpectrum_3.clicked.connect(self.dancingPiSpectrum_demand_3)

        # Bouton stop_Dancing Pi Spectrum 3
        self.button_stop_dancingPiSpectrum_3 = QPushButton('stop_dancingPiSpectrum', self)
        self.button_stop_dancingPiSpectrum_3.setToolTip('stop_dancingPiSpectrum')
        self.button_stop_dancingPiSpectrum_3.setGeometry(710, 750, 100, 25)
        self.button_stop_dancingPiSpectrum_3.clicked.connect(self.stop_dancingPiSpectrum_demand_3)
        #--------------------------------------------------------------------

        # Bouton Dancing Pi Energy 3
        self.button_dancingPiEnergy_3 = QPushButton('dancingPiEnergy', self)
        self.button_dancingPiEnergy_3.setToolTip('dancingPiEnergy')
        self.button_dancingPiEnergy_3.setGeometry(610, 780, 100, 25)
        self.button_dancingPiEnergy_3.clicked.connect(self.dancingPiEnergy_demand_3)

        # Bouton stop_Dancing Pi Energy 3
        self.button_stop_dancingPiEnergy_3 = QPushButton('stop_dancingPiEnergy', self)
        self.button_stop_dancingPiEnergy_3.setToolTip('stop_dancingPiEnergy')
        self.button_stop_dancingPiEnergy_3.setGeometry(710, 780, 100, 25)
        self.button_stop_dancingPiEnergy_3.clicked.connect(self.stop_dancingPiEnergy_demand_3)
        #--------------------------------------------------------------------

        # Bouton Cosmo Ball 3
        self.button_cosmoBall_3 = QPushButton('cosmoBall', self)
        self.button_cosmoBall_3.setToolTip('cosmoBall')
        self.button_cosmoBall_3.setGeometry(610,810, 100, 25)
        #self.button_dancingPi.clicked.connect(self.cosmoBall_demand_3)

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
        # Entree adresse IP
        # Create textbox
        self.textbox_IP_4 = QLineEdit(self)
        self.textbox_IP_4.setText('192.168.0.4')
        self.textbox_IP_4.setGeometry(910, 10, 50, 20)
        # Create a button in the window
        self.button_IP_4 = QPushButton('VNC', self)
        self.button_IP_4.setGeometry(960, 10, 50, 20)
        # connect button to function on_click
        self.button_IP_4.clicked.connect(self.on_click_ip_4)

        # Entree Port
        # Create textbox
        self.textbox_port_4 = QLineEdit(self)
        self.textbox_port_4.setText('50004')
        self.textbox_port_4.setGeometry(910, 60, 50, 20)
        # Create a button in the window
        self.button_port_4 = QPushButton('Port', self)
        self.button_port_4.setGeometry(960, 60, 50, 20)
        # connect button to function on_click
        self.button_port_4.clicked.connect(self.on_click_port_4)

        # Couleur 4
        self.type_color44 = QComboBox(self)
        self.type_color44.setGeometry(910, 110, 100, 20)
        self.type_color44.addItems(
            ["AMBER", "AQUA", "BLACK", "BLUE", "CYAN", "GOLD", "GREEN", "JADE", "MAGENTA", "OLD_LACE"
                , "ORANGE", "PINK", "PURPLE", "RAINBOW", "RED",
             "RGBW_WHITE_RGB", "RGBW_WHITE_RGBW", "RGBW_WHITE_W", "TEAL", "WHITE", "YELLOW"])
        self.type_color44.currentIndexChanged.connect(self.color4_change_demand41)

        # Couleur 4
        self.type_color44 = QComboBox(self)
        self.type_color44.setGeometry(960, 110, 100, 20)
        self.type_color44.addItems(
            ["AMBER", "AQUA", "BLACK", "BLUE", "CYAN", "GOLD", "GREEN", "JADE", "MAGENTA", "OLD_LACE"
                , "ORANGE", "PINK", "PURPLE", "RAINBOW", "RED",
             "RGBW_WHITE_RGB", "RGBW_WHITE_RGBW", "RGBW_WHITE_W", "TEAL", "WHITE", "YELLOW"])
        self.type_color44.currentIndexChanged.connect(self.color4_change_demand42)

        #Entree Frequence Strombo 4
        # Create textbox
        self.textbox_strombo_4 = QLineEdit(self)
        self.textbox_strombo_4.setText('0.1')
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

        # --------------------------------------------------------------------
        # Bouton chase 4
        self.button_chase_4 = QPushButton('chase', self)
        self.button_chase_4.setToolTip('chase')
        self.button_chase_4.setGeometry(910, 540, 100, 25)
        self.button_chase_4.clicked.connect(self.chase_demand_4)

        # Entree chase param speed
        # Create textbox
        self.textbox_chase_speed_4 = QLineEdit(self)
        self.textbox_chase_speed_4.setText('0.1')
        self.textbox_chase_speed_4.setGeometry(1010, 540, 50, 20)
        # Create a button in the window
        self.button_chase_speed_4 = QPushButton('speed', self)
        self.button_chase_speed_4.setGeometry(1060, 540, 50, 20)
        # connect button to function on_click
        self.button_chase_speed_4.clicked.connect(self.on_click_ip)

        # Entree chase param size
        # Create textbox
        self.textbox_chase_size_4 = QLineEdit(self)
        self.textbox_chase_size_4.setText('5')
        self.textbox_chase_size_4.setGeometry(1110, 540, 50, 20)
        # Create a button in the window
        self.button_chase_size_4 = QPushButton('size', self)
        self.button_chase_size_4.setGeometry(1160, 540, 50, 20)
        # connect button to function on_click
        self.button_chase_size_4.clicked.connect(self.on_click_ip)
        # --------------------------------------------------------------------
        # --------------------------------------------------------------------

        # Bouton comet 4
        self.button_comet_4 = QPushButton('comet', self)
        self.button_comet_4.setToolTip('comet')
        self.button_comet_4.setGeometry(910, 570, 100, 25)
        self.button_comet_4.clicked.connect(self.comet_demand_4)

        # Entree comet param speed
        # Create textbox
        self.textbox_comet_speed_4 = QLineEdit(self)
        self.textbox_comet_speed_4.setText('0.1')
        self.textbox_comet_speed_4.setGeometry(1010, 570, 50, 20)
        # Create a button in the window
        self.button_comet_speed_4 = QPushButton('speed', self)
        self.button_comet_speed_4.setGeometry(1060, 570, 50, 20)
        # connect button to function on_click
        self.button_comet_speed_4.clicked.connect(self.on_click_ip)

        # Entree comet param tail
        # Create textbox
        self.textbox_comet_tail_4 = QLineEdit(self)
        self.textbox_comet_tail_4.setText('5')
        self.textbox_comet_tail_4.setGeometry(1110, 570, 50, 20)
        # Create a button in the window
        self.button_comet_tail_4 = QPushButton('tail', self)
        self.button_comet_tail_4.setGeometry(1160, 570, 50, 20)
        # connect button to function on_click
        self.button_comet_tail_4.clicked.connect(self.on_click_ip)
        # --------------------------------------------------------------------

        # Bouton pulse 4
        self.button_pulse_4 = QPushButton('pulse', self)
        self.button_pulse_4.setToolTip('pulse')
        self.button_pulse_4.setGeometry(910, 600, 100, 25)
        self.button_pulse_4.clicked.connect(self.pulse_demand_4)

        # Entree pulse param speed
        # Create textbox
        self.textbox_pulse_speed_4 = QLineEdit(self)
        self.textbox_pulse_speed_4.setText('0.15')
        self.textbox_pulse_speed_4.setGeometry(1010, 600, 50, 20)
        # Create a button in the window
        self.button_pulse_speed_4 = QPushButton('speed', self)
        self.button_pulse_speed_4.setGeometry(1060, 600, 50, 20)
        # connect button to function on_click
        self.button_pulse_speed_4.clicked.connect(self.on_click_ip)

        # Entree pulse param period
        # Create textbox
        self.textbox_pulse_period_4 = QLineEdit(self)
        self.textbox_pulse_period_4.setText('0.15')
        self.textbox_pulse_period_4.setGeometry(1110, 600, 50, 20)
        # Create a button in the window
        self.button_pulse_period_4 = QPushButton('period', self)
        self.button_pulse_period_4.setGeometry(1160, 600, 50, 20)
        # connect button to function on_click
        self.button_pulse_period_4.clicked.connect(self.on_click_ip)
        # --------------------------------------------------------------------

        # Bouton sparkle 4
        self.button_sparkle_4 = QPushButton('sparkle', self)
        self.button_sparkle_4.setToolTip('sparkle')
        self.button_sparkle_4.setGeometry(910, 630, 100, 25)
        self.button_sparkle_4.clicked.connect(self.sparkle_demand_4)

        # Entree sparkle param speed
        # Create textbox
        self.textbox_sparkle_speed_4 = QLineEdit(self)
        self.textbox_sparkle_speed_4.setText('0.1')
        self.textbox_sparkle_speed_4.setGeometry(1010, 630, 50, 20)
        # Create a button in the window
        self.button_sparkle_speed_4 = QPushButton('speed', self)
        self.button_sparkle_speed_4.setGeometry(1060, 630, 50, 20)
        # connect button to function on_click
        self.button_sparkle_speed_4.clicked.connect(self.on_click_ip)

        # Entree sparkle param num_sparkles
        # Create textbox
        self.textbox_sparkle_num_sparkles_4 = QLineEdit(self)
        self.textbox_sparkle_num_sparkles_4.setText('5')
        self.textbox_sparkle_num_sparkles_4.setGeometry(1110, 630, 50, 20)
        # Create a button in the window
        self.button_sparkle_num_sparkles_4 = QPushButton('num_sparkles', self)
        self.button_sparkle_num_sparkles_4.setGeometry(1160, 630, 50, 20)
        # connect button to function on_click
        self.button_sparkle_num_sparkles_4.clicked.connect(self.on_click_ip)
        # --------------------------------------------------------------------

        # Bouton solid 4
        self.button_solid_4 = QPushButton('solid', self)
        self.button_solid_4.setToolTip('solid')
        self.button_solid_4.setGeometry(910, 660, 100, 25)
        self.button_solid_4.clicked.connect(self.solid_demand_4)
        # --------------------------------------------------------------------

        # Bouton colorcycle 4
        self.button_colorcycle_4 = QPushButton('colorcycle', self)
        self.button_colorcycle_4.setToolTip('colorcycle')
        self.button_colorcycle_4.setGeometry(910, 690, 100, 25)
        self.button_colorcycle_4.clicked.connect(self.colorcycle_demand_4)

        # Entree color_cycle param speed
        # Create textbox
        self.textbox_color_cycle_speed_4 = QLineEdit(self)
        self.textbox_color_cycle_speed_4.setText('0.1')
        self.textbox_color_cycle_speed_4.setGeometry(1010, 690, 50, 20)
        # Create a button in the window
        self.button_color_cycle_speed_4 = QPushButton('speed', self)
        self.button_color_cycle_speed_4.setGeometry(1060, 690, 50, 20)
        # connect button to function on_click
        self.button_color_cycle_speed_4.clicked.connect(self.on_click_ip)

        # --------------------------------------------------------------------

        # Bouton Dancing Pi Sroll 4
        self.button_dancingPiScroll_4 = QPushButton('dancingPiSroll', self)
        self.button_dancingPiScroll_4.setToolTip('dancingPiSroll')
        self.button_dancingPiScroll_4.setGeometry(910, 720, 100, 25)
        self.button_dancingPiScroll_4.clicked.connect(self.dancingPiScroll_demand_4)

        # Bouton stop_Dancing Pi Sroll 4
        self.button_stop_dancingPiScroll_4 = QPushButton('stop_dancingPiSroll', self)
        self.button_stop_dancingPiScroll_4.setToolTip('stop_dancingPiSroll')
        self.button_stop_dancingPiScroll_4.setGeometry(1010, 720, 100, 25)
        self.button_stop_dancingPiScroll_4.clicked.connect(self.stop_dancingPiScroll_demand_4)
        # --------------------------------------------------------------------

        # Bouton Dancing Pi Spectrum 4
        self.button_dancingPiSpectrum_4 = QPushButton('dancingPiSpectrum', self)
        self.button_dancingPiSpectrum_4.setToolTip('dancingPiSpectrum')
        self.button_dancingPiSpectrum_4.setGeometry(910, 750, 100, 25)
        self.button_dancingPiSpectrum_4.clicked.connect(self.dancingPiSpectrum_demand_4)

        # Bouton stop_Dancing Pi Spectrum 4
        self.button_stop_dancingPiSpectrum_4 = QPushButton('stop_dancingPiSpectrum', self)
        self.button_stop_dancingPiSpectrum_4.setToolTip('stop_dancingPiSpectrum')
        self.button_stop_dancingPiSpectrum_4.setGeometry(1010, 750, 100, 25)
        self.button_stop_dancingPiSpectrum_4.clicked.connect(self.stop_dancingPiSpectrum_demand_4)
        # --------------------------------------------------------------------

        # Bouton Dancing Pi Energy 4
        self.button_dancingPiEnergy_4 = QPushButton('dancingPiEnergy', self)
        self.button_dancingPiEnergy_4.setToolTip('dancingPiEnergy')
        self.button_dancingPiEnergy_4.setGeometry(910, 780, 100, 25)
        self.button_dancingPiEnergy_4.clicked.connect(self.dancingPiEnergy_demand_4)

        # Bouton stop_Dancing Pi Energy 4
        self.button_stop_dancingPiEnergy_4 = QPushButton('stop_dancingPiEnergy', self)
        self.button_stop_dancingPiEnergy_4.setToolTip('stop_dancingPiEnergy')
        self.button_stop_dancingPiEnergy_4.setGeometry(1010, 780, 100, 25)
        self.button_stop_dancingPiEnergy_4.clicked.connect(self.stop_dancingPiEnergy_demand_4)
        # --------------------------------------------------------------------

        # Bouton Cosmo Ball 4
        self.button_cosmoBall_4 = QPushButton('cosmoBall', self)
        self.button_cosmoBall_4.setToolTip('cosmoBall')
        self.button_cosmoBall_4.setGeometry(910, 810, 100, 25)
        # self.button_dancingPi.clicked.connect(self.cosmoBall_demand_4)

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
        # Entree adresse IP
        # Create textbox
        self.textbox_IP_5 = QLineEdit(self)
        self.textbox_IP_5.setText('192.168.0.5')
        self.textbox_IP_5.setGeometry(1210, 10, 50, 20)
        # Create a button in the window
        self.button_IP_5 = QPushButton('VNC', self)
        self.button_IP_5.setGeometry(1260, 10, 50, 20)
        # connect button to function on_click
        self.button_IP_5.clicked.connect(self.on_click_ip_5)

        # Entree Port
        # Create textbox
        self.textbox_port_5 = QLineEdit(self)
        self.textbox_port_5.setText('50005')
        self.textbox_port_5.setGeometry(1210, 60, 50, 20)
        # Create a button in the window
        self.button_port_5 = QPushButton('Port', self)
        self.button_port_5.setGeometry(1260, 60, 50, 20)
        # connect button to function on_click
        self.button_port_5.clicked.connect(self.on_click_port_5)

        # Couleur 5
        self.type_color55 = QComboBox(self)
        self.type_color55.setGeometry(1210, 110, 100, 20)
        self.type_color55.addItems(
            ["AMBER", "AQUA", "BLACK", "BLUE", "CYAN", "GOLD", "GREEN", "JADE", "MAGENTA", "OLD_LACE"
                , "ORANGE", "PINK", "PURPLE", "RAINBOW", "RED",
             "RGBW_WHITE_RGB", "RGBW_WHITE_RGBW", "RGBW_WHITE_W", "TEAL", "WHITE", "YELLOW"])
        self.type_color55.currentIndexChanged.connect(self.color5_change_demand51)

        # Couleur 5
        self.type_color55 = QComboBox(self)
        self.type_color55.setGeometry(1260, 110, 100, 20)
        self.type_color55.addItems(
            ["AMBER", "AQUA", "BLACK", "BLUE", "CYAN", "GOLD", "GREEN", "JADE", "MAGENTA", "OLD_LACE"
                , "ORANGE", "PINK", "PURPLE", "RAINBOW", "RED",
             "RGBW_WHITE_RGB", "RGBW_WHITE_RGBW", "RGBW_WHITE_W", "TEAL", "WHITE", "YELLOW"])
        self.type_color55.currentIndexChanged.connect(self.color5_change_demand52)

        #Entree Frequence Strombo 5
        # Create textbox
        self.textbox_strombo_5 = QLineEdit(self)
        self.textbox_strombo_5.setText('0.1')
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

        #--------------------------------------------------------------------
        # Bouton chase 5
        self.button_chase_5 = QPushButton('chase', self)
        self.button_chase_5.setToolTip('chase')
        self.button_chase_5.setGeometry(1210, 540, 100, 25)
        self.button_chase_5.clicked.connect(self.chase_demand_5)

        #Entree chase param speed
        # Create textbox
        self.textbox_chase_speed_5= QLineEdit(self)
        self.textbox_chase_speed_5.setText('0.1')
        self.textbox_chase_speed_5.setGeometry(1310, 540, 50, 20)
        # Create a button in the window
        self.button_chase_speed_5= QPushButton('speed', self)
        self.button_chase_speed_5.setGeometry(1360, 540, 50, 20)
        # connect button to function on_click
        self.button_chase_speed_5.clicked.connect(self.on_click_ip)

        #Entree chase param size
        # Create textbox
        self.textbox_chase_size_5= QLineEdit(self)
        self.textbox_chase_size_5.setText('5')
        self.textbox_chase_size_5.setGeometry(1410, 540, 50, 20)
        # Create a button in the window
        self.button_chase_size_5= QPushButton('size', self)
        self.button_chase_size_5.setGeometry(1460, 540, 50, 20)
        # connect button to function on_click
        self.button_chase_size_5.clicked.connect(self.on_click_ip)
        #--------------------------------------------------------------------
        #--------------------------------------------------------------------

        # Bouton comet 5
        self.button_comet_5 = QPushButton('comet', self)
        self.button_comet_5.setToolTip('comet')
        self.button_comet_5.setGeometry(1210, 570, 100, 25)
        self.button_comet_5.clicked.connect(self.comet_demand_5)

        #Entree comet param speed
        # Create textbox
        self.textbox_comet_speed_5= QLineEdit(self)
        self.textbox_comet_speed_5.setText('0.1')
        self.textbox_comet_speed_5.setGeometry(1310, 570, 50, 20)
        # Create a button in the window
        self.button_comet_speed_5= QPushButton('speed', self)
        self.button_comet_speed_5.setGeometry(1360, 570, 50, 20)
        # connect button to function on_click
        self.button_comet_speed_5.clicked.connect(self.on_click_ip)

        #Entree comet param tail
        # Create textbox
        self.textbox_comet_tail_5= QLineEdit(self)
        self.textbox_comet_tail_5.setText('5')
        self.textbox_comet_tail_5.setGeometry(1410, 570, 50, 20)
        # Create a button in the window
        self.button_comet_tail_5= QPushButton('tail', self)
        self.button_comet_tail_5.setGeometry(1460, 570, 50, 20)
        # connect button to function on_click
        self.button_comet_tail_5.clicked.connect(self.on_click_ip)
        #--------------------------------------------------------------------

        # Bouton pulse 5
        self.button_pulse_5 = QPushButton('pulse', self)
        self.button_pulse_5.setToolTip('pulse')
        self.button_pulse_5.setGeometry(1210, 600, 100, 25)
        self.button_pulse_5.clicked.connect(self.pulse_demand_5)

        #Entree pulse param speed
        # Create textbox
        self.textbox_pulse_speed_5= QLineEdit(self)
        self.textbox_pulse_speed_5.setText('0.1')
        self.textbox_pulse_speed_5.setGeometry(1310, 600, 50, 20)
        # Create a button in the window
        self.button_pulse_speed_5= QPushButton('speed', self)
        self.button_pulse_speed_5.setGeometry(1360, 600, 50, 20)
        # connect button to function on_click
        self.button_pulse_speed_5.clicked.connect(self.on_click_ip)

        #Entree pulse param period
        # Create textbox
        self.textbox_pulse_period_5= QLineEdit(self)
        self.textbox_pulse_period_5.setText('0.1')
        self.textbox_pulse_period_5.setGeometry(1410, 600, 50, 20)
        # Create a button in the window
        self.button_pulse_period_5= QPushButton('period', self)
        self.button_pulse_period_5.setGeometry(1460, 600, 50, 20)
        # connect button to function on_click
        self.button_pulse_period_5.clicked.connect(self.on_click_ip)
        #--------------------------------------------------------------------

        # Bouton sparkle 5
        self.button_sparkle_5 = QPushButton('sparkle', self)
        self.button_sparkle_5.setToolTip('sparkle')
        self.button_sparkle_5.setGeometry(1210, 630, 100, 25)
        self.button_sparkle_5.clicked.connect(self.sparkle_demand_5)

        #Entree sparkle param speed
        # Create textbox
        self.textbox_sparkle_speed_5= QLineEdit(self)
        self.textbox_sparkle_speed_5.setText('0.1')
        self.textbox_sparkle_speed_5.setGeometry(1310, 630, 50, 20)
        # Create a button in the window
        self.button_sparkle_speed_5= QPushButton('speed', self)
        self.button_sparkle_speed_5.setGeometry(1360, 630, 50, 20)
        # connect button to function on_click
        self.button_sparkle_speed_5.clicked.connect(self.on_click_ip)

        #Entree sparkle param num_sparkles
        # Create textbox
        self.textbox_sparkle_num_sparkles_5= QLineEdit(self)
        self.textbox_sparkle_num_sparkles_5.setText('5')
        self.textbox_sparkle_num_sparkles_5.setGeometry(1410, 630, 50, 20)
        # Create a button in the window
        self.button_sparkle_num_sparkles_5= QPushButton('num_sparkles', self)
        self.button_sparkle_num_sparkles_5.setGeometry(1460, 630, 50, 20)
        # connect button to function on_click
        self.button_sparkle_num_sparkles_5.clicked.connect(self.on_click_ip)
        #--------------------------------------------------------------------

        # Bouton solid 5
        self.button_solid_5 = QPushButton('solid', self)
        self.button_solid_5.setToolTip('solid')
        self.button_solid_5.setGeometry(1210, 660, 100, 25)
        self.button_solid_5.clicked.connect(self.solid_demand_5)
        #--------------------------------------------------------------------

        # Bouton colorcycle 5
        self.button_colorcycle_5 = QPushButton('colorcycle', self)
        self.button_colorcycle_5.setToolTip('colorcycle')
        self.button_colorcycle_5.setGeometry(1210, 690, 100, 25)
        self.button_colorcycle_5.clicked.connect(self.colorcycle_demand_5)

        #Entree color_cycle param speed
        # Create textbox
        self.textbox_color_cycle_speed_5= QLineEdit(self)
        self.textbox_color_cycle_speed_5.setText('0.1')
        self.textbox_color_cycle_speed_5.setGeometry(1310, 690, 50, 20)
        # Create a button in the window
        self.button_color_cycle_speed_5= QPushButton('speed', self)
        self.button_color_cycle_speed_5.setGeometry(1360, 690, 50, 20)
        # connect button to function on_click
        self.button_color_cycle_speed_5.clicked.connect(self.on_click_ip)

        #--------------------------------------------------------------------

        # Bouton Dancing Pi Sroll 5
        self.button_dancingPiScroll_5 = QPushButton('dancingPiSroll', self)
        self.button_dancingPiScroll_5.setToolTip('dancingPiSroll')
        self.button_dancingPiScroll_5.setGeometry(1210, 720, 100, 25)
        self.button_dancingPiScroll_5.clicked.connect(self.dancingPiScroll_demand_5)

        # Bouton stop_Dancing Pi Sroll 5
        self.button_stop_dancingPiScroll_5 = QPushButton('stop_dancingPiSroll', self)
        self.button_stop_dancingPiScroll_5.setToolTip('stop_dancingPiSroll')
        self.button_stop_dancingPiScroll_5.setGeometry(1310, 720, 100, 25)
        self.button_stop_dancingPiScroll_5.clicked.connect(self.stop_dancingPiScroll_demand_5)
        #--------------------------------------------------------------------

        # Bouton Dancing Pi Spectrum 5
        self.button_dancingPiSpectrum_5 = QPushButton('dancingPiSpectrum', self)
        self.button_dancingPiSpectrum_5.setToolTip('dancingPiSpectrum')
        self.button_dancingPiSpectrum_5.setGeometry(1210, 750, 100, 25)
        self.button_dancingPiSpectrum_5.clicked.connect(self.dancingPiSpectrum_demand_5)

        # Bouton stop_Dancing Pi Spectrum 5
        self.button_stop_dancingPiSpectrum_5 = QPushButton('stop_dancingPiSpectrum', self)
        self.button_stop_dancingPiSpectrum_5.setToolTip('stop_dancingPiSpectrum')
        self.button_stop_dancingPiSpectrum_5.setGeometry(1310, 750, 100, 25)
        self.button_stop_dancingPiSpectrum_5.clicked.connect(self.stop_dancingPiSpectrum_demand_5)
        #--------------------------------------------------------------------

        # Bouton Dancing Pi Energy 5
        self.button_dancingPiEnergy_5 = QPushButton('dancingPiEnergy', self)
        self.button_dancingPiEnergy_5.setToolTip('dancingPiEnergy')
        self.button_dancingPiEnergy_5.setGeometry(1210, 780, 100, 25)
        self.button_dancingPiEnergy_5.clicked.connect(self.dancingPiEnergy_demand_5)

        # Bouton stop_Dancing Pi Energy 5
        self.button_stop_dancingPiEnergy_5 = QPushButton('stop_dancingPiEnergy', self)
        self.button_stop_dancingPiEnergy_5.setToolTip('stop_dancingPiEnergy')
        self.button_stop_dancingPiEnergy_5.setGeometry(1310, 780, 100, 25)
        self.button_stop_dancingPiEnergy_5.clicked.connect(self.stop_dancingPiEnergy_demand_5)
        #--------------------------------------------------------------------

        # Bouton Cosmo Ball 5
        self.button_cosmoBall_5 = QPushButton('cosmoBall', self)
        self.button_cosmoBall_5.setToolTip('cosmoBall')
        self.button_cosmoBall_5.setGeometry(1210,810, 100, 25)
        #self.button_dancingPi.clicked.connect(self.cosmoBall_demand_5)

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
        # Entree adresse IP
        # Create textbox
        self.textbox_IP_6 = QLineEdit(self)
        self.textbox_IP_6.setText('192.168.0.6')
        self.textbox_IP_6.setGeometry(1510, 10, 50, 20)
        # Create a button in the window
        self.button_IP_6 = QPushButton('VNC', self)
        self.button_IP_6.setGeometry(1560, 10, 50, 20)
        # connect button to function on_click
        self.button_IP_6.clicked.connect(self.on_click_ip_6)

        # Entree Port
        # Create textbox
        self.textbox_port_6 = QLineEdit(self)
        self.textbox_port_6.setText('50006')
        self.textbox_port_6.setGeometry(1510, 60, 50, 20)
        # Create a button in the window
        self.button_port_6 = QPushButton('Port', self)
        self.button_port_6.setGeometry(1560, 60, 50, 20)
        # connect button to function on_click
        self.button_port_6.clicked.connect(self.on_click_port_6)

        # Couleur 6
        self.type_color16 = QComboBox(self)
        self.type_color16.setGeometry(1510, 110, 100, 20)
        self.type_color16.addItems(
            ["AMBER", "AQUA", "BLACK", "BLUE", "CYAN", "GOLD", "GREEN", "JADE", "MAGENTA", "OLD_LACE"
                , "ORANGE", "PINK", "PURPLE", "RAINBOW", "RED",
             "RGBW_WHITE_RGB", "RGBW_WHITE_RGBW", "RGBW_WHITE_W", "TEAL", "WHITE", "YELLOW"])
        self.type_color16.currentIndexChanged.connect(self.color6_change_demand61)

        # Couleur 2
        self.type_color26 = QComboBox(self)
        self.type_color26.setGeometry(1560, 110, 100, 20)
        self.type_color26.addItems(
            ["AMBER", "AQUA", "BLACK", "BLUE", "CYAN", "GOLD", "GREEN", "JADE", "MAGENTA", "OLD_LACE"
                , "ORANGE", "PINK", "PURPLE", "RAINBOW", "RED",
             "RGBW_WHITE_RGB", "RGBW_WHITE_RGBW", "RGBW_WHITE_W", "TEAL", "WHITE", "YELLOW"])
        self.type_color26.currentIndexChanged.connect(self.color6_change_demand62)

        #Entree Frequence Strombo 6
        # Create textbox
        self.textbox_strombo_6 = QLineEdit(self)
        self.textbox_strombo_6.setText('0.1')
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

        #--------------------------------------------------------------------
        # Bouton chase 6
        self.button_chase_6 = QPushButton('chase', self)
        self.button_chase_6.setToolTip('chase')
        self.button_chase_6.setGeometry(1510, 540, 100, 25)
        self.button_chase_6.clicked.connect(self.chase_demand_6)

        #Entree chase param speed
        # Create textbox
        self.textbox_chase_speed_6= QLineEdit(self)
        self.textbox_chase_speed_6.setText('0.1')
        self.textbox_chase_speed_6.setGeometry(1610, 540, 50, 20)
        # Create a button in the window
        self.button_chase_speed_6= QPushButton('speed', self)
        self.button_chase_speed_6.setGeometry(1660, 540, 50, 20)
        # connect button to function on_click
        self.button_chase_speed_6.clicked.connect(self.on_click_ip)

        #Entree chase param size
        # Create textbox
        self.textbox_chase_size_6= QLineEdit(self)
        self.textbox_chase_size_6.setText('5')
        self.textbox_chase_size_6.setGeometry(1710, 540, 50, 20)
        # Create a button in the window
        self.button_chase_size_6= QPushButton('size', self)
        self.button_chase_size_6.setGeometry(1760, 540, 50, 20)
        # connect button to function on_click
        self.button_chase_size_6.clicked.connect(self.on_click_ip)
        #--------------------------------------------------------------------
        #--------------------------------------------------------------------

        # Bouton comet 6
        self.button_comet_6 = QPushButton('comet', self)
        self.button_comet_6.setToolTip('comet')
        self.button_comet_6.setGeometry(1510, 570, 100, 25)
        self.button_comet_6.clicked.connect(self.comet_demand_6)

        #Entree comet param speed
        # Create textbox
        self.textbox_comet_speed_6= QLineEdit(self)
        self.textbox_comet_speed_6.setText('0.1')
        self.textbox_comet_speed_6.setGeometry(1610, 570, 50, 20)
        # Create a button in the window
        self.button_comet_speed_6= QPushButton('speed', self)
        self.button_comet_speed_6.setGeometry(1660, 570, 50, 20)
        # connect button to function on_click
        self.button_comet_speed_6.clicked.connect(self.on_click_ip)

        #Entree comet param tail
        # Create textbox
        self.textbox_comet_tail_6= QLineEdit(self)
        self.textbox_comet_tail_6.setText('5')
        self.textbox_comet_tail_6.setGeometry(1710, 570, 50, 20)
        # Create a button in the window
        self.button_comet_tail_6= QPushButton('tail', self)
        self.button_comet_tail_6.setGeometry(1760, 570, 50, 20)
        # connect button to function on_click
        self.button_comet_tail_6.clicked.connect(self.on_click_ip)
        #--------------------------------------------------------------------

        # Bouton pulse 6
        self.button_pulse_6 = QPushButton('pulse', self)
        self.button_pulse_6.setToolTip('pulse')
        self.button_pulse_6.setGeometry(1510, 600, 100, 26)
        self.button_pulse_6.clicked.connect(self.pulse_demand_6)

        #Entree pulse param speed
        # Create textbox
        self.textbox_pulse_speed_6= QLineEdit(self)
        self.textbox_pulse_speed_6.setText('0.1')
        self.textbox_pulse_speed_6.setGeometry(1610, 600, 50, 20)
        # Create a button in the window
        self.button_pulse_speed_6= QPushButton('speed', self)
        self.button_pulse_speed_6.setGeometry(1660, 600, 50, 20)
        # connect button to function on_click
        self.button_pulse_speed_6.clicked.connect(self.on_click_ip)

        #Entree pulse param period
        # Create textbox
        self.textbox_pulse_period_6= QLineEdit(self)
        self.textbox_pulse_period_6.setText('0.1')
        self.textbox_pulse_period_6.setGeometry(1710, 600, 50, 20)
        # Create a button in the window
        self.button_pulse_period_6= QPushButton('period', self)
        self.button_pulse_period_6.setGeometry(1760, 600, 50, 20)
        # connect button to function on_click
        self.button_pulse_period_6.clicked.connect(self.on_click_ip)
        #--------------------------------------------------------------------

        # Bouton sparkle 6
        self.button_sparkle_6 = QPushButton('sparkle', self)
        self.button_sparkle_6.setToolTip('sparkle')
        self.button_sparkle_6.setGeometry(1510, 630, 100, 25)
        self.button_sparkle_6.clicked.connect(self.sparkle_demand_6)

        #Entree sparkle param speed
        # Create textbox
        self.textbox_sparkle_speed_6= QLineEdit(self)
        self.textbox_sparkle_speed_6.setText('0.1')
        self.textbox_sparkle_speed_6.setGeometry(1610, 630, 50, 20)
        # Create a button in the window
        self.button_sparkle_speed_6= QPushButton('speed', self)
        self.button_sparkle_speed_6.setGeometry(1660, 630, 50, 20)
        # connect button to function on_click
        self.button_sparkle_speed_6.clicked.connect(self.on_click_ip)

        #Entree sparkle param num_sparkles
        # Create textbox
        self.textbox_sparkle_num_sparkles_6= QLineEdit(self)
        self.textbox_sparkle_num_sparkles_6.setText('5')
        self.textbox_sparkle_num_sparkles_6.setGeometry(1710, 630, 50, 20)
        # Create a button in the window
        self.button_sparkle_num_sparkles_6= QPushButton('num_sparkles', self)
        self.button_sparkle_num_sparkles_6.setGeometry(1760, 630, 50, 20)
        # connect button to function on_click
        self.button_sparkle_num_sparkles_6.clicked.connect(self.on_click_ip)
        #--------------------------------------------------------------------

        # Bouton solid 6
        self.button_solid_6 = QPushButton('solid', self)
        self.button_solid_6.setToolTip('solid')
        self.button_solid_6.setGeometry(1510, 660, 100, 25)
        self.button_solid_6.clicked.connect(self.solid_demand_6)
        #--------------------------------------------------------------------

        # Bouton colorcycle 6
        self.button_colorcycle_6 = QPushButton('colorcycle', self)
        self.button_colorcycle_6.setToolTip('colorcycle')
        self.button_colorcycle_6.setGeometry(1510, 690, 100, 26)
        self.button_colorcycle_6.clicked.connect(self.colorcycle_demand_6)

        #Entree color_cycle param speed
        # Create textbox
        self.textbox_color_cycle_speed_6= QLineEdit(self)
        self.textbox_color_cycle_speed_6.setText('0.1')
        self.textbox_color_cycle_speed_6.setGeometry(1610, 690, 50, 20)
        # Create a button in the window
        self.button_color_cycle_speed_6= QPushButton('speed', self)
        self.button_color_cycle_speed_6.setGeometry(1660, 690, 50, 20)
        # connect button to function on_click
        self.button_color_cycle_speed_6.clicked.connect(self.on_click_ip)

        #--------------------------------------------------------------------

        # Bouton Dancing Pi Sroll 6
        self.button_dancingPiScroll_6 = QPushButton('dancingPiSroll', self)
        self.button_dancingPiScroll_6.setToolTip('dancingPiSroll')
        self.button_dancingPiScroll_6.setGeometry(1510, 720, 100, 26)
        self.button_dancingPiScroll_6.clicked.connect(self.dancingPiScroll_demand_6)

        # Bouton stop_Dancing Pi Sroll 6
        self.button_stop_dancingPiScroll_6 = QPushButton('stop_dancingPiSroll', self)
        self.button_stop_dancingPiScroll_6.setToolTip('stop_dancingPiSroll')
        self.button_stop_dancingPiScroll_6.setGeometry(1610, 720, 100, 26)
        self.button_stop_dancingPiScroll_6.clicked.connect(self.stop_dancingPiScroll_demand_6)
        #--------------------------------------------------------------------

        # Bouton Dancing Pi Spectrum 6
        self.button_dancingPiSpectrum_6 = QPushButton('dancingPiSpectrum', self)
        self.button_dancingPiSpectrum_6.setToolTip('dancingPiSpectrum')
        self.button_dancingPiSpectrum_6.setGeometry(1510, 750, 100, 25)
        self.button_dancingPiSpectrum_6.clicked.connect(self.dancingPiSpectrum_demand_6)

        # Bouton stop_Dancing Pi Spectrum 6
        self.button_stop_dancingPiSpectrum_6 = QPushButton('stop_dancingPiSpectrum', self)
        self.button_stop_dancingPiSpectrum_6.setToolTip('stop_dancingPiSpectrum')
        self.button_stop_dancingPiSpectrum_6.setGeometry(1610, 750, 100, 25)
        self.button_stop_dancingPiSpectrum_6.clicked.connect(self.stop_dancingPiSpectrum_demand_6)
        #--------------------------------------------------------------------

        # Bouton Dancing Pi Energy 6
        self.button_dancingPiEnergy_6 = QPushButton('dancingPiEnergy', self)
        self.button_dancingPiEnergy_6.setToolTip('dancingPiEnergy')
        self.button_dancingPiEnergy_6.setGeometry(1510, 780, 100, 25)
        self.button_dancingPiEnergy_6.clicked.connect(self.dancingPiEnergy_demand_6)

        # Bouton stop_Dancing Pi Energy 6
        self.button_stop_dancingPiEnergy_6 = QPushButton('stop_dancingPiEnergy', self)
        self.button_stop_dancingPiEnergy_6.setToolTip('stop_dancingPiEnergy')
        self.button_stop_dancingPiEnergy_6.setGeometry(1610, 780, 100, 25)
        self.button_stop_dancingPiEnergy_6.clicked.connect(self.stop_dancingPiEnergy_demand_6)
        #--------------------------------------------------------------------

        # Bouton Cosmo Ball 6
        self.button_cosmoBall_6 = QPushButton('cosmoBall', self)
        self.button_cosmoBall_6.setToolTip('cosmoBall')
        self.button_cosmoBall_6.setGeometry(1510,810, 100, 26)
        #self.button_dancingPi.clicked.connect(self.cosmoBall_demand_6)

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
        #Force restart by SSH - paramiko lib
        subprocess.Popen(args='python Thread_start_display_remote_ssh.py', shell=True)
        #subprocess.Popen(args='python start_display_remote_ssh.py', shell=True)
        i=0
        self.device = []
        for elt in strip_configuration["guirlande"]:
            try:
                self.objs[i].connect(elt["IP"],1883,60)
                print("publish blackout")
                self.device.append(elt["IP"])
                self.objs[i].publish('test1', "cosmoguirlande,blackout")
                            
                
            except:
                print("could not connect to :  ", elt["IP"])
                #====================================================================test
                print("elt['IP']", elt["IP"])
                
                try:
                    #del strip_configuration["guirlande"][i]
                    self.objs.remove(self.objs[i])
                    self.device.remove(elt["IP"])
                except ValueError:
                    pass
                except IndexError:
                    pass
                
                #====================================================================fin test
            
            i = i+1

            for elt in strip_configuration["guirlande"]:
                print(elt)

            for i, elt in enumerate(self.objs):
                print("À l'indice {} se trouve {}.".format(i, elt))

            for i, elt in enumerate(self.device):
                print("À l'indice {} se trouve {}.".format(i, elt))
            #-----------------------------------------------------------------------

    def git_pull_demand(self):
        self.msg1 = 'cosmoguirlande,git_pull'

        #Force restart by SSH - paramiko lib
        subprocess.Popen(args='python git_pull_remote_ssh.py', shell=True)

    def manual_demand_1(self):
        print("selection changed ", self.type_color11.currentText())
        self.msg1 = 'cosmoguirlande,manual'

        i = 0
        #for elt in strip_configuration["guirlande"]:
        for elt in self.device:
            try:
                self.objs[i].connect(elt,1883,60)
                self.objs[i].publish("test1", self.msg1)
            except:
                print("could not send to :  ", elt)
            i = i+1

    def color1_change_demand11(self):
        print("selection changed ", self.type_color11.currentText())
        self.msg1 = 'cosmoguirlande,color1,' + str(( self.type_color11.currentText()))

        i = 0
        #for elt in strip_configuration["guirlande"]:
        for elt in self.device:
            try:
                self.objs[i].connect(elt,1883,60)
                self.objs[i].publish("test1", self.msg1)
            except:
                print("could not send to :  ", elt)
            i = i+1

    def color2_change_demand12(self):
        print("selection changed ", self.type_color21.currentText())
        self.msg1 = 'cosmoguirlande,color2,' + str(( self.type_color21.currentText()))

        i = 0
        #for elt in strip_configuration["guirlande"]:
        for elt in self.device:
            try:
                self.objs[i].connect(elt,1883,60)
                self.objs[i].publish("test1", self.msg1)
            except:
                print("could not send to :  ", elt)
            i = i+1

    def blackout_demand(self):
        self.msg1 = 'cosmoguirlande,blackout'
        try:
            self.objs[0].connect(self.device[0],1883,60)
            self.objs[0].publish("test1", self.msg1)
        except:
            print("first strip on list not effective")
        if self.sync:
            i = 0 
            #for elt in strip_configuration["guirlande"]:
            for elt in self.device:
                try:
                    self.objs[i].connect(elt,1883,60)
                    self.objs[i].publish("test1", self.msg1)
                except:
                    print("could not send to :  ", elt)
                i = i+1

    def rainbow_demand(self):
        self.msg1 = 'cosmoguirlande,rainbow'
        try:
            self.objs[0].connect(self.device[0],1883,60)
            self.objs[0].publish("test1", self.msg1)
        except:
            print("first strip on list not effective")
        if self.sync:
            i = 0
            #for elt in strip_configuration["guirlande"]:
            for elt in self.device:
                try:
                    self.objs[i].connect(elt,1883,60)
                    self.objs[i].publish("test1", self.msg1)
                except:
                    print("could not send to :  ", elt)
                i = i+1

    def strombo_demand(self):
        self.msg1 = 'cosmoguirlande,strombo'
        try:
            self.objs[0].connect(self.device[0],1883,60)
            self.objs[0].publish("test1", self.msg1)
        except:
            print("first strip on list not effective")
        if self.sync:
            i = 0
            #for elt in strip_configuration["guirlande"]:
            for elt in self.device:
                try:
                    self.objs[i].connect(elt,1883,60)
                    self.objs[i].publish("test1", self.msg1)
                except:
                    print("could not send to :  ", elt)
                i = i+1

    def chase_demand_1(self):
        self.msg1 = 'cosmoguirlande,chase,' + self.textbox_chase_speed.text() + ',' + self.textbox_chase_size.text()
        try:
            self.objs[0].connect(self.device[0],1883,60)
            self.objs[0].publish("test1", self.msg1)
        except:
            print("first strip on list not effective")
        if self.sync:
            i = 0
            #for elt in strip_configuration["guirlande"]:
            for elt in self.device:
                try:
                    self.objs[i].connect(elt,1883,60)
                    self.objs[i].publish("test1", self.msg1)
                except:
                    print("could not send to :  ", elt)
                i = i+1

    def comet_demand_1(self):
        self.msg1 = 'cosmoguirlande,comet,' + self.textbox_comet_speed.text() + ',' + self.textbox_comet_tail.text()
        try:
            self.objs[0].connect(self.device[0],1883,60)
            self.objs[0].publish("test1", self.msg1)
        except:
            print("first strip on list not effective")
        if self.sync:
            i = 0
            #for elt in strip_configuration["guirlande"]:
            for elt in self.device:
                try:
                    self.objs[i].connect(elt,1883,60)
                    self.objs[i].publish("test1", self.msg1)
                except:
                    print("could not send to :  ", elt)
                i = i+1

    def sparkle_demand_1(self):
        self.msg1 = 'cosmoguirlande,sparkle,' + self.textbox_sparkle_speed.text() + ',' + self.textbox_sparkle_num_sparkles.text()
        try:
            self.objs[0].connect(self.device[0],1883,60)
            self.objs[0].publish("test1", self.msg1)
        except:
            print("first strip on list not effective")
        if self.sync:
            i = 0
            #for elt in strip_configuration["guirlande"]:
            for elt in self.device:
                try:
                    self.objs[i].connect(elt,1883,60)
                    self.objs[i].publish("test1", self.msg1)
                except:
                    print("could not send to :  ", elt)
                i = i+1

    def pulse_demand_1(self):
        self.msg1 = 'cosmoguirlande,pulse,'+ self.textbox_pulse_period.text() + ',' + self.textbox_pulse_speed.text()
        try:
            self.objs[0].connect(self.device[0],1883,60)
            self.objs[0].publish("test1", self.msg1)
        except:
            print("first strip on list not effective")
        if self.sync:
            i = 0
            #for elt in strip_configuration["guirlande"]:
            for elt in self.device:
                try:
                    self.objs[i].connect(elt,1883,60)
                    self.objs[i].publish("test1", self.msg1)
                except:
                    print("could not send to :  ", elt)
                i = i+1

    def solid_demand_1(self):
        self.msg1 = 'cosmoguirlande,solid'
        try:
            self.objs[0].connect(self.device[0],1883,60)
            self.objs[0].publish("test1", self.msg1)
        except:
            print("first strip on list not effective")
        if self.sync:
            i = 0
            #for elt in strip_configuration["guirlande"]:
            for elt in self.device:
                try:
                    self.objs[i].connect(elt,1883,60)
                    self.objs[i].publish("test1", self.msg1)
                except:
                    print("could not send to :  ", elt)
                i = i+1

    def colorcycle_demand_1(self):
        self.msg1 = 'cosmoguirlande,colorcycle,'+ str((self.type_color11.currentText())) + ',' + str((self.type_color21.currentText()))
        try:
            self.objs[0].connect(self.device[0],1883,60)
            self.objs[0].publish("test1", self.msg1)
        except:
            print("first strip on list not effective")
        if self.sync:
            i = 0
            #for elt in strip_configuration["guirlande"]:
            for elt in self.device:
                try:
                    self.objs[i].connect(elt,1883,60)
                    self.objs[i].publish("test1", self.msg1)
                except:
                    print("could not send to :  ", elt)
                i = i+1

    def sync_demand(self, state):
        self.sync = not self.sync
        if self.sync:
            i = 0
            #for elt in strip_configuration["guirlande"]:
            for elt in self.device:
                try:
                    self.objs[i].connect(elt,1883,60)
                    self.objs[i].publish("test1", self.msg1)
                except:
                    print("could not send to :  ", elt)
                i = i+1

    def dancingPiScroll_demand_1(self):
        self.msg1 = 'cosmoguirlande,dancingPiScroll'
        try:
            self.objs[0].connect(self.device[0],1883,60)
            self.objs[0].publish("test1", self.msg1)
        except:
            print("first strip on list not effective")
        if self.sync:
            i = 0
            #for elt in strip_configuration["guirlande"]:
            for elt in self.device:
                try:
                    self.objs[i].connect(elt,1883,60)
                    self.objs[i].publish("test1", self.msg1)
                except:
                    print("could not send to :  ", elt)
                i = i+1

    def dancingPiEnergy_demand_1(self):
        self.msg1 = 'cosmoguirlande,dancingPiEnergy'
        try:
            self.objs[0].connect(self.device[0],1883,60)
            self.objs[0].publish("test1", self.msg1)
        except:
            print("first strip on list not effective")
        if self.sync:
            i = 0
            #for elt in strip_configuration["guirlande"]:
            for elt in self.device:
                try:
                    self.objs[i].connect(elt,1883,60)
                    self.objs[i].publish("test1", self.msg1)
                except:
                    print("could not send to :  ", elt)
                i = i+1

    def dancingPiSpectrum_demand_1(self):
        self.msg1 = 'cosmoguirlande,dancingPiSpectrum'
        try:
            self.objs[0].connect(self.device[0],1883,60)
            self.objs[0].publish("test1", self.msg1)
        except:
            print("first strip on list not effective")
        if self.sync:
            i = 0
            #for elt in strip_configuration["guirlande"]:
            for elt in self.device:
                try:
                    self.objs[i].connect(elt,1883,60)
                    self.objs[i].publish("test1", self.msg1)
                except:
                    print("could not send to :  ", elt)
                i = i+1

    def stop_dancingPiEnergy_demand_1(self):
        self.msg1 = 'cosmoguirlande,stop_dancingPiEnergy'
        try:
            self.objs[0].connect(self.device[0],1883,60)
            self.objs[0].publish("test1", self.msg1)
        except:
            print("first strip on list not effective")
        if self.sync:
            i = 0
            #for elt in strip_configuration["guirlande"]:
            for elt in self.device:
                try:
                    self.objs[i].connect(elt,1883,60)
                    self.objs[i].publish("test1", self.msg1)
                except:
                    print("could not send to :  ", elt)
                i = i+1

    def colorAll2Color_demand_1(self):
        self.msg1 = 'cosmoguirlande,colorAll2Color'
        try:
            self.objs[0].connect(self.device[0],1883,60)
            self.objs[0].publish("test1", self.msg1)
        except:
            print("first strip on list not effective")
        if self.sync:
            i = 0
            #for elt in strip_configuration["guirlande"]:
            for elt in self.device:
                try:
                    self.objs[i].connect(elt,1883,60)
                    self.objs[i].publish("test1", self.msg1)
                except:
                    print("could not send to :  ", elt)
                i = i+1

    def FadeInOut_demand_1(self):
        self.msg1 = 'cosmoguirlande,FadeInOut'
        try:
            self.objs[0].connect(self.device[0],1883,60)
            self.objs[0].publish("test1", self.msg1)
        except:
            print("first strip on list not effective")
        if self.sync:
            i = 0
            #for elt in strip_configuration["guirlande"]:
            for elt in self.device:
                try:
                    self.objs[i].connect(elt,1883,60)
                    self.objs[i].publish("test1", self.msg1)
                except:
                    print("could not send to :  ", elt)
                i = i+1

    def Strobe_demand_1(self):
        self.msg1 = 'cosmoguirlande,Strobe'
        try:
            self.objs[0].connect(self.device[0],1883,60)
            self.objs[0].publish("test1", self.msg1)
        except:
            print("first strip on list not effective")
        if self.sync:
            i = 0
            #for elt in strip_configuration["guirlande"]:
            for elt in self.device:
                try:
                    self.objs[i].connect(elt,1883,60)
                    self.objs[i].publish("test1", self.msg1)
                except:
                    print("could not send to :  ", elt)
                i = i+1

    def HalloweenEyes_demand_1(self):
        self.msg1 = 'cosmoguirlande,HalloweenEyes'
        try:
            self.objs[0].connect(self.device[0],1883,60)
            self.objs[0].publish("test1", self.msg1)
        except:
            print("first strip on list not effective")
        if self.sync:
            i = 0
            #for elt in strip_configuration["guirlande"]:
            for elt in self.device:
                try:
                    self.objs[i].connect(elt,1883,60)
                    self.objs[i].publish("test1", self.msg1)
                except:
                    print("could not send to :  ", elt)
                i = i+1

    def CylonBounce_demand_1(self):
        self.msg1 = 'cosmoguirlande,CylonBounce'
        try:
            self.objs[0].connect(self.device[0],1883,60)
            self.objs[0].publish("test1", self.msg1)
        except:
            print("first strip on list not effective")
        if self.sync:
            i = 0
            #for elt in strip_configuration["guirlande"]:
            for elt in self.device:
                try:
                    self.objs[i].connect(elt,1883,60)
                    self.objs[i].publish("test1", self.msg1)
                except:
                    print("could not send to :  ", elt)
                i = i+1

    def NewKITT_demand_1(self):
        self.msg1 = 'cosmoguirlande,NewKITT'
        try:
            self.objs[0].connect(self.device[0],1883,60)
            self.objs[0].publish("test1", self.msg1)
        except:
            print("first strip on list not effective")
        if self.sync:
            i = 0
            #for elt in strip_configuration["guirlande"]:
            for elt in self.device:
                try:
                    self.objs[i].connect(elt,1883,60)
                    self.objs[i].publish("test1", self.msg1)
                except:
                    print("could not send to :  ", elt)
                i = i+1

    def Twinkle_demand_1(self):
        self.msg1 = 'cosmoguirlande,Twinkle'
        try:
            self.objs[0].connect(self.device[0],1883,60)
            self.objs[0].publish("test1", self.msg1)
        except:
            print("first strip on list not effective")
        if self.sync:
            i = 0
            #for elt in strip_configuration["guirlande"]:
            for elt in self.device:
                try:
                    self.objs[i].connect(elt,1883,60)
                    self.objs[i].publish("test1", self.msg1)
                except:
                    print("could not send to :  ", elt)
                i = i+1

    def TwinkleRandom_demand_1(self):
        self.msg1 = 'cosmoguirlande,TwinkleRandom'
        try:
            self.objs[0].connect(self.device[0],1883,60)
            self.objs[0].publish("test1", self.msg1)
        except:
            print("first strip on list not effective")
        if self.sync:
            i = 0
            #for elt in strip_configuration["guirlande"]:
            for elt in self.device:
                try:
                    self.objs[i].connect(elt,1883,60)
                    self.objs[i].publish("test1", self.msg1)
                except:
                    print("could not send to :  ", elt)
                i = i+1

    def SnowSparkle_demand_1(self):
        self.msg1 = 'cosmoguirlande,SnowSparkle'
        try:
            self.objs[0].connect(self.device[0],1883,60)
            self.objs[0].publish("test1", self.msg1)
        except:
            print("first strip on list not effective")
        if self.sync:
            i = 0
            #for elt in strip_configuration["guirlande"]:
            for elt in self.device:
                try:
                    self.objs[i].connect(elt,1883,60)
                    self.objs[i].publish("test1", self.msg1)
                except:
                    print("could not send to :  ", elt)
                i = i+1

    def RunningLights_demand_1(self):
        self.msg1 = 'cosmoguirlande,*RunningLights'
        try:
            self.objs[0].connect(self.device[0],1883,60)
            self.objs[0].publish("test1", self.msg1)
        except:
            print("first strip on list not effective")
        if self.sync:
            i = 0
            #for elt in strip_configuration["guirlande"]:
            for elt in self.device:
                try:
                    self.objs[i].connect(elt,1883,60)
                    self.objs[i].publish("test1", self.msg1)
                except:
                    print("could not send to :  ", elt)
                i = i+1

    def colorWipe_demand_1(self):
        self.msg1 = 'cosmoguirlande,colorWipe'
        try:
            self.objs[0].connect(self.device[0],1883,60)
            self.objs[0].publish("test1", self.msg1)
        except:
            print("first strip on list not effective")
        if self.sync:
            i = 0
            #for elt in strip_configuration["guirlande"]:
            for elt in self.device:
                try:
                    self.objs[i].connect(elt,1883,60)
                    self.objs[i].publish("test1", self.msg1)
                except:
                    print("could not send to :  ", elt)
                i = i+1

    def theaterChaseRainbow_demand_1(self):
        self.msg1 = 'cosmoguirlande,theaterChaseRainbow'
        try:
            self.objs[0].connect(self.device[0],1883,60)
            self.objs[0].publish("test1", self.msg1)
        except:
            print("first strip on list not effective")
        if self.sync:
            i = 0
            #for elt in strip_configuration["guirlande"]:
            for elt in self.device:
                try:
                    self.objs[i].connect(elt,1883,60)
                    self.objs[i].publish("test1", self.msg1)
                except:
                    print("could not send to :  ", elt)
                i = i+1

    def Fire_demand_1(self):
        self.msg1 = 'cosmoguirlande,Fire'
        try:
            self.objs[0].connect(self.device[0],1883,60)
            self.objs[0].publish("test1", self.msg1)
        except:
            print("first strip on list not effective")
        if self.sync:
            i = 0
            #for elt in strip_configuration["guirlande"]:
            for elt in self.device:
                try:
                    self.objs[i].connect(elt,1883,60)
                    self.objs[i].publish("test1", self.msg1)
                except:
                    print("could not send to :  ", elt)
                i = i+1

    def FireCustom_demand_1(self):
        self.msg1 = 'cosmoguirlande,FireCustom'
        try:
            self.objs[0].connect(self.device[0],1883,60)
            self.objs[0].publish("test1", self.msg1)
        except:
            print("first strip on list not effective")
        if self.sync:
            i = 0
            #for elt in strip_configuration["guirlande"]:
            for elt in self.device:
                try:
                    self.objs[i].connect(elt,1883,60)
                    self.objs[i].publish("test1", self.msg1)
                except:
                    print("could not send to :  ", elt)
                i = i+1

    def FadeInOut_demand_1(self):
        self.msg1 = 'cosmoguirlande,FadeInOut'
        try:
            self.objs[0].connect(self.device[0],1883,60)
            self.objs[0].publish("test1", self.msg1)
        except:
            print("first strip on list not effective")
        if self.sync:
            i = 0
            #for elt in strip_configuration["guirlande"]:
            for elt in self.device:
                try:
                    self.objs[i].connect(elt,1883,60)
                    self.objs[i].publish("test1", self.msg1)
                except:
                    print("could not send to :  ", elt)
                i = i+1

    def fadeToBlack_demand_1(self):
        self.msg1 = 'cosmoguirlande,fadeToBlack'
        try:
            self.objs[0].connect(self.device[0],1883,60)
            self.objs[0].publish("test1", self.msg1)
        except:
            print("first strip on list not effective")
        if self.sync:
            i = 0
            #for elt in strip_configuration["guirlande"]:
            for elt in self.device:
                try:
                    self.objs[i].connect(elt,1883,60)
                    self.objs[i].publish("test1", self.msg1)
                except:
                    print("could not send to :  ", elt)
                i = i+1

    def BouncingBalls_demand_1(self):
        self.msg1 = 'cosmoguirlande,*BouncingBalls'
        try:
            self.objs[0].connect(self.device[0],1883,60)
            self.objs[0].publish("test1", self.msg1)
        except:
            print("first strip on list not effective")
        if self.sync:
            i = 0
            #for elt in strip_configuration["guirlande"]:
            for elt in self.device:
                try:
                    self.objs[i].connect(elt,1883,60)
                    self.objs[i].publish("test1", self.msg1)
                except:
                    print("could not send to :  ", elt)
                i = i+1

    def BouncingColoredBalls_demand_1(self):
        self.msg1 = 'cosmoguirlande,*BouncingColoredBalls'
        try:
            self.objs[0].connect(self.device[0],1883,60)
            self.objs[0].publish("test1", self.msg1)
        except:
            print("first strip on list not effective")
        if self.sync:
            i = 0
            #for elt in strip_configuration["guirlande"]:
            for elt in self.device:
                try:
                    self.objs[i].connect(elt,1883,60)
                    self.objs[i].publish("test1", self.msg1)
                except:
                    print("could not send to :  ", elt)
                i = i+1

    def meteorRain_demand_1(self):
        self.msg1 = 'cosmoguirlande,meteorRain'
        try:
            self.objs[0].connect(self.device[0],1883,60)
            self.objs[0].publish("test1", self.msg1)
        except:
            print("first strip on list not effective")
        if self.sync:
            i = 0
            #for elt in strip_configuration["guirlande"]:
            for elt in self.device:
                try:
                    self.objs[i].connect(elt,1883,60)
                    self.objs[i].publish("test1", self.msg1)
                except:
                    print("could not send to :  ", elt)
                i = i+1

    def Matrix_demand_1(self):
        self.msg1 = 'cosmoguirlande,Matrix'
        try:
            self.objs[0].connect(self.device[0],1883,60)
            self.objs[0].publish("test1", self.msg1)
        except:
            print("first strip on list not effective")
        if self.sync:
            i = 0
            #for elt in strip_configuration["guirlande"]:
            for elt in self.device:
                try:
                    self.objs[i].connect(elt,1883,60)
                    self.objs[i].publish("test1", self.msg1)
                except:
                    print("could not send to :  ", elt)
                i = i+1
    
    def Drain_demand_1(self):
        self.msg1 = 'cosmoguirlande,*Drain'
        try:
            self.objs[0].connect(self.device[0],1883,60)
            self.objs[0].publish("test1", self.msg1)
        except:
            print("first strip on list not effective")
        if self.sync:
            i = 0
            #for elt in strip_configuration["guirlande"]:
            for elt in self.device:
                try:
                    self.objs[i].connect(elt,1883,60)
                    self.objs[i].publish("test1", self.msg1)
                except:
                    print("could not send to :  ", elt)
                i = i+1
  
    def Pancake_demand_1(self):
        self.msg1 = 'cosmoguirlande,Pancake'
        try:
            self.objs[0].connect(self.device[0],1883,60)
            self.objs[0].publish("test1", self.msg1)
        except:
            print("first strip on list not effective")
        if self.sync:
            i = 0
            #for elt in strip_configuration["guirlande"]:
            for elt in self.device:
                try:
                    self.objs[i].connect(elt,1883,60)
                    self.objs[i].publish("test1", self.msg1)
                except:
                    print("could not send to :  ", elt)
                i = i+1
     
    def HeartBeat_demand_1(self):
        self.msg1 = 'cosmoguirlande,HeartBeat'
        try:
            self.objs[0].connect(self.device[0],1883,60)
            self.objs[0].publish("test1", self.msg1)
        except:
            print("first strip on list not effective")
        if self.sync:
            i = 0
            #for elt in strip_configuration["guirlande"]:
            for elt in self.device:
                try:
                    self.objs[i].connect(elt,1883,60)
                    self.objs[i].publish("test1", self.msg1)
                except:
                    print("could not send to :  ", elt)
                i = i+1
      
    def rainbowGlitter_demand_1(self):
        self.msg1 = 'cosmoguirlande,rainbowGlitter'
        try:
            self.objs[0].connect(self.device[0],1883,60)
            self.objs[0].publish("test1", self.msg1)
        except:
            print("first strip on list not effective")
        if self.sync:
            i = 0
            #for elt in strip_configuration["guirlande"]:
            for elt in self.device:
                try:
                    self.objs[i].connect(elt,1883,60)
                    self.objs[i].publish("test1", self.msg1)
                except:
                    print("could not send to :  ", elt)
                i = i+1

    def Confetti_demand_1(self):
        self.msg1 = 'cosmoguirlande,Confetti'
        try:
            self.objs[0].connect(self.device[0],1883,60)
            self.objs[0].publish("test1", self.msg1)
        except:
            print("first strip on list not effective")
        if self.sync:
            i = 0
            #for elt in strip_configuration["guirlande"]:
            for elt in self.device:
                try:
                    self.objs[i].connect(elt,1883,60)
                    self.objs[i].publish("test1", self.msg1)
                except:
                    print("could not send to :  ", elt)
                i = i+1
   
    def Sinelon_demand_1(self):
        self.msg1 = 'cosmoguirlande,Sinelon'
        try:
            self.objs[0].connect(self.device[0],1883,60)
            self.objs[0].publish("test1", self.msg1)
        except:
            print("first strip on list not effective")
        if self.sync:
            i = 0
            #for elt in strip_configuration["guirlande"]:
            for elt in self.device:
                try:
                    self.objs[i].connect(elt,1883,60)
                    self.objs[i].publish("test1", self.msg1)
                except:
                    print("could not send to :  ", elt)
                i = i+1
 
    def BPM_demand_1(self):
        subprocess.Popen(args='python start_display_remote_ssh.py', shell=True)

        '''self.msg1 = 'cosmoguirlande,**BPM'
        try:
            self.objs[0].connect(self.device[0],1883,60)
            self.objs[0].publish("test1", self.msg1)
        except:
            print("first strip on list not effective")
        if self.sync:
            i = 0
            for elt in strip_configuration["guirlande"]:
                try:
                    self.objs[i].connect(elt["IP"],1883,60)
                    self.objs[i].publish("test1", self.msg1)
                except:
                    print("could not send to :  ", elt["IP"])
                i = i+1'''
 
    # Slider Buttons functions
    def slider_R1(self, R1):
        self.msg1 = 'cosmoguirlande,R,' + str((R1))
        try:
            self.objs[0].connect(self.device[0],1883,60)
            self.objs[0].publish("test1", self.msg1)
        except:
            print("first strip on list not effective")
        if self.sync:
            i = 0
            #for elt in strip_configuration["guirlande"]:
            for elt in self.device:
                try:
                    self.objs[i].connect(elt,1883,60)
                    self.objs[i].publish("test1", self.msg1)
                except:
                    print("could not connect to :  ", elt)
                i = i+1

    def slider_G1(self, G1):
        self.msg1 = 'cosmoguirlande,G,' + str((G1))
        try:
            self.objs[0].connect(self.device[0],1883,60)
            self.objs[0].publish("test1", self.msg1)
        except:
            print("first strip on list not effective")
        if self.sync:
            i = 0
            #for elt in strip_configuration["guirlande"]:
            for elt in self.device:
                try:
                    self.objs[i].connect(elt,1883,60)
                    self.objs[i].publish("test1", self.msg1)
                except:
                    print("could not connect to :  ", elt)
                i = i+1

    def slider_B1(self, B1):
        self.msg1 = 'cosmoguirlande,B,' + str((B1))
        try:
            self.objs[0].connect(self.device[0],1883,60)
            self.objs[0].publish("test1", self.msg1)
        except:
            print("first strip on list not effective")
        if self.sync:
            i = 0
            #for elt in strip_configuration["guirlande"]:
            for elt in self.device:
                try:
                    self.objs[i].connect(elt,1883,60)
                    self.objs[i].publish("test1", self.msg1)
                except:
                    print("could not connect to :  ", elt)
                i = i+1

    def slider_W1(self, W1):
        self.msg1 = 'cosmoguirlande,W,' + str((W1))
        try:
            self.objs[0].connect(self.device[0],1883,60)
            self.objs[0].publish("test1", self.msg1)
        except:
            print("first strip on list not effective")
        if self.sync:
            i = 0
            #for elt in strip_configuration["guirlande"]:
            for elt in self.device:
                try:
                    self.objs[i].connect(elt,1883,60)
                    self.objs[i].publish("test1", self.msg1)
                except:
                    print("could not connect to :  ", elt)
                i = i+1

    def on_click_ip(self):
        self.IPValue = self.textbox_IP.text()
        self.vnc_window_1 = VNC_Window(self.IPValue)
        self.vnc_window_1.start()

    def on_click_port(self):
        PortValue = self.textbox_port.text()

    def on_click_strombo_frequency(self):
        Strombo_frequency = self.textbox_port.text()

    #########################################################################################################Strip 2
    def color2_change_demand21(self):
        print("selection changed ", self.type_color22.currentText())
        self.msg2 = 'cosmoguirlande,color1,' + str(( self.type_color21.currentText()))
        self.objs[1].connect(self.device[1],1883,60)
        self.objs[1].publish("test1", self.msg2)

    def color2_change_demand22(self):
        print("selection changed ", self.type_color22.currentText())
        self.msg2 = 'cosmoguirlande,color2,' + str(( self.type_color22.currentText()))
        self.objs[1].connect(self.device[1],1883,60)
        self.objs[1].publish("test1", self.msg2)

    def on_click_ip_2(self):
        self.IPValue_2 = self.textbox_IP_2.text()
        self.vnc_window_2 = VNC_Window(self.IPValue_2)
        self.vnc_window_2.start()

    def on_click_port_2(self):
        PortValue_2 = self.textbox_port_2.text()

    def on_click_strombo_2_frequency(self):
        Strombo_frequency = self.textbox_port.text()
        QMessageBox.question(self, 'Message - pythonspot.com', "You typed: " + Strombo_frequency, QMessageBox.Ok,
                             QMessageBox.Ok)
        self.textbox.setText("")

    def blackout_demand_2(self):
        self.msg2 ='cosmoguirlande,blackout'
        self.objs[1].connect(self.device[1],1883,60)
        self.objs[1].publish("test1", self.msg2)

    def rainbow_demand_2(self):
        self.msg2 = 'cosmoguirlande,rainbow'
        self.objs[1].connect(self.device[1],1883,60)
        self.objs[1].publish("test1", self.msg2)

    def strombo_demand_2(self):
        self.msg2 = 'cosmoguirlande,strombo'
        self.objs[1].connect(self.device[1],1883,60)
        self.objs[1].publish("test1", self.msg2)

    def chase_demand_2(self):
        self.msg2 = 'cosmoguirlande,chase' +',' + self.textbox_chase_speed_2.text() + ',' + self.textbox_chase_size_2.text()
        self.objs[1].connect(self.device[1],1883,60)
        self.objs[1].publish("test1", self.msg2)

    def comet_demand_2(self):
        self.msg2 = 'cosmoguirlande,comet'+ ',' +self.textbox_comet_speed_2.text() + ',' + self.textbox_comet_tail_2.text()
        self.objs[1].connect(self.device[1],1883,60)
        self.objs[1].publish("test1", self.msg2)

    def sparkle_demand_2(self):
        self.msg2 = 'cosmoguirlande,sparkle' +',' + self.textbox_sparkle_speed_2.text() + ',' + self.textbox_sparkle_num_sparkles_2.text()
        self.objs[1].connect(self.device[1],1883,60)
        self.objs[1].publish("test1", self.msg2)

    def pulse_demand_2(self):
        self.msg2 = 'cosmoguirlande,pulse'  +',' + self.textbox_pulse_period_2.text() + ',' + self.textbox_pulse_speed_2.text() 
        self.objs[1].connect(self.device[1],1883,60)
        self.objs[1].publish("test1", self.msg2)

    def solid_demand_2(self):
        self.msg2 = 'cosmoguirlande,solid'
        self.objs[1].connect(self.device[1],1883,60)
        self.objs[1].publish("test1", self.msg2)

    def colorcycle_demand_2(self):
        self.msg2 = 'cosmoguirlande,colorcycle'
        self.objs[1].connect(self.device[1],1883,60)
        self.objs[1].publish("test1", self.msg2)

    def sync_demand_2(self):
        self.msg2 = 'cosmoguirlande,sync'
        self.objs[1].connect(self.device[1],1883,60)
        self.objs[1].publish("test1", self.msg2)

    def dancingPiScroll_demand_2(self):
        self.msg2 = 'cosmoguirlande,dancingPiScroll'
        self.objs[1].connect(self.device[1],1883,60)
        self.objs[1].publish("test1", self.msg2)

    def dancingPiEnergy_demand_2(self):
        self.msg2 = 'cosmoguirlande,dancingPiEnergy'
        self.objs[1].connect(self.device[1],1883,60)
        self.objs[1].publish("test1", self.msg2)

    def dancingPiSpectrum_demand_2(self):
        self.msg2 = 'cosmoguirlande,dancingPiSpectrum'
        self.objs[1].connect(self.device[1],1883,60)
        self.objs[1].publish("test1", self.msg2)

    def stop_dancingPiEnergy_demand_2(self):
        self.msg2 = 'cosmoguirlande,stop_dancingPiEnergy'
        self.objs[1].connect(self.device[1],1883,60)
        self.objs[1].publish("test1", self.msg2)

    def stop_dancingPiSpectrum_demand_2(self):
        self.msg2 = 'cosmoguirlande,stop_dancingPiSpectrum'
        self.objs[1].connect(self.device[1],1883,60)
        self.objs[1].publish("test1", self.msg2)

    def stop_dancingPiScroll_demand_2(self):
        self.msg2 = 'cosmoguirlande,stop_dancingPiScroll'
        self.objs[1].connect(self.device[1],1883,60)
        self.objs[1].publish("test1", self.msg2)

    # Slider Buttons functions
    def slider_R2(self, R2):
        self.msg2 = 'cosmoguirlande,R,' + str((R2))
        self.objs[1].connect(self.device[1],1883,60)
        self.objs[1].publish("test1", self.msg2)

    def slider_G2(self, G2):
        self.msg2 = 'cosmoguirlande,G,' + str((G2))
        self.objs[1].connect(self.device[1],1883,60)
        self.objs[1].publish("test1", self.msg2)

    def slider_B2(self, B2):
        self.msg2 = 'cosmoguirlande,B,' + str((B2))
        self.objs[1].connect(self.device[1],1883,60)
        self.objs[1].publish("test1", self.msg2)

    def slider_W2(self, W2):
        self.msg2 = 'cosmoguirlande,W,' + str((W2))
        self.objs[1].connect(self.device[1],1883,60)
        self.objs[1].publish("test1", self.msg2)
    #########################################################################################################Strip 3
    def on_click_strombo_3_frequency(self):
        Strombo_frequency = self.textbox_port.text()
        QMessageBox.question(self, 'Message - pythonspot.com', "You typed: " + Strombo_frequency, QMessageBox.Ok,
                             QMessageBox.Ok)
        self.textbox.setText("")

    def color3_change_demand31(self):
        print("selection changed ", self.type_color31.currentText())
        self.msg3 = 'cosmoguirlande,color1,' + str(( self.type_color31.currentText()))
        self.objs[2].connect(self.device[2],1883,60)
        self.objs[2].publish("test1", self.msg3)
        print("change color 3 method 1")

    def color3_change_demand32(self):
        print("selection changed ", self.type_color32.currentText())
        self.msg3 = 'cosmoguirlande,color2,' + str(( self.type_color32.currentText()))
        self.objs[2].connect(self.device[2],1883,60)
        self.objs[2].publish("test1", self.msg3)
        print("change color 3 method 2")

    def on_click_ip_3(self):
        self.IPValue_3 = self.textbox_IP_3.text()
        self.vnc_window_3 = VNC_Window(self.IPValue_3)
        self.vnc_window_3.start()

    def on_click_port_3(self):
        PortValue_3 = self.textbox_port_3.text()

    def blackout_demand_3(self):
        self.msg3 ='cosmoguirlande,blackout'
        self.objs[2].connect(self.device[2],1883,60)
        self.objs[2].publish("test1", self.msg3)

    def rainbow_demand_3(self):
        self.msg3 = 'cosmoguirlande,rainbow'
        self.objs[2].connect(self.device[2],1883,60)
        self.objs[2].publish("test1", self.msg3)

    def strombo_demand_3(self):
        self.msg3 = 'cosmoguirlande,strombo'
        self.objs[2].connect(self.device[2],1883,60)
        self.objs[2].publish("test1", self.msg3)

    def chase_demand_3(self):
        self.msg3 = 'cosmoguirlande,chase'+ ',' +self.textbox_chase_speed_3.text() + ',' + self.textbox_chase_size_3.text()
        self.objs[2].connect(self.device[2],1883,60)
        self.objs[2].publish("test1", self.msg3)

    def comet_demand_3(self):
        self.msg3 = 'cosmoguirlande,comet' +',' + self.textbox_comet_speed_3.text() + ',' + self.textbox_comet_tail_3.text()
        self.objs[2].connect(self.device[2],1883,60)
        self.objs[2].publish("test1", self.msg3)

    def sparkle_demand_3(self):
        self.msg3 = 'cosmoguirlande,sparkle'+',' + self.textbox_sparkle_speed_3.text() + ',' + self.textbox_sparkle_num_sparkles_3.text()
        self.objs[2].connect(self.device[2],1883,60)
        self.objs[2].publish("test1", self.msg3)

    def pulse_demand_3(self):
        self.msg3 = 'cosmoguirlande,pulse'+ ',' +self.textbox_pulse_period_3.text() + ',' + self.textbox_pulse_speed_3.text()
        self.objs[2].connect(self.device[2],1883,60)
        self.objs[2].publish("test1", self.msg3)

    def solid_demand_3(self):
        self.msg3 = 'cosmoguirlande,solid'
        self.objs[2].connect(self.device[2],1883,60)
        self.objs[2].publish("test1", self.msg3)

    def colorcycle_demand_3(self):
        self.msg3 = 'cosmoguirlande,colorcycle'
        self.objs[2].connect(self.device[2],1883,60)
        self.objs[2].publish("test1", self.msg3)

    def sync_demand_3(self):
        self.msg3 = 'cosmoguirlande,sync'
        self.objs[2].connect(self.device[2],1883,60)
        self.objs[2].publish("test1", self.msg3)

    def dancingPiScroll_demand_3(self):
        self.msg3 = 'cosmoguirlande,dancingPiScroll'
        self.objs[2].connect(self.device[2],1883,60)
        self.objs[2].publish("test1", self.msg3)

    def dancingPiEnergy_demand_3(self):
        self.msg3 = 'cosmoguirlande,dancingPiEnergy'
        self.objs[2].connect(self.device[2],1883,60)
        self.objs[2].publish("test1", self.msg3)

    def dancingPiSpectrum_demand_3(self):
        self.msg3 = 'cosmoguirlande,dancingPiSpectrum'
        self.objs[2].connect(self.device[2],1883,60)
        self.objs[2].publish("test1", self.msg3)

    def stop_dancingPiEnergy_demand_3(self):
        self.msg3 = 'cosmoguirlande,stop_dancingPiEnergy'
        self.objs[2].connect(self.device[2],1883,60)
        self.objs[2].publish("test1", self.msg3)

    def stop_dancingPiSpectrum_demand_3(self):
        self.msg3 = 'cosmoguirlande,stop_dancingPiSpectrum'
        self.objs[2].connect(self.device[2],1883,60)
        self.objs[2].publish("test1", self.msg3)

    def stop_dancingPiScroll_demand_3(self):
        self.msg3 = 'cosmoguirlande,stop_dancingPiScroll'
        self.objs[2].connect(self.device[2],1883,60)
        self.objs[2].publish("test1", self.msg3)

    # Slider Buttons functions
    def slider_R3(self, R3):
        self.msg3 = 'cosmoguirlande,R,' + str((R3))
        self.objs[2].connect(self.device[2],1883,60)
        self.objs[2].publish("test1", self.msg3)

    def slider_G3(self, G3):                             
        self.msg3 = 'cosmoguirlande,G,' + str((G3))
        self.objs[2].connect(self.device[2],1883,60)
        self.objs[2].publish("test1", self.msg3)

    def slider_B3(self, B3):
        self.msg3 = 'cosmoguirlande,B,' + str((B3))
        self.objs[2].connect(self.device[2],1883,60)
        self.objs[2].publish("test1", self.msg3)

    def slider_W3(self, W3):
        self.msg3 = 'cosmoguirlande,W,' + str((W3))
        self.objs[2].connect(self.device[2],1883,60)
        self.objs[2].publish("test1", self.msg3)              

    #########################################################################################################Strip 4
    def color4_change_demand41(self):
        print("selection changed ", self.type_color44.currentText())
        self.msg4 = 'cosmoguirlande,color1,' + str((self.type_color41.currentText()))
        self.objs[3].connect(self.device[3],1883,60)
        self.objs[3].publish("test1", self.msg4)

    def color4_change_demand42(self):
        print("selection changed ", self.type_color44.currentText())
        self.msg4 = 'cosmoguirlande,color2,' + str((self.type_color42.currentText()))
        self.objs[3].connect(self.device[3],1883,60)
        self.objs[3].publish("test1", self.msg4)

    def on_click_ip_4(self):
        self.IPValue_4 = self.textbox_IP_4.text()
        self.vnc_window_4 = VNC_Window(self.IPValue_4)
        self.vnc_window_4.start()

    def on_click_port_4(self):
        PortValue_4 = self.textbox_port_4.text()

    def on_click_strombo_4_frequency(self):
        Strombo_frequency = self.textbox_port.text()
        QMessageBox.question(self, 'Message - pythonspot.com', "You typed: " + Strombo_frequency, QMessageBox.Ok,
                             QMessageBox.Ok)
        self.textbox.setText("")

    def blackout_demand_4(self):
        self.msg4 = 'cosmoguirlande,blackout'
        self.objs[3].connect(self.device[3],1883,60)
        self.objs[3].publish("test1", self.msg4)

    def rainbow_demand_4(self):
        self.msg4 = 'cosmoguirlande,rainbow'
        self.objs[3].connect(self.device[3],1883,60)
        self.objs[3].publish("test1", self.msg4)

    def strombo_demand_4(self):
        self.msg4 = 'cosmoguirlande,strombo'
        self.objs[3].connect(self.device[3],1883,60)
        self.objs[3].publish("test1", self.msg4)

    def theaterChase_demand_4(self):
        self.msg4 = 'cosmoguirlande,theaterChase'+ self.textbox_chase_speed_4.text() + ',' + self.textbox_chase_size_4.text()
        self.objs[3].connect(self.device[3],1883,60)
        self.objs[3].publish("test1", self.msg4)

    def theaterChaseRainbow_demand_4(self):
        self.msg4 = 'cosmoguirlande,theaterChaseRainbow'
        self.objs[3].connect(self.device[3],1883,60)
        self.objs[3].publish("test1", self.msg4)

    def multiColorWipe_demand_4(self):
        self.msg4 = 'cosmoguirlande,multiColorWipe'
        self.objs[3].connect(self.device[3],1883,60)
        self.objs[3].publish("test1", self.msg4)

    def sync_demand_4(self):
        self.msg4 = 'cosmoguirlande,sync'
        self.objs[3].connect(self.device[3],1883,60)
        self.objs[3].publish("test1", self.msg4)

    def dancingPiScroll_demand_4(self):
        self.msg4 = 'cosmoguirlande,dancingPiScroll'
        self.objs[3].connect(self.device[3],1883,60)
        self.objs[3].publish("test1", self.msg4)

    def dancingPiEnergy_demand_4(self):
        self.msg4 = 'cosmoguirlande,dancingPiEnergy'
        self.objs[3].connect(self.device[3],1883,60)
        self.objs[3].publish("test1", self.msg4)

    def dancingPiSpectrum_demand_4(self):
        self.msg4 = 'cosmoguirlande,dancingPiSpectrum'
        self.objs[3].connect(self.device[3],1883,60)
        self.objs[3].publish("test1", self.msg4)

    def stop_dancingPiEnergy_demand_4(self):
        self.msg4 = 'cosmoguirlande,stop_dancingPiEnergy'
        self.objs[3].connect(self.device[3],1883,60)
        self.objs[3].publish("test1", self.msg4)

    def stop_dancingPiSpectrum_demand_4(self):
        self.msg4 = 'cosmoguirlande,stop_dancingPiSpectrum'
        self.objs[3].connect(self.device[3],1883,60)
        self.objs[3].publish("test1", self.msg4)

    def stop_dancingPiScroll_demand_4(self):
        self.msg4 = 'cosmoguirlande,stop_dancingPiScroll'
        self.objs[3].connect(self.device[3],1883,60)
        self.objs[3].publish("test1", self.msg4)

    def strombo_demand_4(self):
        self.msg4 = 'cosmoguirlande,strombo'
        self.objs[3].connect(self.device[3],1883,60)
        self.objs[3].publish("test1", self.msg4)

    def chase_demand_4(self):
        self.msg4 = 'cosmoguirlande,chase'+',' + self.textbox_chase_speed_4.text() + ',' + self.textbox_chase_size_4.text()
        self.objs[3].connect(self.device[3],1883,60)
        self.objs[3].publish("test1", self.msg4)

    def comet_demand_4(self):
        self.msg4 = 'cosmoguirlande,comet' +',' + self.textbox_comet_speed_4.text() + ',' + self.textbox_comet_tail_4.text()
        self.objs[3].connect(self.device[3],1883,60)
        self.objs[3].publish("test1", self.msg4)

    def sparkle_demand_4(self):
        self.msg4 = 'cosmoguirlande,sparkle'+',' + self.textbox_sparkle_speed_4.text() + ',' + self.textbox_sparkle_num_sparkles_4.text()
        self.objs[3].connect(self.device[3],1883,60)
        self.objs[3].publish("test1", self.msg4)

    def pulse_demand_4(self):
        self.msg4 = 'cosmoguirlande,pulse'+',' + self.textbox_pulse_period_4.text() + ',' + self.textbox_pulse_speed_4.text()
        self.objs[3].connect(self.device[3],1883,60)
        self.objs[3].publish("test1", self.msg4)

    def solid_demand_4(self):
        self.msg4 = 'cosmoguirlande,solid'
        self.objs[3].connect(self.device[3],1883,60)
        self.objs[3].publish("test1", self.msg4)

    def colorcycle_demand_4(self):
        self.msg4 = 'cosmoguirlande,colorcycle'
        self.objs[3].connect(self.device[3],1883,60)
        self.objs[3].publish("test1", self.msg4)

    # Slider Buttons functions
    def slider_R4(self, R4):
        self.msg4 = 'cosmoguirlande,R,' + str((R4))
        self.objs[3].connect(self.device[3],1883,60)
        self.objs[3].publish("test1", self.msg4)

    def slider_G4(self, G4):
        self.msg4 = 'cosmoguirlande,G,' + str((G4))
        self.objs[3].connect(self.device[3],1883,60)
        self.objs[3].publish("test1", self.msg4)

    def slider_B4(self, B4):
        self.msg4 = 'cosmoguirlande,B,' + str((B4))
        self.objs[3].connect(self.device[3],1883,60)
        self.objs[3].publish("test1", self.msg4)

    def slider_W4(self, W4):
        self.msg4 = 'cosmoguirlande,W,' + str((W4))
        self.objs[3].connect(self.device[3],1883,60)
        self.objs[3].publish("test1", self.msg4)

    #########################################################################################################Strip 5
    def color5_change_demand51(self):
        print("selection changed ", self.type_color55.currentText())
        self.msg5 = 'cosmoguirlande,color1,' + str(( self.type_color51.currentText()))
        self.objs[4].connect(self.device[4],1883,60)
        self.objs[4].publish("test1", self.msg5)

    def color5_change_demand52(self):
        print("selection changed ", self.type_color55.currentText())
        self.msg5 = 'cosmoguirlande,color2,' + str(( self.type_color52.currentText()))
        self.objs[4].connect(self.device[4],1883,60)
        self.objs[4].publish("test1", self.msg5)

    def on_click_ip_5(self):
        self.IPValue_5 = self.textbox_IP_5.text()
        self.vnc_window_5 = VNC_Window(self.IPValue_5)
        self.vnc_window_5.start()

    def on_click_port_5(self):
        PortValue_5 = self.textbox_port_5.text()

    def on_click_strombo_5_frequency(self):
        Strombo_frequency = self.textbox_port.text()
        QMessageBox.question(self, 'Message - pythonspot.com', "You typed: " + Strombo_frequency, QMessageBox.Ok,
                             QMessageBox.Ok)
        self.textbox.setText("")

    def blackout_demand_5(self):
        self.msg5 = 'cosmoguirlande,blackout'
        self.objs[4].connect(self.device[4],1883,60)
        self.objs[4].publish("test1", self.msg5)

    def rainbow_demand_5(self):
        self.msg5 = 'cosmoguirlande,rainbow'
        self.objs[4].connect(self.device[4],1883,60)
        self.objs[4].publish("test1", self.msg5)

    def strombo_demand_5(self):
        self.msg5 = 'cosmoguirlande,strombo'
        self.objs[4].connect(self.device[4],1883,60)
        self.objs[4].publish("test1", self.msg5)

    def theaterChase_demand_5(self):
        self.msg5 = 'cosmoguirlande,theaterChase'+ self.textbox_chase_speed_5.text() + ',' + self.textbox_chase_size_6.text()
        self.objs[4].connect(self.device[4],1883,60)
        self.objs[4].publish("test1", self.msg5)

    def theaterChaseRainbow_demand_5(self):
        self.msg5 = 'cosmoguirlande,theaterChaseRainbow'
        self.objs[4].connect(self.device[4],1883,60)
        self.objs[4].publish("test1", self.msg5)

    def multiColorWipe_demand_5(self):
        self.msg5 = 'cosmoguirlande,multiColorWipe'
        self.objs[4].connect(self.device[4],1883,60)
        self.objs[4].publish("test1", self.msg5)

    def sync_demand_5(self):
        self.msg5 = 'cosmoguirlande,sync'
        self.objs[4].connect(self.device[4],1883,60)
        self.objs[4].publish("test1", self.msg5)

    def strombo_demand_5(self):
        self.msg5 = 'cosmoguirlande,strombo'
        self.objs[4].connect(self.device[4],1883,60)
        self.objs[4].publish("test1", self.msg5)

    def chase_demand_5(self):
        self.msg5 = 'cosmoguirlande,chase'+',' + self.textbox_chase_speed_6.text() + ',' + self.textbox_chase_size_6.text()
        self.objs[4].connect(self.device[4],1883,60)
        self.objs[4].publish("test1", self.msg5)

    def comet_demand_5(self):
        self.msg5 = 'cosmoguirlande,comet' +',' + self.textbox_comet_speed_5.text() + ',' + self.textbox_comet_tail_5.text()
        self.objs[4].connect(self.device[4],1883,60)
        self.objs[4].publish("test1", self.msg5)

    def sparkle_demand_5(self):
        self.msg5 = 'cosmoguirlande,sparkle' +',' + self.textbox_sparkle_speed_5.text() + ',' + self.textbox_sparkle_num_sparkles_5.text()
        self.objs[4].connect(self.device[4],1883,60)
        self.objs[4].publish("test1", self.msg5)

    def pulse_demand_5(self):
        self.msg5 = 'cosmoguirlande,pulse'+',' + self.textbox_pulse_period_5.text() + ',' + self.textbox_pulse_speed_5.text()
        self.objs[4].connect(self.device[4],1883,60)
        self.objs[4].publish("test1", self.msg5)

    def solid_demand_5(self):
        self.msg5 = 'cosmoguirlande,solid'
        self.objs[4].connect(self.device[4],1883,60)
        self.objs[4].publish("test1", self.msg5)

    def colorcycle_demand_5(self):
        self.msg5 = 'cosmoguirlande,colorcycle'
        self.objs[4].connect(self.device[4],1883,60)
        self.objs[4].publish("test1", self.msg5)

    def dancingPiScroll_demand_5(self):
        self.msg5 = 'cosmoguirlande,dancingPiScroll'
        self.objs[4].connect(self.device[4],1883,60)
        self.objs[4].publish("test1", self.msg5)

    def dancingPiEnergy_demand_5(self):
        self.msg5 = 'cosmoguirlande,dancingPiEnergy'
        self.objs[4].connect(self.device[4],1883,60)
        self.objs[4].publish("test1", self.msg5)

    def dancingPiSpectrum_demand_5(self):
        self.msg5 = 'cosmoguirlande,dancingPiSpectrum'
        self.objs[4].connect(self.device[4],1883,60)
        self.objs[4].publish("test1", self.msg5)

    def stop_dancingPiEnergy_demand_5(self):
        self.msg5 = 'cosmoguirlande,stop_dancingPiEnergy'
        self.objs[4].connect(self.device[4],1883,60)
        self.objs[4].publish("test1", self.msg5)

    def stop_dancingPiSpectrum_demand_5(self):
        self.msg5 = 'cosmoguirlande,stop_dancingPiSpectrum'
        self.objs[4].connect(self.device[4],1883,60)
        self.objs[4].publish("test1", self.msg5)

    def stop_dancingPiScroll_demand_5(self):
        self.msg5 = 'cosmoguirlande,stop_dancingPiScroll'
        self.objs[4].connect(self.device[4],1883,60)
        self.objs[4].publish("test1", self.msg5)

    # Slider Buttons functions
    def slider_R5(self, R5):
        self.msg5 = 'cosmoguirlande,R,' + str((R5))
        self.objs[4].connect(self.device[4],1883,60)
        self.objs[4].publish("test1", self.msg5)

    def slider_G5(self, G5):
        self.msg5 = 'cosmoguirlande,G,' + str((G5))
        self.objs[4].connect(self.device[4],1883,60)
        self.objs[4].publish("test1", self.msg5)

    def slider_B5(self, B5):
        self.msg5 = 'cosmoguirlande,B,' + str((B5))
        self.objs[4].connect(self.device[4],1883,60)
        self.objs[4].publish("test1", self.msg5)

    def slider_W5(self, W5):
        self.msg5 = 'cosmoguirlande,W,' + str((W5))
        self.objs[4].connect(self.device[4],1883,60)
        self.objs[4].publish("test1", self.msg5)

    #########################################################################################################Strip 6
    def color6_change_demand61(self):
        print("selection changed ", self.type_color66.currentText())
        self.msg6 = 'cosmoguirlande,color1,' + str(( self.type_color61.currentText()))
        self.objs[5].connect(self.device[5],1883,60)
        self.objs[5].publish("test1", self.msg6)

    def color6_change_demand62(self):
        print("selection changed ", self.type_color66.currentText())
        self.msg6 = 'cosmoguirlande,color2,' + str(( self.type_color62.currentText()))
        self.objs[5].connect(self.device[5],1883,60)
        self.objs[5].publish("test1", self.msg6)

    def on_click_ip_6(self):
        self.IPValue_6 = self.textbox_IP_6.text()
        self.vnc_window_6 = VNC_Window(self.IPValue_6)
        self.vnc_window_6.start()

    def on_click_port_6(self):
        PortValue_6 = self.textbox_port_6.text()

    def on_click_strombo_6_frequency(self):
        Strombo_frequency = self.textbox_port.text()
        QMessageBox.question(self, 'Message - pythonspot.com', "You typed: " + Strombo_frequency, QMessageBox.Ok,
                             QMessageBox.Ok)
        self.textbox.setText("")

    def blackout_demand_6(self):
        self.msg6 = 'cosmoguirlande,blackout'
        self.objs[5].connect(self.device[5],1883,60)
        self.objs[5].publish("test1", self.msg6)

    def rainbow_demand_6(self):
        self.msg6 = 'cosmoguirlande,rainbow'
        self.objs[5].connect(self.device[5],1883,60)
        self.objs[5].publish("test1", self.msg6)

    def strombo_demand_6(self):
        self.msg6 = 'cosmoguirlande,strombo'
        self.objs[5].connect(self.device[5],1883,60)
        self.objs[5].publish("test1", self.msg6)

    def theaterChase_demand_6(self):
        self.msg6 = 'cosmoguirlande,theaterChase'
        self.objs[5].connect(self.device[5],1883,60)
        self.objs[5].publish("test1", self.msg6)

    def theaterChaseRainbow_demand_6(self):
        self.msg6 = 'cosmoguirlande,theaterChaseRainbow'
        self.objs[5].connect(self.device[5],1883,60)
        self.objs[5].publish("test1", self.msg6)

    def multiColorWipe_demand_6(self):
        self.msg6 = 'cosmoguirlande,multiColorWipe'
        self.objs[5].connect(self.device[5],1883,60)
        self.objs[5].publish("test1", self.msg6)

    def sync_demand_6(self):
        self.msg6 = 'cosmoguirlande,sync'
        self.objs[5].connect(self.device[5],1883,60)
        self.objs[5].publish("test1", self.msg6)

    def strombo_demand_6(self):
        self.msg6 = 'cosmoguirlande,strombo'
        self.objs[5].connect(self.device[5],1883,60)
        self.objs[5].publish("test1", self.msg6)

    def chase_demand_6(self):
        self.msg6 = 'cosmoguirlande,chase'+',' + self.textbox_chase_speed_6.text() + ',' + self.textbox_chase_size_6.text()
        self.objs[5].connect(self.device[5],1883,60)
        self.objs[5].publish("test1", self.msg6)

    def comet_demand_6(self):
        self.msg6 = 'cosmoguirlande,comet' +',' + self.textbox_comet_speed_6.text() + ',' + self.textbox_comet_tail_6.text()
        self.objs[5].connect(self.device[5],1883,60)
        self.objs[5].publish("test1", self.msg6)

    def sparkle_demand_6(self):
        self.msg6 = 'cosmoguirlande,sparkle' +',' + self.textbox_sparkle_speed_6.text() + ',' + self.textbox_sparkle_num_sparkles_6.text()
        self.objs[5].connect(self.device[5],1883,60)
        self.objs[5].publish("test1", self.msg6)

    def pulse_demand_6(self):
        self.msg6 = 'cosmoguirlande,pulse'+',' + self.textbox_pulse_period_6.text() + ',' + self.textbox_pulse_speed_6.text()
        self.objs[5].connect(self.device[5],1883,60)
        self.objs[5].publish("test1", self.msg6)

    def solid_demand_6(self):
        self.msg6 = 'cosmoguirlande,solid'
        self.objs[5].connect(self.device[5],1883,60)
        self.objs[5].publish("test1", self.msg6)

    def colorcycle_demand_6(self):
        self.msg6 = 'cosmoguirlande,colorcycle'
        self.objs[5].connect(self.device[5],1883,60)
        self.objs[5].publish("test1", self.msg6)

    def dancingPiScroll_demand_6(self):
        self.msg6 = 'cosmoguirlande,dancingPiScroll'
        self.objs[5].connect(self.device[5],1883,60)
        self.objs[5].publish("test1", self.msg6)

    def dancingPiEnergy_demand_6(self):
        self.msg6 = 'cosmoguirlande,dancingPiEnergy'
        self.objs[5].connect(self.device[5],1883,60)
        self.objs[5].publish("test1", self.msg6)

    def dancingPiSpectrum_demand_6(self):
        self.msg6 = 'cosmoguirlande,dancingPiSpectrum'
        self.objs[5].connect(self.device[5],1883,60)
        self.objs[5].publish("test1", self.msg6)

    def stop_dancingPiEnergy_demand_6(self):
        self.msg6 = 'cosmoguirlande,stop_dancingPiEnergy'
        self.objs[5].connect(self.device[5],1883,60)
        self.objs[5].publish("test1", self.msg6)

    def stop_dancingPiSpectrum_demand_6(self):
        self.msg6 = 'cosmoguirlande,stop_dancingPiSpectrum'
        self.objs[5].connect(self.device[5],1883,60)
        self.objs[5].publish("test1", self.msg6)

    def stop_dancingPiScroll_demand_6(self):
        self.msg6 = 'cosmoguirlande,stop_dancingPiScroll'
        self.objs[5].connect(self.device[5],1883,60)
        self.objs[5].publish("test1", self.msg6)

    # Slider Buttons functions
    def slider_R6(self, R6):
        self.msg6 = 'cosmoguirlande,R,' + str((R6))
        self.objs[5].connect(self.device[5],1883,60)
        self.objs[5].publish("test1", self.msg6)

    def slider_G6(self, G6):
        self.msg6 = 'cosmoguirlande,G,' + str((G6))
        self.objs[5].connect(self.device[5],1883,60)
        self.objs[5].publish("test1", self.msg6)

    def slider_B6(self, B6):
        self.msg6 = 'cosmoguirlande,B,' + str((B6))
        self.objs[5].connect(self.device[5],1883,60)
        self.objs[5].publish("test1", self.msg6)

    def slider_W6(self, W6):
        self.msg6 = 'cosmoguirlande,W,' + str((W6))
        self.objs[5].connect(self.device[5],1883,60)
        self.objs[5].publish("test1", self.msg6)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWin()
    win.show()
    sys.exit(app.exec_())