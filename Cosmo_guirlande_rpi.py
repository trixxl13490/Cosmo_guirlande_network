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

class Cosmo_Communication(threading.Thread):

    def __init__(self, guirlande_number, pixel_number, tcp_ip, tcp_port, buffer_size):
        threading.Thread.__init__(self)
        self.guirlande_number = guirlande_number
        self.pixel_number = pixel_number
        self.tcp_ip = str(tcp_ip)
        self.tcp_port = tcp_port
        self.buffer_size = buffer_size
        self.data_rcv = ""
        self.state = ""


        print("Cosmo Guirlande Number: " + str(self.guirlande_number))
        print("TCP ip server: " + str(self.tcp_ip))
        print("TCP port : " + str(self.tcp_port))
        print("TCP buffer size: " + str(self.buffer_size))

    def run(self):
        try:
            while True:
                ##construction socket
                connexion_serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

                ##connexion socket avec connect et tuple parametre
                connexion_serveur.connect((self.tcp_ip, self.tcp_port))

                ##message confirmation
                print("Connexion etablie avec le serveur sur le port {}".format(self.tcp_port))


                # Send message
                line = str("cosmoguirlande_" + str(self.guirlande_number) + "," + str(
                    self.pixel_number) + "," + self.tcp_ip + "," + str(self.tcp_port))
                print(line)
                line = line.encode()
                connexion_serveur.send(line)

                #Receive message
                self.data_rcv = connexion_serveur.recv(self.buffer_size)
                self.data_rcv = self.data_rcv.decode()
                print("data_rcv : ", self.data_rcv)

                ##fermeture connexion
                connexion_serveur.close()
                time.sleep(0.5)

                if self.data_rcv.find('stop_dancingPi') != -1:
                    print("close dancyPi from cosmo_communication class")
                    os.system("ps aux | grep dancyPi | awk '{print $2}' | xargs sudo kill -9")
                elif self.data_rcv.startswith('cosmoguirlande,restart'):
                    self.state = 'restart'


        except ConnectionResetError:
            print("connection reset")
            time.sleep(1)
            self.run()

        except TimeoutError:
            print("Timeout Error, start again thread")
            time.sleep(1)
            self.run()

        except OSError:
            print("OS Error, start again thread")
            time.sleep(1)
            self.run()

        except KeyboardInterrupt:
            print("keyboard interrupt, blackout LED")
            connexion_serveur.close()

class Cosmo_guirlande_rpi(threading.Thread):
    def __init__(self, pixels, guirlande_number, pixel_number, tcp_ip, tcp_port, buffer_size):
        threading.Thread.__init__(self)
        self.pixels = pixels
        self.pixel_number = pixel_number
        self.controle_manuel = False
        self.r = '0'
        self.g = '0'
        self.b = '0'
        self.w = '0'
        self.fixed_color = False
        self.chase_speed = 0.1
        self.chase_size = 10
        self.comet_speed = 0.01
        self.comet_tail = 3
        self.pulse_speed = 0.1
        self.pulse_period = 1
        self.sparkle_speed = 0.1
        self.sparkle_num = 10
        self.color_cycle_speed = 0.4
        self.pixels = pixels
        self.guirlande_number = guirlande_number
        self.pixel_number = pixel_number
        self.tcp_ip = tcp_ip
        self.tcp_port = tcp_port
        self.buffer_size = buffer_size

        #Create Socket to communicate
        self.newSocket = Cosmo_Communication(guirlande_number, pixel_number, tcp_ip, tcp_port, buffer_size)
        self.newSocket.start()

        #Watchdog
        self.watchdog_count = 0
        self.state = ""
        self.previous_state = ""

    def wheel(self, pos):
        # Input a value 0 to 255 to get a color value.
        # The colours are a transition r - g - b - back to r.
        if pos < 0 or pos > 255:
            r = g = b = 0
        elif pos < 85:
            r = int(pos * 3)
            g = int(255 - pos * 3)
            b = 0
        elif pos < 170:
            pos -= 85
            r = int(255 - pos * 3)
            g = 0
            b = int(pos * 3)
        else:
            pos -= 170
            r = 0
            g = int(pos * 3)
            b = int(255 - pos * 3)
        return (r, g, b) if neopixel.RGBW in (neopixel.RGB, neopixel.GRB) else (r, g, b, 0)


    def stromboscope(self, color, wait_s):
        print("self.color1",color)
        print("type self.color1", type(color))
        blink = Blink(self.pixels, speed=wait_s, color=color)
        animations = AnimationSequence(
            blink,
            advance_interval=5,
            auto_clear=True,
        )
        while self.newSocket.data_rcv.startswith('cosmoguirlande,strombo'):
            animations.animate()

    def blackout(self):
        solid = Solid(self.pixels, color=BLACK)
        animations = AnimationSequence(
            solid,
            advance_interval=5,
            auto_clear=True,
        )
        while self.newSocket.data_rcv.startswith('cosmoguirlande,blackout'):
            animations.animate()

    def changeColor(self, r, g, b, w):
        self.color1 = (int(r), int(g), int(b), int(w))
        self.pixels.fill((int(r), int(g), int(b), int(w)))
        self.pixels.show()
        time.sleep(0.3)

    def changeColor1String(self, color):
        self.r = '0'
        self.g = '0'
        self.b = '0'
        self.w = '0'
        self.pixels.fill((int(self.r), int(self.g), int(self.b), int(self.w)))
        self.color1 = color
        solid = Solid(self.pixels, color=self.color1)
        animations = AnimationSequence(
            solid,
            advance_interval=5,
            auto_clear=True,
        )
        while self.newSocket.data_rcv.startswith('cosmoguirlande,color1'):
            animations.animate()

    def changeColor2String(self, color):
        self.color2 = color
        solid = Solid(self.pixels, color=self.color2)
        animations = AnimationSequence(
            solid,
            advance_interval=5,
            auto_clear=True,
        )
        while self.newSocket.data_rcv.startswith('cosmoguirlande,color2'):
            animations.animate()

    def rainbow_cycle(self, wait):
        for j in range(255):
            for i in range(self.pixel_number):
                pixel_index = (i * 256 // self.pixel_number) + j
                self.pixels[i] = self.wheel(pixel_index & 255)
            self.pixels.show()
            time.sleep(wait)

    def comet(self):
        comet = Comet(self.pixels, speed=0.01, color=self.color1, tail_length=10, bounce=True)
        animations = AnimationSequence(
            comet,
            advance_interval=5,
            auto_clear=True,
        )
        while self.newSocket.data_rcv.startswith('cosmoguirlande,comet'):
            animations.animate()

    def chase(self):
        chase = Chase(self.pixels, speed=self.chase_speed, size=self.chase_size, spacing=6, color=self.color1)
        animations = AnimationSequence(
            chase,
            advance_interval=5,
            auto_clear=True,
        )
        while self.newSocket.data_rcv.startswith('cosmoguirlande,chase'):
            animations.animate()

    def pulse(self):
        pulse = Pulse(self.pixels, speed=self.pulse_speed, period=self.pulse_period, color=self.color1)
        animations = AnimationSequence(
            pulse,
            advance_interval=5,
            auto_clear=True,
        )
        while self.newSocket.data_rcv.startswith('cosmoguirlande,pulse'):
            animations.animate()

    def sparkle(self):
        sparkle = Sparkle(self.pixels, speed=self.sparkle_speed, color=self.color1, num_sparkles=self.sparkle_num)
        animations = AnimationSequence(
            sparkle,
            advance_interval=5,
            auto_clear=True,
        )
        while self.newSocket.data_rcv.startswith('cosmoguirlande,sparkle'):
            animations.animate()


    def solid(self):
        solid = Solid(self.pixels, color=self.color1)
        animations = AnimationSequence(
            solid,
            advance_interval=5,
            auto_clear=True,
        )
        animations.animate()

    def colorcycle(self):
        colorcycle = ColorCycle(self.pixels, speed=self.color_cycle_speed, colors=[self.color1, self.color2])
        animations = AnimationSequence(
            colorcycle,
            advance_interval=5,
            auto_clear=True,
        )
        while self.newSocket.data_rcv.startswith('cosmoguirlande,colorcycle'):
            animations.animate()

    def dancingPiScroll(self):
        os.system("sudo python3 /home/pi/dancyPi-audio-reactive-led/python/visualization.py scroll")

    def stop_dancingPiScroll(self):
        os.system("sudo ps aux | grep dancyPi | awk '{print $2}' | xargs sudo kill -9")

    def dancingPiEnergy(self):
        os.system("sudo python3 /home/pi/dancyPi-audio-reactive-led/python/visualization.py energy")

    def stop_dancingPiEnergy(self):
        os.system("sudo ps aux | grep dancyPi | awk '{print $2}' | xargs sudo kill -9")

    def dancingPiSpectrum(self):
        os.system("sudo python3 /home/pi/dancyPi-audio-reactive-led/python/visualization.py spectrum")

    def stop_dancingPiSpectrum(self):
        os.system("sudo ps aux | grep dancyPi | awk '{print $2}' | xargs sudo kill -9")
        # os.system("ps aux | grep dancyPi | awk '{print $2}' | xargs sudo kill -9")

    def run(self):
        try:
            while True:

                # Create Socket to communicate
                #self.newSocket = Cosmo_Communication(self.guirlande_number, self.pixel_number, self.tcp_ip, self.tcp_port, self.buffer_size)
                #self.newSocket.start()

                print("Cosmoguirlande class run")
                print("state :", self.state)
                print("previous state :", self.state)
                self.previous_state = self.state

                # wait for animation type and threshold
                if self.newSocket.data_rcv.startswith("cosmoguirlande,manual"):
                    print("manual control, do nothing while checkbox is on")
                    time.sleep(0.3)

                elif self.newSocket.data_rcv.startswith("cosmoguirlande,strombo"):
                    self.state = "strombo"
                    self.stromboscope(self.color1, 0.05)
                    time.sleep(0.3)

                elif self.newSocket.data_rcv.startswith('cosmoguirlande,color1'):
                    self.state = 'color1'
                    function_type, function, self.color1 = self.newSocket.data_rcv.split(',')
                    print("color1 :", self.color1)
                    self.w = 0
                    if self.color1 =='AMBER':
                        self.changeColor1String(AMBER)
                    elif self.color1 =='AQUA':
                        self.changeColor1String(AQUA)
                    elif self.color1 == 'YELLOW':
                        self.changeColor1String(YELLOW)
                    elif self.color1 == 'WHITE':
                        self.changeColor1String(WHITE)
                    elif self.color1 == 'TEAL':
                        self.changeColor1String(TEAL)
                    elif self.color1 == 'RGBW_WHITE_W':
                        self.changeColor1String(RGBW_WHITE_W)
                    elif self.color1 == 'RGBW_WHITE_RGBW':
                        self.changeColor1String(RGBW_WHITE_RGBW)
                    elif self.color1 == 'RGBW_WHITE_RGB':
                        self.changeColor1String(RGBW_WHITE_RGB)
                    elif self.color1 == 'RED':
                        self.changeColor1String(RED)
                    elif self.color1 == 'PURPLE':
                        self.changeColor1String(PURPLE)
                    elif self.color1 == 'PINK':
                        self.changeColor1String(PINK)
                    elif self.color1 == 'ORANGE':
                        self.changeColor1String(ORANGE)
                    elif self.color1 =='OLD_LACE':
                        self.changeColor1String(OLD_LACE)
                    elif self.color1 == 'MAGENTA':
                        self.changeColor1String(MAGENTA)
                    elif self.color1 == 'JADE':
                        self.changeColor1String(JADE)
                    elif self.color1 == 'GREEN':
                        self.changeColor1String(GREEN)
                    elif self.color1 =='GOLD':
                        self.changeColor1String(GOLD)
                    elif self.color1 == 'CYAN':
                        self.changeColor1String(CYAN)
                    elif self.color1 == 'BLUE':
                        self.changeColor1String(BLUE)
                    elif self.color1 == 'BLACK':
                        self.changeColor1String(BLACK)

                elif self.newSocket.data_rcv.startswith('cosmoguirlande,color2'):
                    self.state = 'color2'
                    function_type, function, self.color2 = self.newSocket.data_rcv.split(',')
                    if self.color2 =='AMBER':
                        self.changeColor2String(AMBER)
                    elif self.color2 =='AQUA':
                        self.changeColor2String(AQUA)
                    elif self.color2 == 'YELLOW':
                        self.changeColor2String(YELLOW)
                    elif self.color2 == 'WHITE':
                        self.changeColor2String(WHITE)
                    elif self.color2 == 'TEAL':
                        self.changeColor2String(TEAL)
                    elif self.color2 == 'RGBW_WHITE_W':
                        self.changeColor2String(RGBW_WHITE_W)
                    elif self.color2 == 'RGBW_WHITE_RGBW':
                        self.changeColor2String(RGBW_WHITE_RGBW)
                    elif self.color2 == 'RGBW_WHITE_RGB':
                        self.changeColor2String(RGBW_WHITE_RGB)
                    elif self.color2 == 'RED':
                        self.changeColor2String(RED)
                    elif self.color2 == 'PURPLE':
                        self.changeColor2String(PURPLE)
                    elif self.color2 == 'PINK':
                        self.changeColor2String(PINK)
                    elif self.color2 == 'ORANGE':
                        self.changeColor2String(ORANGE)
                    elif self.color2 =='OLD_LACE':
                        self.changeColor2String(OLD_LACE)
                    elif self.color2 == 'MAGENTA':
                        self.changeColor2String(MAGENTA)
                    elif self.color2 == 'JADE':
                        self.changeColor2String(JADE)
                    elif self.color2 == 'GREEN':
                        self.changeColor2String(GREEN)
                    elif self.color2 =='GOLD':
                        self.changeColor2String(GOLD)
                    elif self.color2 == 'CYAN':
                        self.changeColor2String(CYAN)
                    elif self.color2 == 'BLUE':
                        self.changeColor2String(BLUE)
                    elif self.color2 == 'BLACK':
                        self.changeColor2String(BLACK)

                elif self.newSocket.data_rcv.startswith("cosmoguirlande,rainbow"):
                    self.state = "rainbow"
                    for j in range(2):
                        self.rainbow_cycle(0.01)

                elif self.newSocket.data_rcv.startswith("cosmoguirlande,blackout"):
                    self.state = "blackout"
                    self.blackout()

                elif self.newSocket.data_rcv.startswith('cosmoguirlande,chase'):
                    self.state = "chase"
                    function_type, function, chase_speed, chase_size = self.newSocket.data_rcv.split(',')
                    try:
                        self.chase_speed = float(chase_speed)
                    except ValueError:
                        self.chase_speed = 0
                    try:
                        self.chase_size = int(chase_size)
                    except ValueError:
                        self.chase_size = 0
                    self.chase()

                elif self.newSocket.data_rcv.startswith('cosmoguirlande,comet'):
                    self.state = "comet"
                    function_type, function, comet_speed, comet_tail = self.newSocket.data_rcv.split(',')
                    try:
                        self.comet_speed = float(comet_speed)
                    except ValueError:
                        self.comet_speed = 0
                    try:
                        self.comet_tail = int(comet_tail)
                    except ValueError:
                        self.comet_tail = 0
                    self.comet()

                elif self.newSocket.data_rcv.startswith('cosmoguirlande,sparkle'):
                    self.state = "sparkle"
                    function_type, function, sparkle_speed, sparkle_num = self.newSocket.data_rcv.split(',')
                    try:
                        self.sparkle_speed = float(sparkle_speed)
                    except ValueError:
                        self.sparkle_speed = 0
                    try:
                        self.sparkle_num = int(sparkle_num)
                    except ValueError:
                        self.sparkle_num = 0
                    self.sparkle()

                elif self.newSocket.data_rcv.startswith('cosmoguirlande,pulse'):
                    self.state = "pulse"
                    function_type, function, pulse_period, pulse_speed = self.newSocket.data_rcv.split(',')
                    try:
                        self.pulse_period = float(pulse_period)
                    except ValueError:
                        self.pulse_period = 0
                    try:
                        self.pulse_speed = float(pulse_speed)
                    except ValueError:
                        self.pulse_speed = 0
                    self.pulse()

                elif self.newSocket.data_rcv.startswith('cosmoguirlande,solid'):
                    self.state = "solid"
                    self.solid()
                    time.sleep(0.5)

                elif self.newSocket.data_rcv.startswith('cosmoguirlande,colorcycle'):
                    self.state = "colorcycle"
                    function_type, function, self.color2 = self.newSocket.data_rcv.split(',')
                    self.colorcycle()

                elif self.newSocket.data_rcv.startswith('cosmoguirlande,dancingPiScroll'):
                    self.state = "dancingPiScroll"
                    self.blackout()
                    self.dancingPiScroll()

                elif self.newSocket.data_rcv.startswith('cosmoguirlande,dancingPiEnergy'):
                    self.state = "dancingPiEnergy"
                    self.blackout()
                    self.dancingPiEnergy()

                elif self.newSocket.data_rcv.startswith('cosmoguirlande,dancingPiSpectrum'):
                    self.state = "dancingPiSpectrum"
                    self.blackout()
                    self.dancingPiSpectrum()

                elif self.newSocket.data_rcv.startswith('cosmoguirlande,stop_dancingPiScroll'):
                    self.state = "stop_dancingPiScroll"
                    self.stop_dancingPiScroll()

                elif self.newSocket.data_rcv.startswith('cosmoguirlande,stop_dancingPiEnergy'):
                    self.state = "stop_dancingPiEnergy"
                    self.stop_dancingPiEnergy()

                elif self.newSocket.data_rcv.startswith('cosmoguirlande,stop_dancingPiSpectrum'):
                    self.state = "stop_dancingPiSpectrum"
                    self.stop_dancingPiSpectrum()

                elif self.newSocket.data_rcv.startswith("cosmoguirlande,R"):
                    self.state = "R"
                    function_type, function, self.r = self.newSocket.data_rcv.split(',')
                    self.changeColor(self.r, self.g, self.b, self.w)
                    time.sleep(0.5)

                elif self.newSocket.data_rcv.startswith("cosmoguirlande,G"):
                    self.state = "G"
                    function_type, function, self.g = self.newSocket.data_rcv.split(',')
                    self.changeColor(self.r, self.g, self.b, self.w)
                    time.sleep(0.5)

                elif self.newSocket.data_rcv.startswith("cosmoguirlande,B"):
                    self.state = "B"
                    function_type, function, self.b = self.newSocket.data_rcv.split(',')
                    self.changeColor(self.r, self.g, self.b, self.w)
                    time.sleep(0.5)

                elif self.newSocket.data_rcv.startswith("cosmoguirlande,W"):
                    self.state = "W"
                    function_type, function, self.w = self.newSocket.data_rcv.split(',')
                    self.changeColor(self.r, self.g, self.b, self.w)
                    time.sleep(0.5)

                elif self.state == "nothing":
                    #increse count if last states are "main"
                    if self.previous_state == "nothing":
                        self.watchdog_count = self.watchdog_count +1
                        print("watchdog_count :",self.watchdog_count)
                        time.sleep(0.5)
                    #if no messages since last 10 sec (10 "main state), start again
                    elif self.watchdog_count == 20:
                        self.watchdog_count = 0
                        self.run()
                    self.previous_state = self.state

                elif self.state == "restart":
                    self.state = "restart"
                    # Del former, create a new one and start it
                    self.newSocket.connexion_serveur.close()
                    self.newSocket = Cosmo_Communication(self.guirlande_number, self.pixel_number, self.tcp_ip, self.tcp_port, self.buffer_size)
                    self.newSocket.start()

                else:
                    print("nothing")
                    self.state = "nothing"
                    time.sleep(1)

                self.previous_message = self.newSocket.data_rcv


        except TypeError:
            print("type error")
            self.run()

        except KeyboardInterrupt:
            print("keyboard interrupt, blackout LED")
            self.state = "keyboard"
            if args.clear:
                pixels.fill((0, 0, 0, 0))

#Check if main class is style alive - to be run on a thread


if __name__ == '__main__':
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    parser.add_argument('guirlande_number', metavar='guirlande_number', type=int, help='Cosmo Guirlande NUmber')
    parser.add_argument('num_pixel', metavar='num_pixel', type=int, help='Number of pixel')
    parser.add_argument('server_tcp_ip', metavar='server_tcp_ip', type=str, help='Server IP')
    parser.add_argument('tcp_port', metavar='tcp_port', type=int, help='Tcp Port')
    parser.add_argument('buffer_size', metavar='buffer_size', type=int, help='Buffer Size')
    args = parser.parse_args()

    # Configuration des LED
    pixels = neopixel.NeoPixel(
        board.D18, args.num_pixel, brightness=0.9, auto_write=False, pixel_order=neopixel.GRBW
    )
    print('Press Ctrl-C to quit.')

    # Run ex: sudo python3 Desktop/Cosmo_guirlande_rpi.py 1 30 192.168.0.17 50001 1024

    cosmo_guirlande = Cosmo_guirlande_rpi(args.guirlande_number, args.num_pixel, args.server_tcp_ip, args.tcp_port, args.buffer_size)
    while(True):
        try:
            cosmo_guirlande.run()
        except :
            cosmo_guirlande.run()


