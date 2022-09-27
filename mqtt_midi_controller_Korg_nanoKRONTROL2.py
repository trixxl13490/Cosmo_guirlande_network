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
"cosmoguirlande,strombo"
"cosmoguirlande,blackout"
'cosmoguirlande,chase,chase_speed,chase_size'
'cosmoguirlande,comet,comet_speed,comet_tail'
'cosmoguirlande,sparkle,sparkle_speed,sparkle_num'
'cosmoguirlande,pulse,pulse_period,pulse_speed
'cosmoguirlande,solid'
"cosmoguirlande,Strobe"

"cosmoguirlande,Fire"
"cosmoguirlande,R,value"
"cosmoguirlande,G,value"
"cosmoguirlande,B,value"
"""
'''----------------------------------------
Méthode détection & connexion Guirlande:
----------------------------------------'''
device = []
conf_file = open('IP_configuration.json')
strip_configuration = json.load(conf_file)
i = 0
for elt in strip_configuration["guirlande"]:
	print("i :", i)
	#get IPs from JSON
	print("IP : ", elt["IP"])
	objs = [mqtt.Client() for i in range(len(strip_configuration['guirlande']))]
	
	try:
		objs[i].connect(elt["IP"],1883,60)
		print("publish blackout")
		device.append(elt["IP"])
		objs[i].publish('test1', "cosmoguirlande,blackout")
					
		
	except:
		print("could not connect to :  ", elt["IP"])
		#====================================================================test
		print("elt['IP']", elt["IP"])
		#del strip_configuration["guirlande"][i]
		#objs.remove(objs[i])
		try:
			device.remove(elt["IP"])
		except ValueError:
			pass
	i = i+1

for i, elt in enumerate(device):
	print("À l'indice {} se trouve {}.".format(i, elt))
		#====================================================================fin test
	

'''----------------------------------------
Méthode envoi message :
----------------------------------------'''
def send_message(strip_number, command):
	print("strip_number: ", strip_number)
	print("command: ", command)
	msg = command
	try:
		objs[strip_number-1].connect(device[strip_number],1883,60)
		objs[strip_number-1].publish("test1", msg)
	except:
		print("could not send to :  ", device[strip_number-1])

'''----------------------------------------
Méthode envoi message sync :
----------------------------------------'''
def send_message_sync(command):
	print("command: ", command)
	msg = command
	i = 0
	for elt in strip_configuration["guirlande"]:
		#print("i :", i)
		try:
			objs[i].connect(device[i],1883,60)
			objs[i].publish("test1", msg)
		except IndexError:
			pass
		except:
			print("could not send to :  ", device[i])
		i = i+1

#global varibales
log = logging.getLogger('midiin_poll')
logging.basicConfig(level=logging.DEBUG)
sync = False
color1 = ''
color2 = ''
color3 = ''
color4 = ''
color5 = ''
color6 = ''
color7 = ''
color8 = ''
previous_velocity = 0
previous_timer = 0
latency_flag = True

# Prompts user for MIDI input port, unless a valid port number or name
# is given as the first argument on the command line.
# API backend defaults to ALSA on Linux.
#port = sys.argv[1] if len(sys.argv) > 1 else None
port = 0

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

			groupe_touche, touche, velocity = message

			latency_flag = True

			#-----------------------------------------------------------------------------Anti rebond fin de course fader pour sync mode
			if (groupe_touche == 224 or groupe_touche == 225  or groupe_touche == 226  or groupe_touche == 227 
			 or groupe_touche == 228  or groupe_touche == 229  or groupe_touche == 230  or groupe_touche == 231 ) and abs(velocity - previous_velocity) > 10:
				latency_flag = False
				print("too big step between former and new value")
				pass
			#-----------------------------------------------------------------------------Slim buttons
			elif groupe_touche== 144 and touche == 46 and velocity == 127: #1st Do
				#send mqtt commmande
				sync = not(sync)
						
			elif groupe_touche== 144 and touche == 47: #1st Do
				#send mqtt commmande
				send_message_sync("cosmoguirlande,strombo")
							
			elif groupe_touche== 144 and touche == 86: #1st Do
				#send mqtt commmande
				send_message_sync("cosmoguirlande,blackout")
				'''send_message_sync("cosmoguirlande,R,0")
				send_message_sync("cosmoguirlande,G,0")
				send_message_sync("cosmoguirlande,B,0")'''

						
			elif groupe_touche== 144 and touche == 82: #1st Do
				#send mqtt commmande
				send_message_sync("cosmoguirlande,*BouncingBalls")

			elif groupe_touche== 144 and touche == 84: #1st Do
				#send mqtt commmande
				send_message_sync("cosmoguirlande,chase,0.1,5")
						
			elif groupe_touche== 144 and touche == 85: #1st Do
				#send mqtt commmande
				send_message_sync("cosmoguirlande,comet,0.1,5")

			#-----------------------------------------------------------------------------buttons

			elif groupe_touche== 144 and touche == 91: #1st Do
				#send mqtt commmande
				send_message_sync("cosmoguirlande,sparkle,0.1,5")

			elif groupe_touche== 144 and touche == 92: #1st Do
				#send mqtt commmande
				send_message_sync("cosmoguirlande,pulse,0.2,0.2")
						
			elif groupe_touche== 144 and touche == 93: #1st Do
				#send mqtt commmande
				send_message_sync("cosmoguirlande,Strobe")

			elif groupe_touche== 144 and touche == 94: #1st Do
				#send mqtt commmande
				send_message_sync("cosmoguirlande,Fire")

			elif groupe_touche== 144 and touche == 95 and velocity == 127: #1st Do
				#send mqtt commmande
				send_message_sync("cosmoguirlande,restart")
				#FONCTION RESTART HERE
				subprocess.Popen(args='python Thread_start_display_remote_ssh.py', shell=True)
				subprocess.Popen(args='python start_display_remote_ssh.py', shell=True)
			#-----------------------------------------------------------------------------column1

			elif groupe_touche== 176 and touche == 16: #1st Do
				#send mqtt commmande
				pass

			elif groupe_touche== 224 : #Color1 fader
				#send mqtt commmande
				print("abs(velocity - previous_velocity) : ", abs(velocity - previous_velocity))
				
				if sync :					
					send_message_sync("cosmoguirlande," + color1 + ',' + str(velocity*2) )

					#reduce latency by emptying midi message buffer, to be improved
					if velocity >0 or velocity<127:
						for i in range(15):
							msg = midiin.get_message()

				elif not(sync):
					send_message(1, "cosmoguirlande," + color1 + ',' + str(velocity) )
						
			elif groupe_touche== 144 and touche == 8 and velocity>0: #R1
				#send mqtt commmande
				color1 = 'R'

			elif groupe_touche== 144 and touche == 16 and velocity>0: #G1
				#send mqtt commmande
				color1 = 'G'

			elif groupe_touche== 144 and touche == 0 and velocity>0: #B1
				#send mqtt commmande
				color1 = 'B'

			#-----------------------------------------------------------------------------column2

			elif groupe_touche== 176 and touche == 17: #1st Do
				#send mqtt commmande
				pass

			elif groupe_touche== 225 : #Color2 fader
				#send mqtt commmande
				send_message(2, "cosmoguirlande," + color2 + ',' + str(velocity*2) )
						
			elif groupe_touche== 144 and touche == 9 and velocity>0: #R2
				#send mqtt commmande
				color2 = 'R'

			elif groupe_touche== 144 and touche == 17 and velocity>0: #G2
				#send mqtt commmande
				color2 = 'G'

			elif groupe_touche== 144 and touche == 1 and velocity>0: #B2
				#send mqtt commmande
				color2 = 'B'

			#-----------------------------------------------------------------------------column3

			elif groupe_touche== 176 and touche == 18: #1st Do
				#send mqtt commmande
				pass

			elif groupe_touche== 226 : #Color3 fader
				#send mqtt commmande
				send_message(3, "cosmoguirlande," + color3 + ',' + str(velocity*2) )
						
			elif groupe_touche== 144 and touche == 10 and velocity>0: #R3
				#send mqtt commmande
				color3 = 'R'

			elif groupe_touche== 144 and touche == 18 and velocity>0: #G3
				#send mqtt commmande
				color3 = 'G'

			elif groupe_touche== 144 and touche == 2 and velocity>0: #B3
				#send mqtt commmande
				color3 = 'B'

			#-----------------------------------------------------------------------------column4

			elif groupe_touche== 176 and touche == 19: #1st Do
				#send mqtt commmande
				pass

			elif groupe_touche== 227 : #Color4 fader
				#send mqtt commmande
				send_message(4, "cosmoguirlande," + color4 + ',' + str(velocity*2) )
						
			elif groupe_touche== 144 and touche == 11 and velocity>0: #R4
				#send mqtt commmande
				color4 = 'R'

			elif groupe_touche== 144 and touche == 19 and velocity>0: #G4
				#send mqtt commmande
				color4 = 'G'

			elif groupe_touche== 144 and touche == 3 and velocity>0: #B4
				#send mqtt commmande
				color4 = 'B'

			#-----------------------------------------------------------------------------column5

			elif groupe_touche== 176 and touche == 20: #1st Do
				#send mqtt commmande
				pass

			elif groupe_touche== 228 : #Color5 fader
				#send mqtt commmande
				send_message(5, "cosmoguirlande," + color5 + ',' + str(velocity*2) )
						
			elif groupe_touche== 144 and touche == 12 and velocity>0: #R5
				#send mqtt commmande
				color5 = 'R'

			elif groupe_touche== 144 and touche == 20 and velocity>0: #G5
				#send mqtt commmande
				color5 = 'G'

			elif groupe_touche== 144 and touche == 4 and velocity>0: #B5
				#send mqtt commmande
				color5 = 'B'

			#-----------------------------------------------------------------------------column6

			elif groupe_touche== 176 and touche == 21: #1st Do
				#send mqtt commmande
				pass

			elif groupe_touche== 229 : #Color6 fader
				#send mqtt commmande
				send_message(6, "cosmoguirlande," + color6 + ',' + str(velocity*2) )
						
			elif groupe_touche== 144 and touche == 13 and velocity>0: #R6
				#send mqtt commmande
				color6 = 'R'

			elif groupe_touche== 144 and touche == 21 and velocity>0: #G6
				#send mqtt commmande
				color6 = 'G'

			elif groupe_touche== 144 and touche == 5 and velocity>0: #B6
				#send mqtt commmande
				color6 = 'B'

			#-----------------------------------------------------------------------------column7

			elif groupe_touche== 176 and touche == 22: #1st Do
				#send mqtt commmande
				pass

			elif groupe_touche== 230 : ##Color7 fader
				#send mqtt commmande
				send_message(7, "cosmoguirlande," + color7 + ',' + str(velocity*2) )
						
			elif groupe_touche== 144 and touche == 14 and velocity>0: #R7
				#send mqtt commmande
				color7 = 'R'

			elif groupe_touche== 144 and touche == 22 and velocity>0: #G7
				#send mqtt commmande
				color7 = 'G'

			elif groupe_touche== 144 and touche == 6 and velocity>0: #B7
				#send mqtt commmande
				color7 = 'B'

			#-----------------------------------------------------------------------------column8

			elif groupe_touche== 176 and touche == 23: #1st Do
				#send mqtt commmande
				pass

			elif groupe_touche== 231 : #Color8 fader
				#send mqtt commmande
				send_message(8, "cosmoguirlande," + color8 + ',' + str(velocity*2) )
				send_message(9, "cosmoguirlande," + color8 + ',' + str(velocity*2) )
						
			elif groupe_touche== 144 and touche == 15 and velocity>0: #R8
				#send mqtt commmande
				color8 = 'R'

			elif groupe_touche== 144 and touche == 23 and velocity>0: #G8
				#send mqtt commmande
				color8 = 'G'

			elif groupe_touche== 144 and touche == 7 and velocity>0: #B8
				#send mqtt commmande
				color8 = 'B'

			previous_velocity = velocity
			previous_timer = timer


except KeyboardInterrupt:
    print('')
finally:
    print("Exit.")
    midiin.close_port()
    del midiin