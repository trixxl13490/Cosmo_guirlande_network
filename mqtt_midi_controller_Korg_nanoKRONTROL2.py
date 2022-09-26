#!/usr/bin/env python
#
# midiin_poll.py
#
"""Show how to receive MIDI input by polling an input port."""

from __future__ import print_function

import logging
import sys
import time

from rtmidi.midiutil import open_midiinput

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
            print("type(message) :", type(message))
            for elt in message:
                print("element de message: ", elt)


        '''
		slim_button1 = [176,16,value]
		slim_button2 = [176,16,value]
		slim_button3 = [176,16,value]
		slim_button4 = [176,16,value]
		slim_button5 = [176,16,value]

		button1 = [224,value,value]
		button1 = [176,16,value]
		button1 = [224,value,value]
		button1 = [224,value,value]
		button1 = [176,16,value]

		
		
		potar1 = [176,16,value]
		fader1 = [224,value,value]
		side_button11 = [144,8,value]
		side_button12 = [144,16,value]
		side_button13 = [144,0,value]

		potar2 = [176,17,value]
		fader2 = [225,value,value]
		side_button21 = [144,9,value]
		side_button22 = [144,17,value]
		side_button23 = [144,1,value]

		potar3 = [176,18,value]
		fader3 = [226,value,value]
		side_button31 = [144,value,value]
		side_button32 = [144,value,value]
		side_button33 = [144,value,value]

		potar4 = [176,19,value]
		fader4 =[227,value,value]
		side_button41 = [144,value,value]
		side_button42 = [144,value,value]
		side_button43 = [144,value,value]

		potar5 = [176,20,value]
		fader5 = [228,value,value]
		side_button51 = [144,value,value]
		side_button52 = [144,value,value]
		side_button53 = [144,value,value]

		potar6 = [176,21,value]
		fader6 = [229,value,value]
		side_button61 = [144,value,value]
		side_button62 = [144,value,value]
		side_button63 = [144,value,value]

		potar7 = [176,22,value]
		fader7 = [230,value,value]
		side_button71 = [144,value,value]
		side_button72 = [144,value,value]
		side_button73 = [144,value,value]

		potar8 = [176,23,value]
		fader8 = [231,value,value]
		side_button81 = [144,value,value]
		side_button82 = [144,value,value]
		side_button83 = [144,value,value]

		----------------------------------------
		EX. Mapping touches
		Piano Yamaha 
		----------------------------------------
		touches 1 = do = 36 
		touche  -1 = do = 96
		potar1 = 

		----------------------------------------
		Méthode détection & connexion Guirlande:
		----------------------------------------
		conf_file = open('IP_configuration.json')
		strip_configuration = json.load(conf_file)
		i = 0
		for elt in strip_configuration["guirlande"]:
			objs = [mqtt.Client() for i in range(len(strip_configuration['guirlande']))]
			device.append(elt["IP"])
			i = i+1


		----------------------------------------
		Méthode envoi message :
		----------------------------------------
		msg1 = 'cosmoguirlande,chase,' + speed.text() + ',' + chase_size.text()
		i = 0
		for elt in strip_configuration["guirlande"]:
			try:
				objs[i].connect(device[i],1883,60)
				objs[i].publish("test1", self.msg1)
			except:
				print("could not send to :  ", device[i])
			i = i+1


		----------------------------------------
		Exemple Mapping Touche
		----------------------------------------
		Groupe_touche, touche, Velocity = message
		if touche = "do" and velocity >=10:
			#send mqtt commmande

		----------------------------------------

		'''

except KeyboardInterrupt:
    print('')
finally:
    print("Exit.")
    midiin.close_port()
    del midiin