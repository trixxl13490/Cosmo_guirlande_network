#!/usr/bin/env python
#
# midiin_poll.py
#
"""Show how to receive MIDI input by polling an input port."""

from __future__ import print_function

import logging
import sys
import time
import json
import paho.mqtt.client as mqtt
from rtmidi.midiutil import open_midiinput
import subprocess

"""identification des touches
    Mapping des touches / boutons / faders aux messages à envoye0r
    Commandes:

'cosmoguirlande,color1'
	'AMBER'
	'AQUA'
	'YELLOW'
	'WHITE'
	'TEAL'
	'RGBW_WHITE_W'
	'RGBW_WHITE_RGBW'
	'RGBW_WHITE_RGB'
	'RED'
	'PURPLE'
	'PINK'
	'ORANGE'
	'OLD_LACE'
	'MAGENTA'
	'JADE'
	'GREEN'
	'GOLD'
	'CYAN'
	'BLUE'
	'BLACK'
'cosmoguirlande,color2'
	'AMBER'
	'AQUA'
	'YELLOW'
	'WHITE'
	'TEAL'
	'RGBW_WHITE_W'
	'RGBW_WHITE_RGBW'
	'RGBW_WHITE_RGB'
	'RED'
	'PURPLE'
	'PINK'
	'ORANGE'
	'OLD_LACE'
	'MAGENTA'
	'JADE'
	'GREEN'
	'GOLD'
	'CYAN'
	'BLUE'
	'BLACK'
"cosmoguirlande,strombo"
"cosmoguirlande,rainbow"
"cosmoguirlande,blackout"
'cosmoguirlande,chase,chase_speed,chase_size'
'cosmoguirlande,comet,comet_speed,comet_tail'
'cosmoguirlande,sparkle,sparkle_speed,sparkle_num'
'cosmoguirlande,pulse,pulse_period,pulse_speed
'cosmoguirlande,solid'
'cosmoguirlande,colorcycle'
'cosmoguirlande,dancingPiScroll'
'cosmoguirlande,dancingPiEnergy'
'cosmoguirlande,dancingPiSpectrum'
'cosmoguirlande,stop_dancingPiScroll'
'cosmoguirlande,stop_dancingPiEnergy'
'cosmoguirlande,stop_dancingPiSpectrum'
"cosmoguirlande,R,value"
"cosmoguirlande,G,value"
"cosmoguirlande,B,value"
"cosmoguirlande,W,value"
"cosmoguirlande,colorAll2Color"
"cosmoguirlande,FadeInOut"
"cosmoguirlande,Strobe"
"cosmoguirlande,HalloweenEyes"
"cosmoguirlande,CylonBounce"
"cosmoguirlande,NewKITT"
"cosmoguirlande,Twinkle"
"cosmoguirlande,TwinkleRandom"
"cosmoguirlande,SnowSparkle"
"cosmoguirlande,*RunningLights"
"cosmoguirlande,colorWipe"
"cosmoguirlande,theaterChaseRainbow"
"cosmoguirlande,Fire"
"cosmoguirlande,FireCustom"
"cosmoguirlande,meteorRain"
"cosmoguirlande,fadeToBlack"
"cosmoguirlande,*BouncingBalls"
"cosmoguirlande,*BouncingColoredBalls"
"cosmoguirlande,Matrix"
"cosmoguirlande,*Drain"
"cosmoguirlande,Pancake"
"cosmoguirlande,HeartBeat"
"cosmoguirlande,rainbowWithGlitter"
"cosmoguirlande,Confetti"
"cosmoguirlande,Sinelon"
"cosmoguirlande,**BPM"
"""



'''----------------------------------------
Méthode détection & connexion Guirlande:
----------------------------------------'''
device = []
conf_file = open('IP_configuration.json')
strip_configuration = json.load(conf_file)
i = 0
for elt in strip_configuration["guirlande"]:
	objs = [mqtt.Client() for i in range(len(strip_configuration['guirlande']))]
	device.append(elt["IP"])
	print(device[i])
	i = i+1


'''----------------------------------------
Méthode envoi message :
----------------------------------------'''
def send_message_sync(command):
	msg = command
	i = 0
	for elt in strip_configuration["guirlande"]:
		try:
			objs[i].connect(device[i],1883,60)
			objs[i].publish("test1", msg)
		except:
			print("could not send to :  ", device[i])
		i = i+1


log = logging.getLogger('midiin_poll')
logging.basicConfig(level=logging.DEBUG)

# Prompts user for MIDI input port, unless a valid port number or name
# is given as the first argument on the command line.
# API backend defaults to ALSA on Linux.
port = sys.argv[1] if len(sys.argv) > 1 else None

try:
    midiin, port_name = open_midiinput(port)
except (EOFError, KeyboardInterrupt):
    sys.exit()

print("Entering main loop. Press Control-C to exit.")
try:
	timer = time.time()
	while True:
		msg = midiin.get_message()
		if msg:
			message, deltatime = msg
			timer += deltatime
			print("[%s] @%0.6f %r" % (port_name, timer, message))
			'''print("type(message) :", type(message))
			for elt in message:
				print("element de message: ", elt)
				print("type de message: ", type(elt))'''

			#R0
			groupe_touche, touche, velocity = message
			if touche == 36: #1st Do
				#send mqtt commmande
				send_message_sync("cosmoguirlande,R,0")

			if touche == 37: #1st Do
				#send mqtt commmande
				send_message_sync("cosmoguirlande,R,25")

			if touche == 38: #1st Do
				#send mqtt commmande
				send_message_sync("cosmoguirlande,R,50")

			if touche == 39: #1st Do
				#send mqtt commmande
				send_message_sync("cosmoguirlande,R,75")

			if touche == 40: #1st Do
				#send mqtt commmande
				send_message_sync("cosmoguirlande,R,100")

			if touche == 41: #1st Do
				#send mqtt commmande
				send_message_sync("cosmoguirlande,R,125")

			if touche == 42: #1st Do
				#send mqtt commmande
				send_message_sync("cosmoguirlande,R,150")

			if touche == 43: #1st Do
				#send mqtt commmande
				send_message_sync("cosmoguirlande,R,175")

			if touche == 45: #1st Do
				#send mqtt commmande
				send_message_sync("cosmoguirlande,R,200")

			if touche == 46: #1st Do
				#send mqtt commmande
				send_message_sync("cosmoguirlande,R,225")

			if touche == 47: #1st Do
				#send mqtt commmande
				send_message_sync("cosmoguirlande,G,0")

			if touche == 48: #1st Do
				#send mqtt commmande
				send_message_sync("cosmoguirlande,G,30")

			if touche == 49: #1st Do
				#send mqtt commmande
				send_message_sync("cosmoguirlande,G,60")

			if touche == 50: #1st Do
				#send mqtt commmande
				send_message_sync("cosmoguirlande,G,90")

			if touche == 51: #1st Do
				#send mqtt commmande
				send_message_sync("cosmoguirlande,G,120")

			if touche == 52: #1st Do
				#send mqtt commmande
				send_message_sync("cosmoguirlande,G,150")

			if touche == 53: #1st Do
				#send mqtt commmande
				send_message_sync("cosmoguirlande,G,180")

			if touche == 54: #1st Do
				#send mqtt commmande
				send_message_sync("cosmoguirlande,G,210")

			if touche == 55: #1st Do
				#send mqtt commmande
				send_message_sync("cosmoguirlande,G,240")

			if touche == 56: #1st Do
				#send mqtt commmande
				send_message_sync("cosmoguirlande,G,255")

			if touche == 57: #1st Do
				#send mqtt commmande
				send_message_sync("cosmoguirlande,B,0")

			if touche == 58: #1st Do
				#send mqtt commmande
				send_message_sync("cosmoguirlande,B,16")

			if touche == 59: #1st Do
				#send mqtt commmande
				send_message_sync("cosmoguirlande,B,32")

			if touche == 60: #1st Do
				#send mqtt commmande
				send_message_sync("cosmoguirlande,B,48")

			if touche == 61: #1st Do
				#send mqtt commmande
				send_message_sync("cosmoguirlande,B,54")

			if touche == 62: #1st Do
				#send mqtt commmande
				send_message_sync("cosmoguirlande,B,60")

			if touche == 63: #1st Do
				#send mqtt commmande
				send_message_sync("cosmoguirlande,B,76")

			if touche == 64: #1st Do
				#send mqtt commmande
				send_message_sync("cosmoguirlande,B,92")

			if touche == 65: #1st Do
				#send mqtt commmande
				send_message_sync("cosmoguirlande,B,108")

			if touche == 66: #1st Do
				#send mqtt commmande
				send_message_sync("cosmoguirlande,B,124")

			if touche == 67: #1st Do
				#send mqtt commmande
				send_message_sync("cosmoguirlande,Confetti")

			if touche == 68: #1st Do
				#send mqtt commmande
				send_message_sync("cosmoguirlande,HeartBeat")

			if touche == 69: #1st Do
				#send mqtt commmande
				send_message_sync("cosmoguirlande,fadeToBlack")

			if touche == 70: #1st Do
				#send mqtt commmande
				send_message_sync("cosmoguirlande,Fire")

			if touche == 71: #1st Do
				#send mqtt commmande
				send_message_sync("cosmoguirlande,Strobe")

			if touche == 72: #1st Do
				#send mqtt commmande
				send_message_sync("cosmoguirlande,FadeInOut")

			if touche == 73: #1st Do
				#send mqtt commmande
				send_message_sync("cosmoguirlande,solid")

			if touche == 74: #1st Do
				#send mqtt commmande
				send_message_sync("cosmoguirlande,pulse,pulse_period,pulse_speed")

			if touche == 75: #1st Do
				#send mqtt commmande
				send_message_sync("cosmoguirlande,pulse,pulse_period,pulse_speed")

			if touche == 76: #1st Do
				#send mqtt commmande
				send_message_sync("cosmoguirlande,pulse,pulse_period,pulse_speed")

			if touche == 77: #1st Do
				#send mqtt commmande
				send_message_sync("cosmoguirlande,pulse,pulse_period,pulse_speed")

			if touche == 78: #1st Do
				#send mqtt commmande
				send_message_sync("cosmoguirlande,sparkle,sparkle_speed,sparkle_num")

			if touche == 79: #1st Do
				#send mqtt commmande
				send_message_sync("cosmoguirlande,sparkle,sparkle_speed,sparkle_num")

			if touche == 80: #1st Do
				#send mqtt commmande
				send_message_sync("cosmoguirlande,sparkle,sparkle_speed,sparkle_num")

			if touche == 81: #1st Do
				#send mqtt commmande
				send_message_sync("cosmoguirlande,comet,comet_speed,comet_tail")

			if touche == 82: #1st Do
				#send mqtt commmande
				send_message_sync("cosmoguirlande,comet,comet_speed,comet_tail")

			if touche == 83: #1st Do
				#send mqtt commmande
				send_message_sync("cosmoguirlande,comet,comet_speed,comet_tail")

			if touche == 84: #1st Do
				#send mqtt commmande
				send_message_sync("cosmoguirlande,chase,chase_speed,chase_size")

			if touche == 85: #1st Do
				#send mqtt commmande
				send_message_sync("cosmoguirlande,chase,chase_speed,chase_size")

			if touche == 86: #1st Do
				#send mqtt commmande
				send_message_sync("cosmoguirlande,chase,chase_speed,chase_size")

			if touche == 87: #1st Do
				#send mqtt commmande
				send_message_sync("")

			if touche == 88: #1st Do
				#send mqtt commmande
				send_message_sync("")

			if touche == 89: #1st Do
				#send mqtt commmande
				send_message_sync("")

			if touche == 90: #1st Do
				#send mqtt commmande
				send_message_sync("")

			if touche == 91: #1st Do
				#send mqtt commmande
				send_message_sync("")

			if touche == 92: #1st Do
				#send mqtt commmande
				send_message_sync("")

			if touche == 93: #1st Do
				#send mqtt commmande
				send_message_sync("cosmoguirlande,rainbow")

			if touche == 94: #1st Do
				#send mqtt commmande
				send_message_sync("cosmoguirlande,strombo")

			if touche == 95: #1st Do
				#send mqtt commmande
				send_message_sync("cosmoguirlande,blackout")

			if touche == 96: #1st Do
				#send mqtt commmande
				subprocess.Popen(args='python start_display_remote_ssh.py', shell=True)

		time.sleep(0.01)
except KeyboardInterrupt:
    print('')
finally:
    print("Exit.")
    midiin.close_port()
    del midiin