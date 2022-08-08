# Simple test for NeoPixels on Raspberry Pi
import argparse
import time
import board
import neopixel
import os
import threading
import math
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
import random
from RPi_mqtt_socket import RPi_mqtt_socket

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


        '''print("Cosmo Guirlande Number: " + str(self.guirlande_number))
        print("TCP ip server: " + str(self.tcp_ip))
        print("TCP port : " + str(self.tcp_port))
        print("TCP buffer size: " + str(self.buffer_size))'''

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
                #print(line)
                line = line.encode()
                connexion_serveur.send(line)

                #Receive message - wait for it
                #while self.previous_message != self.newSocket.data_rcv:
                self.data_rcv = connexion_serveur.recv(self.buffer_size)
                self.data_rcv = self.data_rcv.decode()
                print("data_rcv : ", self.data_rcv)
                time.sleep(0.1)

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
            connexion_serveur.close()
            print("connection close")
            time.sleep(1)
            self.run()

        except TimeoutError:
            print("Timeout Error, start again thread")
            time.sleep(1)
            connexion_serveur.close()
            print("connection close")
            self.run()

        except OSError:
            print("OS Error, start again thread")
            time.sleep(1)
            connexion_serveur.close()
            print("connection close")
            self.run()

        except KeyboardInterrupt:
            print("keyboard interrupt, blackout LED")
            connexion_serveur.close()


class Cosmo_guirlande_rpi(threading.Thread):
    def __init__(self, pixels, guirlande_number, pixel_number, tcp_ip, tcp_port, buffer_size, rgb):
        threading.Thread.__init__(self)
        self.pixels = pixels
        self.pixel_number = pixel_number
        self.controle_manuel = False
        self.rgb = rgb
        self.r = '0'
        self.g = '0'
        self.b = '0'
        self.w = '0'
        self.color1 = "AMBER"
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
        self.guirlande_number = guirlande_number
        self.pixel_number = pixel_number
        self.tcp_ip = tcp_ip
        self.tcp_port = tcp_port
        self.buffer_size = buffer_size
        self.levelobj = (43, 73, 103, 135, 160, 188, 213, 236, 255, 272, 286, 295, 300)
        self.levelobjcount = len(self.levelobj)
        self.levelgroups = (5, 9, 14, 17, 19, 23, 25, 28, 30, 32, 35, 39, 43)
        self.PartyColors_p = (
    ((0x55),(0x50),(0xAB)), ((0x84),(0x00),(0x7C)), ((0xB5),(0x00),(0x4B)), ((0xE5),(0x00),(0x1B)),
    ((0xE8),(0x17),(0x00)), ((0xB8),(0x47),(0x00)), ((0xAB),(0x77),(0x00)), ((0xAB),(0xAB),(0x00)),
    ((0xAB),(0x55),(0x00)), ((0xDD),(0x22),(0x00)), ((0xF2),(0x00),(0x0E)), ((0xC2),(0x00),(0x3E)),
    ((0x8F),(0x00),(0x71)), ((0x5F),(0x00),(0xA1)), ((0x2F),(0x00),(0xD0)), ((0x00),(0x07),(0xF9))  )

        #Create Socket to communicate
        self.newSocket = Cosmo_Communication(guirlande_number, pixel_number, tcp_ip, tcp_port, buffer_size)
        self.newSocket_mqtt = RPi_mqtt_socket()
        
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
        if self.rgb.startswith("RGBW"):
            self.color1 = (int(r), int(g), int(b), int(w))
            self.pixels.fill((int(r), int(g), int(b), int(w)))
            self.pixels.show()
            time.sleep(0.3)

        elif self.rgb.startswith("RGB"):
            self.color1 = (int(r), int(g), int(b))
            self.pixels.fill((int(r), int(g), int(b)))
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
        animations.animate()
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
        animations.animate()

    def dancingPiScroll(self):
        os.system("sudo python3 dancyPi-audio-reactive-led/python/visualization.py scroll")

    def stop_dancingPiScroll(self):
        os.system("sudo ps aux | grep dancyPi | awk '{print $2}' | xargs sudo kill -9")

    def dancingPiEnergy(self):
        os.system("sudo python3 dancyPi-audio-reactive-led/python/visualization.py energy")

    def stop_dancingPiEnergy(self):
        os.system("sudo ps aux | grep dancyPi | awk '{print $2}' | xargs sudo kill -9")

    def dancingPiSpectrum(self):
        os.system("sudo python3 dancyPi-audio-reactive-led/python/visualization.py spectrum")

    def stop_dancingPiSpectrum(self):
        os.system("sudo ps aux | grep dancyPi | awk '{print $2}' | xargs sudo kill -9")

    # colorAll2Color((red1, green1, blue1), (red2, green2, blue2)) 
    def colorAll2Color(self, c1, c2):
        for i in range(self.pixel_number):
            if(i % 2 == 0): # even
                self.pixels[i] = c1
            else: # odd   
                self.pixels[i] = c2
        self.pixels.show()
    '''
    def wheel(pos):
        # Input a value 0 to 255 to get a color value.
        # The colours are a transition r - g - b - back to r.
        if pos < 0 or pos > 255:
            r = g = b = 0
        elif pos < 85:
            r = int(pos * 3)
            g = int(255 - pos*3)
            b = 0
        elif pos < 170:
            pos -= 85
            r = int(255 - pos*3)
            g = 0
            b = int(pos*3)
        else:
            pos -= 170
            r = 0
            g = int(pos*3)
            b = int(255 - pos*3)
        return (r, g, b) if neopixel.ORDER == neopixel.RGB or neopixel.ORDER == neopixel.GRB else (r, g, b, 0)
    
    def rainbow_cycle(self,delay, cycles):
        for j in range(255 * cycles):
            for i in range(self.pixel_number):
                # " // "  this divides and returns the integer value of the quotient. 
                # It dumps the digits after the decimal
                pixel_index = (i * 256 // self.pixel_numbers) + j
                self.pixels[i] = self.wheel(pixel_index & 255)
            self.pixels.show()
            time.sleep(delay)
    '''
    # RGBLoop(delay)
    def RGBLoop(self, delay):
        for j in range(3):
            # Fade IN
            for k in range(256):
                if j == 0:
                    self.pixels.fill((k, 0, 0))
                elif j == 1:
                    self.pixels.fill((0, k, 0))
                elif j == 2:
                    self.pixels.fill((0, 0, k))
                self.pixels.show()
                time.sleep(delay)

            # Fade OUT
            for k in range(256):
                if j == 2:
                    self.pixels.fill((k, 0, 0))
                elif j == 1:
                    self.pixels.fill((0, k, 0))
                elif j == 0:
                    self.pixels.fill((0, 0, k))
                self.pixels.show()
                time.sleep(delay)

    def wheelBrightLevel(self, pos, bright):
        # Input a value 0 to 255 to get a color value.
        # The colours are a transition r - g - b - back to r.
        if pos < 0 or pos > 255:
            r = g = b = 0
        elif pos < 85:
            r = int(pos * 3)
            g = int(255 - pos*3)
            b = 0
        elif pos < 170:
            pos -= 85
            r = int(255 - pos*3)
            g = 0
            b = int(pos*3)
        else:
            pos -= 170
            r = 0
            g = int(pos*3)
            b = int(255 - pos*3)

        # bight level logic
        color = self.brightnessRGB(r, g, b, bright)
        r = color[0]
        g = color[1]
        b = color[2]

        return color

    def brightnessRGB(self, red, green, blue, bright):
        r = (bright/256.0)*red
        g = (bright/256.0)*green
        b = (bright/256.0)*blue
        return (int(r), int(g), int(b))

    def clear_level(self, level):
        #levels = (58, 108, 149, 187, 224, 264, 292, 309, 321, 327, 336, 348) #this only works if you have 350 lights
        #levels = (11, 20, 27, 34, 39, 43, 47, 50) #this works for 50 lights
        #levels = (20, 34, 43, 50) #this works for 50 lights
        levels = self.levelobj
        startPxl = 0
        if (level == 0):
            startPxl = 0
        else:
            startPxl = levels[level-1]
        for i in range(startPxl, levels[level]):
            self.pixels[i] = (0,0,0)  #CRGB::Black;

    # FadeInOut(red, green, blue, delay)  
    def FadeInOut(self,red, green, blue, delay):
        r = 0
        g = 0
        b = 0
        red = int(red) 
        green = int(green)
        blue = int(blue)
        for k in range(256):
            r = (k/256.0)*red
            g = (k/256.0)*green
            b = (k/256.0)*blue
            self.pixels.fill((int(r), int(g), int(b)))
            self.pixels.show()
            time.sleep(delay)
        
        for k in range(256, -1, -1):
            r = (k/256.0)*red
            g = (k/256.0)*green
            b = (k/256.0)*blue
            self.pixels.fill((int(r), int(g), int(b)))
            self.pixels.show()
            time.sleep(delay)

    # Strobe(red, green, blue, StrobeCount, FlashDelay, EndPause)
    def Strobe(self, red, green, blue, StrobeCount, FlashDelay, EndPause):
        red = int(red) 
        green = int(green)
        blue = int(blue)
        for j in range(StrobeCount):
            self.pixels.fill((red,green,blue))
            self.pixels.show()
            time.sleep(FlashDelay)
            self.pixels.fill((0,0,0))
            self.pixels.show()
            time.sleep(FlashDelay)
    
        time.sleep(EndPause)

    # HalloweenEyes(red, green, blue, EyeWidth, EyeSpace, Fade, Steps, FadeDelay, EndPause)
    def HalloweenEyes(self, red, green, blue, EyeWidth, EyeSpace, Fade, Steps, FadeDelay, EndPause):
        red = int(red) 
        green = int(green)
        blue = int(blue)
        self.pixels.fill((0,0,0))
        r = 0
        g = 0
        b = 0

        # define eye1 and eye2 location
        StartPoint  = random.randint( 0, self.pixel_number - (2*EyeWidth) - EyeSpace )
        Start2ndEye = StartPoint + EyeWidth + EyeSpace

        #  set color of eyes for given location
        for i in range(EyeWidth):
            self.pixels[StartPoint + i] = (red, green, blue)
            self.pixels[Start2ndEye + i] = (red, green, blue)
        self.pixels.show()

        # if user wants fading, then fadeout pixel color
        if Fade == True:
            for j in range(Steps, -1, -1):
                r = (j/Steps)*red
                g = (j/Steps)*green
                b = (j/Steps)*blue

                for i in range(EyeWidth):
                    self.pixels[StartPoint + i] = ((int(r), int(g), int(b)))
                    self.pixels[Start2ndEye + i] = ((int(r), int(g), int(b)))

                self.pixels.show()
                time.sleep(FadeDelay)
        
        # Set all pixels to black
        self.pixels.fill((0,0,0))

        # pause before changing eye location
        time.sleep(EndPause)

    # CylonBounce(red, green, blue, EyeSize, SpeedDelay, ReturnDelay)
    def CylonBounce(self, red, green, blue, EyeSize, SpeedDelay, ReturnDelay):
        red = int(red) 
        green = int(green)
        blue = int(blue)
        for i in range(self.pixel_number - EyeSize - 1):
            self.pixels.fill((0,0,0))
            self.pixels[i] = (int(red/10), int(green/10), int(blue/10))

            for j in range(1, EyeSize+1):
                self.pixels[i+j] = (red, green, blue)

            self.pixels[i+EyeSize+1] = (int(red/10), int(green/10), int(blue/10))
            self.pixels.show()
            time.sleep(SpeedDelay)
    
        time.sleep(ReturnDelay)
        time.sleep(10)
        
        for i in range(self.pixel_number - EyeSize - 2, -1, -1):
            self.pixels.fill((0,0,0))
            self.pixels[i] = (int(red/10), int(green/10), int(blue/10))

            for j in range(1, EyeSize+1):
                self.pixels[i+j] = (red, green, blue)

            self.pixels[i+EyeSize+1] = (int(red/10), int(green/10), int(blue/10))
            self.pixels.show()
            time.sleep(SpeedDelay)

        time.sleep(ReturnDelay)
        time.sleep(10)

    # NewKITT(red, green, blue, EyeSize, SpeedDelay, ReturnDelay)
    def NewKITT(self, red, green, blue, EyeSize, SpeedDelay, ReturnDelay):
        self.RightToLeft(red, green, blue, EyeSize, SpeedDelay, ReturnDelay)
        self.LeftToRight(red, green, blue, EyeSize, SpeedDelay, ReturnDelay)
        self.OutsideToCenter(red, green, blue, EyeSize, SpeedDelay, ReturnDelay)
        self.CenterToOutside(red, green, blue, EyeSize, SpeedDelay, ReturnDelay)
        self.LeftToRight(red, green, blue, EyeSize, SpeedDelay, ReturnDelay)
        self.RightToLeft(red, green, blue, EyeSize, SpeedDelay, ReturnDelay)
        self.OutsideToCenter(red, green, blue, EyeSize, SpeedDelay, ReturnDelay)
        self.CenterToOutside(red, green, blue, EyeSize, SpeedDelay, ReturnDelay)

    def CenterToOutside(self,red, green, blue, EyeSize, SpeedDelay, ReturnDelay):
        red = int(red) 
        green = int(green)
        blue = int(blue)
        for i in range(int((self.pixel_number - EyeSize)/2), -1, -1):
            self.pixels.fill((0,0,0))
            self.pixels[i] = (int(red/10), int(green/10), int(blue/10))

            for j in range(1, EyeSize+1):
                self.pixels[i + j] = (red, green, blue)
            
            self.pixels[i + EyeSize + 1] = (int(red/10), int(green/10), int(blue/10))
            self.pixels[self.pixel_number - i - j] = (int(red/10), int(green/10), int(blue/10))

            for j in range(1, EyeSize+1):
                self.pixels[self.pixel_number - i - j] = (red, green, blue)

            self.pixels[self.pixel_number - i - EyeSize - 1] = (int(red/10), int(green/10), int(blue/10))
            self.pixels.show()
            time.sleep(SpeedDelay)

        time.sleep(ReturnDelay)

    def OutsideToCenter(self, red, green, blue, EyeSize, SpeedDelay, ReturnDelay):
        red = int(red) 
        green = int(green)
        blue = int(blue)
        for i in range(int(((self.pixel_number - EyeSize)/2)+1)):
            self.pixels.fill((0,0,0))
            self.pixels[i] = (int(red/10), int(green/10), int(blue/10))

            for j in range(1, EyeSize+1):
                self.pixels[i + j] = (red, green, blue) 
            
            self.pixels[i + EyeSize +1] = (int(red/10), int(green/10), int(blue/10))
            self.pixels[self.pixel_number - i-1] = (int(red/10), int(green/10), int(blue/10))

            for j in range(1, EyeSize+1):
                self.pixels[self.pixel_number - i - j] = (red, green, blue)
            
            self.pixels[self.pixel_number - i - EyeSize - 1] = (int(red/10), int(green/10), int(blue/10))
            self.pixels.show()
            time.sleep(SpeedDelay)
    
        time.sleep(ReturnDelay)

    def LeftToRight(self, red, green, blue, EyeSize, SpeedDelay, ReturnDelay):
        red = int(red) 
        green = int(green)
        blue = int(blue)
        for i in range(self.pixel_number - EyeSize - 2):
            self.pixels.fill((0,0,0))
            self.pixels[i] = (int(red/10), int(green/10), int(blue/10))

            for j in range(1, EyeSize+1):
                self.pixels[i + j] = (red, green, blue)

            self.pixels[i + EyeSize + 1] = (int(red/10), int(green/10), int(blue/10))
            self.pixels.show()
            time.sleep(SpeedDelay)
        
        time.sleep(ReturnDelay)

    def RightToLeft(self, red, green, blue, EyeSize, SpeedDelay, ReturnDelay):
        red = int(red) 
        green = int(green)
        blue = int(blue)
        for i in range(self.pixel_number - EyeSize - 2, 0, -1):
            self.pixels.fill((0,0,0))
            self.pixels[i] = (int(red/10), int(green/10), int(blue/10))

            for j in range(1, EyeSize+1):
                self.pixels[i + j] = (red, green, blue)

            self.pixels[i + EyeSize + 1] = (int(red/10), int(green/10), int(blue/10))
            self.pixels.show()
            time.sleep(SpeedDelay)
    
        time.sleep(ReturnDelay)

    # Twinkle(red, green, blue, Count, SpeedDelay, OnlyOne)
    def Twinkle(self, red, green, blue, Count, SpeedDelay, OnlyOne):
        self.pixels.fill((0,0,0))
        red = int(red) 
        green = int(green)
        blue = int(blue)
        for i in range(Count):
            self.pixels[random.randint(0, self.pixel_number-1)] = (red, green, blue)
            self.pixels.show()
            time.sleep(SpeedDelay)
            if OnlyOne:
                self.pixels.fill((0,0,0))

        time.sleep(SpeedDelay)

    # TwinkleRandom( Count, SpeedDelay, OnlyOne) 
    def TwinkleRandom(self, Count, SpeedDelay, OnlyOne):
        self.pixels.fill((0,0,0))

        for i in range(Count):
            self.pixels[random.randint(0, self.pixel_number-1)] = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
            self.pixels.show()
            time.sleep(SpeedDelay)
            if OnlyOne:
                self.pixels.fill((0,0,0))

        time.sleep(SpeedDelay)

    def Sparkle(self, red, green, blue, Count, SpeedDelay):
        red = int(red) 
        green = int(green)
        blue = int(blue)
        for i in range(Count):    
            Pixel = random.randint(0,self.pixel_number-1)
            self.pixels[Pixel] = (red,green,blue)
            self.pixels.show()
            time.sleep(SpeedDelay)
            self.pixels[Pixel] = (0,0,0)
    
    # SnowSparkle(red, green, blue, Count, SparkleDelay, SpeedDelay)
    def SnowSparkle(self, red, green, blue, Count, SparkleDelay, SpeedDelay):
        red = int(red) 
        green = int(green)
        blue = int(blue)
        self.pixels.fill((red,green,blue))

        for i in range(Count):
            Pixel = random.randint(0,self.pixel_number-1)
            self.pixels[Pixel] = (255,255,255)
            self.pixels.show()
            time.sleep(SparkleDelay)
            self.pixels[Pixel] = (red,green,blue)
            self.pixels.show()
            time.sleep(SpeedDelay)

    # RunningLights(red, green, blue, WaveDelay)
    def RunningLights(self, red, green, blue, WaveDelay):
        red = int(red) 
        green = int(green)
        blue = int(blue)
        Position = 0
        
        for j in range(self.pixel_number*2):
            Position = Position + 1
            
            for i in range(self.pixel_number):
                # sine wave, 3 offset waves make a rainbow!
                # float level = sin(i+Position) * 127 + 128;
                # setPixel(i,level,0,0);
                # float level = sin(i+Position) * 127 + 128;
                level = math.sin(i + Position) * 127 + 128
                r = int((level/255)*red)
                g = int((level/255)*green)
                b = int((level/255)*blue)
                self.pixels[i] = (r,g,b)

            self.pixels.show()
            time.sleep(WaveDelay)

    # colorWipe(red, green, blue, SpeedDelay)
    def colorWipe(self, red, green, blue, SpeedDelay):
        red = int(red) 
        green = int(green)
        blue = int(blue)
        for i in range(self.pixel_number):
            self.pixels[i] = (red, green, blue)
            self.pixels.show()
            time.sleep(SpeedDelay)

    # theaterChase(red, green, blue, cycles, SpeedDelay)
    def theaterChase(self, red, green, blue, cycles, SpeedDelay):
        red = int(red) 
        green = int(green)
        blue = int(blue)
        for j in range(cycles):
            for q in range(3):
                for i in range(0, self.pixel_number, 3):
                    if i+q < self.pixel_number:
                        # turn every third pixel on
                        self.pixels[i+q] = (red, green, blue)
                
                self.pixels.show()
                time.sleep(SpeedDelay)
                
                for i in range(0, self.pixel_number, 3):
                    if i+q < self.pixel_number:
                        # turn every third pixel off
                        self.pixels[i+q] = (0,0,0)

    # theaterChaseRainbow(SpeedDelay)
    def theaterChaseRainbow(self, SpeedDelay, cycles):
        # cycle all 256 colors in the wheel
        for j in range(cycles):

            for q in range(3):
                for i in range(0, self.pixel_number, 3):
                    # check that pixel index is not greater than number of pixels
                    if i+q < self.pixel_number:
                        # turn every third pixel on
                        pixel_index = (i * 256 // self.pixel_number) + j
                        self.pixels[i+q] = self.wheel(pixel_index & 255)

                
                self.pixels.show()
                time.sleep(SpeedDelay)
                
                for i in range(0, self.pixel_number, 3):
                    # check that pixel index is not greater than number of pixels
                    if i+q < self.pixel_number:
                        # turn every third pixel off
                        self.pixels[i+q] = (0,0,0)

    ### Fix Me - something is broken with the logic. the color doesn't change. and the fire effect seems small
    ### orginal code; https://www.tweaking4all.com/hardware/arduino/adruino-led-strip-effects/#LEDStripEffectFire

    # Fire(CoolingRangeStart, CoolingRangeEnd, Sparking, SparkingRangeStart, SparkingRangeEnd, SpeedDelay, FireColor, FireEffect, LoopCount)
        #CoolingRangeStart = 0-255
        #CoolingRangeEnd = 0-255
        #Sparking = 0-100  (0= 0% sparkes randomly added, 100= 100% sparks randomly added)
        #SparkingRangeStart = 0-255 
        #SparkingRangeEnd = 0-255
        #FireColor = 0-2 (0=red, 1=blue , 2=green)
        #FireEffect = 0-2

	# Fire(Cooling, Sparking, SpeedDelay, LoopCount)
    def Fire(self, Cooling, Sparking, SpeedDelay, LoopCount):
        heat = []
        for i in range(self.pixel_number):
            heat.append(0)
        for l in range(LoopCount):
            cooldown = 0
            
            # Step 1.  Cool down every cell a little
            for i in range(self.pixel_number):
                randomCooldown = ((Cooling * 10) / self.pixel_number) + 2
                cooldown = random.randint(0, int(randomCooldown))

                if cooldown > heat[i]:
                    heat[i]=0
                else: 
                    heat[i]=heat[i]-cooldown
            
            
            # Step 2.  Heat from each cell drifts 'up' and diffuses a little
            for k in range(self.pixel_number - 1, 2, -1):
                heat[k] = (heat[k - 1] + heat[k - 2] + heat[k - 2]) / 3
                
            # Step 3.  Randomly ignite new 'sparks' near the bottom
            if random.randint(0,255) < Sparking:
                y = random.randint(0,7)
                #heat[y] = heat[y] + random.randint(160,255)
                heat[y] = random.randint(160,255)

            # Step 4.  Convert heat to LED colors
            for j in range(self.pixel_number):
                self.setPixelHeatColor(j, int(heat[j]) )

            self.pixels.show()
            time.sleep(SpeedDelay)

    def setPixelHeatColor (self, Pixel, temperature):
        # Scale 'heat' down from 0-255 to 0-191
        t192 = round((temperature/255.0)*191)

        # calculate ramp up from
        heatramp = t192 & 63 # 0..63  0x3f=63
        heatramp <<= 2 # scale up to 0..252
        # figure out which third of the spectrum we're in:
        if t192 > 0x80: # hottest 128 = 0x80
            self.pixels[Pixel] = (255, 255, int(heatramp))
        elif t192 > 0x40: # middle 64 = 0x40
            self.pixels[Pixel] = (255, int(heatramp), 0)
        else: # coolest
            self.pixels[Pixel] = (int(heatramp), 0, 0)

    # FireCustom(CoolingRangeStart, CoolingRangeEnd, Sparking, SparkingRangeStart, SparkingRangeEnd, 
    #             SpeedDelay, cycles):
        #   CoolingRangeStart: (0-255) cooling random value, start range
        #   CoolingRangeEnd: (0-255) cooling random value, end range
        #   Sparking: (0-100)  chance of sparkes are added randomly controld througn a % value, 100= 100% and 0 = 0%
        #   SparkingRangeStart: (0- number of pixels) spark position random value, start range
        #   SparkingRangeEnd: (0- number of pixels) spark position random value, end range
        #   SpeedDelay: (0-...) slow down the effect by injecting a delay in Sec. 0=no delay, .05=50msec, 2=2sec
    def FireCustom(self, CoolingRangeStart, CoolingRangeEnd, Sparking, SparkingRangeStart, SparkingRangeEnd, SpeedDelay, FireColor, FireEffect, LoopCount):
        heat = []
        for i in range(self.pixel_number):
            heat.append(0)
        for l in range(LoopCount):
            cooldown = 0
            
            # Step 1.  Cool down every cell a little
            for i in range(self.pixel_number):
                # for 50 leds and cooling 50
                # cooldown = random.randint(0, 12)
                # cooldown = random.randint(0, ((Cooling * 10) / self.pixel_number) + 2)
                cooldown = random.randint(CoolingRangeStart, CoolingRangeEnd)
                if cooldown > heat[i]:
                    heat[i]=0
                else: 
                    heat[i]=heat[i]-cooldown
            
            # Step 2.  Heat from each cell drifts 'up' and diffuses a little
            for k in range(self.pixel_number - 1, 2, -1):
                heat[k] = (heat[k - 1] + heat[k - 2] + heat[k - 2]) / 3
                
            # Step 3.  Randomly ignite new 'sparks' near the bottom
            if random.randint(0,100) < Sparking:
                
                # randomly pick the position of the spark
                y = random.randint(SparkingRangeStart,SparkingRangeEnd)
                # different fire effects 
                if FireEffect == 0:
                    heat[y] = random.randint(int(heat[y]),255)
                elif FireEffect == 1:
                    heat[y] = heat[y] + random.randint(160,255)
                else:
                    heat[y] = random.randint(160,255)

            # Step 4.  Convert heat to LED colors
            for j in range(self.pixel_number):
                t192 = round((int(heat[j])/255.0)*191)

                # calculate ramp up from
                heatramp = t192 & 63 # 0..63  0x3f=63
                heatramp <<= 2 # scale up to 0..252
                # figure out which third of the spectrum we're in:
                if FireColor == 2: #green flame
                    if t192 > 0x80: # hottest 128 = 0x80
                        self.pixels[j] = (int(heatramp),255, 255)
                    elif t192 > 0x40: # middle 64 = 0x40
                        self.pixels[j] = (0, 255, int(heatramp))
                    else: # coolest
                        self.pixels[j] = (0, int(heatramp), 0)
                elif FireColor == 1: #blue flame
                    if t192 > 0x80: # hottest 128 = 0x80
                        self.pixels[j] = (255, int(heatramp), 255)
                    elif t192 > 0x40: # middle 64 = 0x40
                        self.pixels[j] = (int(heatramp), 0, 255)
                    else: # coolest
                        self.pixels[j] = (0, 0, int(heatramp))
                else: #FireColor == 0: #red flame
                    if t192 > 0x80: # hottest 128 = 0x80
                        self.pixels[j] = (255, 255, int(heatramp))
                    elif t192 > 0x40: # middle 64 = 0x40
                        self.pixels[j] = (255, int(heatramp), 0)
                    else: # coolest
                        self.pixels[j] = (int(heatramp), 0, 0)
                    

            self.pixels.show()
            time.sleep(SpeedDelay)

    # meteorRain(red, green, blue, meteorSize, meteorTrailDecay, meteorRandomDecay, LoopCount, SpeedDelay)
    def meteorRain(self, red, green, blue, meteorSize, meteorTrailDecay, meteorRandomDecay, LoopCount, SpeedDelay): 
        red = int(red) 
        green = int(green)
        blue = int(blue)
        for loop in range(LoopCount):
            self.pixels.fill((0,0,0))
            
            for i in range(self.pixel_number*2):
                # fade brightness all LEDs one step
                for j in range(self.pixel_number):
                    if (not meteorRandomDecay) or (random.randint(0,10) > 5):
                        self.fadeToBlack(j, meteorTrailDecay )      
                
                # draw meteor
                for j in range(meteorSize):
                    if ( i-j < self.pixel_number) and (i-j >= 0): 
                        self.pixels[i-j] = (red, green, blue)

                self.pixels.show()
                time.sleep(SpeedDelay)

    def fadeToBlack(self, ledNo, fadeValue):
        oldColor = self.pixels[ledNo]
        r = oldColor[0]
        g = oldColor[1]
        b = oldColor[2]

        if (r<=10):
            r = 0
        else:
            r = r - ( r * fadeValue / 256 )

        if (g<=10):
            g = 0
        else:
            g = g - ( g * fadeValue / 256 )

        if (b<=10):
            b = 0
        else:
            b = b - ( b * fadeValue / 256 )

        self.pixels[ledNo] = ( int(r), int(g), int(b) )

    # BouncingBalls(red, green, blue, BallCount, LoopCount) 
    def BouncingBalls(self, red, green, blue, BallCount, LoopCount):
        red = int(red) 
        green = int(green)
        blue = int(blue)
        ## setup 
        Gravity = -9.81
        StartHeight = 1

        Height = []
        for i in range(BallCount):
            Height.append(0)

        ImpactVelocityStart = math.sqrt( -2 * Gravity * StartHeight )

        ImpactVelocity = []
        for i in range(BallCount):
            ImpactVelocity.append(0)

        TimeSinceLastBounce = []
        for i in range(BallCount):
            TimeSinceLastBounce.append(0)

        Position = []
        for i in range(BallCount):
            Position.append(0)

        ClockTimeSinceLastBounce = []
        for i in range(BallCount):
            ClockTimeSinceLastBounce.append(0)
        
        Dampening = []
        for i in range(BallCount):
            Dampening.append(0)

        for i in range(BallCount):
            ClockTimeSinceLastBounce[i] = int(round(time.time() * 1000))

            Height[i] = StartHeight
            Position[i] = 0
            ImpactVelocity[i] = ImpactVelocityStart
            TimeSinceLastBounce[i] = 0
            Dampening[i] = 0.90 - float(i)/pow(BallCount,2)
        
        ## loop 
        for loop in range(LoopCount):
            for i in range(BallCount):
                TimeSinceLastBounce[i] =  int(round(time.time() * 1000)) - ClockTimeSinceLastBounce[i]
                Height[i] = 0.5 * Gravity * pow( TimeSinceLastBounce[i]/1000 , 2.0 ) + ImpactVelocity[i] * TimeSinceLastBounce[i]/1000
        
                if Height[i] < 0:                 
                    Height[i] = 0
                    ImpactVelocity[i] = Dampening[i] * ImpactVelocity[i]
                    ClockTimeSinceLastBounce[i] = int(round(time.time() * 1000))
            
                    if ImpactVelocity[i] < 0.01:
                        ImpactVelocity[i] = ImpactVelocityStart

                Position[i] = round( Height[i] * (self.pixel_number - 1) / StartHeight)
            
            for i in range(BallCount):
                self.pixels[Position[i]] = (red,green,blue)
            
            self.pixels.show()
            self.pixels.fill((0, 0, 0))
            
    # BouncingColoredBalls(BallCount, colors[][3], LoopCount) 
    def BouncingColoredBalls(self, BallCount, colors, LoopCount):
        
        ## setup 
        Gravity = -9.81
        StartHeight = 1

        Height = []
        for i in range(BallCount):
            Height.append(0)

        ImpactVelocityStart = math.sqrt( -2 * Gravity * StartHeight )

        ImpactVelocity = []
        for i in range(BallCount):
            ImpactVelocity.append(0)

        TimeSinceLastBounce = []
        for i in range(BallCount):
            TimeSinceLastBounce.append(0)

        Position = []
        for i in range(BallCount):
            Position.append(0)

        ClockTimeSinceLastBounce = []
        for i in range(BallCount):
            ClockTimeSinceLastBounce.append(0)
        
        Dampening = []
        for i in range(BallCount):
            Dampening.append(0)

        for i in range(BallCount):
            ClockTimeSinceLastBounce[i] = int(round(time.time() * 1000))

            Height[i] = StartHeight
            Position[i] = 0
            ImpactVelocity[i] = ImpactVelocityStart
            TimeSinceLastBounce[i] = 0
            Dampening[i] = 0.90 - float(i)/pow(BallCount,2)
        
        ## loop 
        for loop in range(LoopCount):
            for i in range(BallCount):
                TimeSinceLastBounce[i] =  int(round(time.time() * 1000)) - ClockTimeSinceLastBounce[i]
                Height[i] = 0.5 * Gravity * pow( TimeSinceLastBounce[i]/1000 , 2.0 ) + ImpactVelocity[i] * TimeSinceLastBounce[i]/1000
        
                if Height[i] < 0:                 
                    Height[i] = 0
                    ImpactVelocity[i] = Dampening[i] * ImpactVelocity[i]
                    ClockTimeSinceLastBounce[i] = int(round(time.time() * 1000))
            
                    if ImpactVelocity[i] < 0.01:
                        ImpactVelocity[i] = ImpactVelocityStart

                Position[i] = round( Height[i] * (self.pixel_number - 1) / StartHeight)
            
            for i in range(BallCount):
                self.pixels[Position[i]] = (colors[i][0],colors[i][1],colors[i][2])
            
            self.pixels.show()
            self.pixels.fill((0, 0, 0))
        
    def brightnessRGB(self,red, green, blue, bright):
        r = (bright/256.0)*red
        g = (bright/256.0)*green
        b = (bright/256.0)*blue
        return (int(r), int(g), int(b))

    def fadeall(self,scale):
        for i in range(self.pixel_number): #for(int i = 0; i < NUM_LEDS; i++) 
            #leds[i].nscale8(250)
            
            #get current color pf pixel
            c = self.pixels[i]
            red = c[0]
            green = c[1]
            blue = c[2]
            
            # scale color
            #scale = 250
            r = (scale/256.0)*red
            g = (scale/256.0)*green
            b = (scale/256.0)*blue

            #change pixel
            self.pixels[i] = (int(r),int(g),int(b))

    def matrix(self, random_percent, delay, cycles):
        for loop in range(cycles):
            rand = random.randint(0, 100)

            # set first pixel
            if rand <= random_percent:
                self.pixels[0] = self.wheelBrightLevel(random.randint(0, 255), 255)
            else:
                self.pixels[0] = (0,0,0)
            
            # show pixels 
            self.pixels.show()
            time.sleep(delay)

            # rotate pixel positon
            for i in range(self.pixel_number - 1, 0, -1):
                self.pixels[i] = self.pixels[i-1]

    def random_levels(self, NUM_LEVELS, delay, cycles ):
        for loop in range(cycles):

            level = random.randint(0, NUM_LEVELS)
            if (NUM_LEVELS == level):
                level = 0
            self.light_level_random(level, 1)
            self.pixels.show()
            time.sleep(delay)

    def light_level_random(self, level,  clearall ):
        #levels = (58, 108, 149, 187, 224, 264, 292, 309, 321, 327, 336, 348) #this only works if you have 350 lights
        #levels = (11, 20, 27, 34, 39, 43, 47, 50) #this works for 50 lights
        #levels = (20, 34, 43, 50) #this works for 50 lights
        levels = self.levelobj
        if (clearall):
            self.pixels.fill((0, 0, 0)) # clear all
            self.pixels.show()
        
        startPxl = 0
        if (level == 0):
            startPxl = 0
        else:
            startPxl = levels[level-1]
        
        for i in range(startPxl, levels[level]):
            self.pixels[i] = self.wheelBrightLevel(random.randint(0, 255), random.randint(50, 255))

    def drain(self,level, delay):
        interrupt = False
        for pancakeLevel in range(level):

            # only needed if you ouput to a small display 
            # updateControlVars() 
            
            if (interrupt):
                return
            
            for level in range(pancakeLevel, -1, -1):
                # only needed if you ouput to a small display 
                # updateControlVars()  
                
                if (interrupt) :
                    return

                self.clear_level(level)
                if (level >= 1) :
                    self.light_level_random(level-1, 0)

                # show pixel values 
                self.pixels.show()
                time.sleep(delay)

    def pancake(self, groupsObj, delay):
        NUM_LEVELS = len(groupsObj)
        for pancakeLevel in range(NUM_LEVELS):
            
            for level in range(NUM_LEVELS-1, pancakeLevel-1, -1):
                # only needed if you ouput to a small display 
                # updateControlVars()   

                if (level < NUM_LEVELS-1):
                    self.clear_level(level+1)
                    
                self.light_level_random(level, 0)

                # show pixel values 
                self.pixels.show()
                time.sleep(delay)

    def HeartBeat(self, redo, greeno, blueo, cycles):
        for loop in range(cycles):
            #redo =random.randint(0, 255)
            #greeno = random.randint(0, 255)
            #blueo = random.randint(0, 255)
            
            #strip.setPixelColor(2, redo, greeno, blueo)
            self.pixels.fill((redo, greeno, blueo))
            self.pixels.show()
            time.sleep(.020)
            
            x = 3
            for ii in range(1,252,x): #for ( ii = 1 ; ii <252 ; ii = ii = ii + x)
                self.pixels.fill( self.brightnessRGB(redo, greeno, blueo, ii) ) #strip.setBrightness(ii)
                self.pixels.show()
                time.sleep(.005)

            for ii in range(252,3,-x): #for (int ii = 252 ; ii > 3 ; ii = ii - x){
                self.pixels.fill( self.brightnessRGB(redo, greeno, blueo, ii) ) #strip.setBrightness(ii)
                self.pixels.show()
                time.sleep(.003)

            time.sleep(.0010)
            
            y = 6
            for ii in range(1,252,y): #for (int ii = 1 ; ii <255 ; ii = ii = ii + y){
                self.pixels.fill( self.brightnessRGB(redo, greeno, blueo, ii) ) #strip.setBrightness(ii)
                self.pixels.show()
                time.sleep(.002)

            for ii in range(252,3,-y): #for (int ii = 255 ; ii > 1 ; ii = ii - y){
                self.pixels.fill( self.brightnessRGB(redo, greeno, blueo, ii) ) #strip.setBrightness(ii)
                self.pixels.show()
                time.sleep(.003)
        
            time.sleep(.050) 
           
    def fill_rainbow(self, initialhue, deltahue, delay):
        hue = initialhue
        
        for i in range(self.pixel_number):
            self.pixels[i] =  self.wheel(hue) 
            hue = hue + deltahue
            if hue > 255:
                hue = hue - 255
            self.pixels.show()
            time.sleep(delay)    

    def addGlitter( self,chanceOfGlitter):
        if random.randint(0, 100) < chanceOfGlitter :
            index = random.randint(0, self.pixel_number-1)
            self.pixels[ index ] = (255,255,255)

    def rainbowWithGlitter(self, initialhue, deltahue, delay, cycles):
        hue = initialhue
        for loop in range(cycles):
            # built-in FastLED rainbow, plus some random sparkly glitter
            #rainbow() #fill_rainbow( leds, NUM_LEDS, gHue, 7);
            self.fill_rainbow(hue, deltahue, 0)
            self.addGlitter(80)

            hue = hue + 1
            if hue == 256:
                hue = 0
            time.sleep(delay)

    def confetti(self, delay, cycles):
        for loop in range(cycles):
            # random colored speckles that blink in and fade smoothly
            self.fadeall(10)
            pos = random.randint(0, self.pixel_number-1)
            hue = random.randint(0, 64)
            #pixels[pos] += CHSV( gHue + random8(64), 200, 255);
            self.pixels[pos] = self.wheel(hue)
            self.pixels.show()
            time.sleep(delay)

    def sinelon(self, hue, fadescale, delay, cycles):
        for loop in range(cycles):
            # a colored dot sweeping back and forth, with fading trails
            self.fadeall(fadescale) 
            beatsin = (math.sin( loop/self.pixel_number))
            pos = (self.pixel_number) * (beatsin+1)/2
            
            #pixels[pos] += CHSV( gHue, 255, 192)
            self.pixels[int(pos)] = self.wheel(hue)
            self.pixels.show()
            time.sleep(delay)

    def bpm(self, pallet, delay, cycles): 
        # colored stripes pulsing at a defined Beats-Per-Minute (BPM)
        """
        uint8_t BeatsPerMinute = 62;
        CRGBPalette16 palette = PartyColors_p;
        uint8_t beat = beatsin8( BeatsPerMinute, 64, 255);
        for( int i = 0; i < NUM_LEDS; i++) { //9948
            leds[i] = ColorFromPalette(palette, gHue+(i*2), beat-gHue+(i*10));
        """
        gHue = 0
        for loop in range(cycles):

            #beat = beatsin8( BeatsPerMinute, 64, 255)
            beatsin = (math.sin( loop/self.pixel_number))
            delta = (255-64) * (beatsin+1)/2
            beat = 64 + delta

            for i in  range(0, self.pixel_number, 1):  #for( int i = 0; i < NUM_LEDS; i++) #9948
                palColor = pallet[i % len(pallet) ]
                
                color = self.brightnessRGB(palColor[0], palColor[1], palColor[2], beat)
                self.pixels[i] = color
            self.pixels.show()
            time.sleep(delay)

    def juggle(self, fadescale, delay, cycles):
        # eight colored dots, weaving in and out of sync with each other
        for loop in range(cycles):
            self.fadeall(fadescale)  #fadeToBlackBy( leds, NUM_LEDS, 20);
            dothue = 0
            for i in  range(0, 8, 1):  #for( int i = 0; i < 8; i++) {
                #leds[beatsin16( i+7, 0, NUM_LEDS-1 )] |= CHSV(dothue, 200, 255);
                beatsin = (math.sin( loop/self.pixel_number))
                index = (i+7) * (beatsin+1)/2
                pixels[int(index)] = self.wheel(dothue)
                dothue += 32
            self.pixels.show()
            time.sleep(delay)

    #Check if main class is style alive - to be run on a thread
    def run(self):
        self.newSocket.start()
        self.newSocket_mqtt.start()
        try:
            while True:

                # Create Socket to communicate
                '''self.newSocket = Cosmo_Communication(self.guirlande_number, self.pixel_number, self.tcp_ip, self.tcp_port, self.buffer_size)
                self.newSocket.start()'''

                print("Cosmoguirlande class run")
                print("state :", self.state)
                print("previous state :", self.state)
                print('self.newSocket.data_rcv :', self.newSocket.data_rcv)
                print('self.newSocket_mqtt.data_rcv :', self.newSocket_mqtt.data_rcv)
                self.previous_state = self.state

                '''# wait for animation type and threshold
                if self.newSocket.data_rcv.startswith("cosmoguirlande,manual"):
                    print("manual control, do nothing while checkbox is on")
                    # time.sleep(0.3)

                elif self.newSocket.data_rcv.startswith("cosmoguirlande,strombo"):
                    self.state = "strombo"
                    self.stromboscope(self.color1, 0.05)
                    # time.sleep(0.3)

                elif self.newSocket.data_rcv.startswith('cosmoguirlande,color1'):
                    self.state = 'color1'
                    try:
                        function_type, function, self.color1 = self.newSocket.data_rcv.split(',')
                    except :
                        function_type, function, self.color1 = self.newSocket_mqtt.data_rcv.split(',')

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

                elif self.newSocket.data_rcv.startswith('cosmoguirlande,color2') :
                    self.state = 'color2'
                    try:
                        function_type, function, self.color2 = self.newSocket.data_rcv.split(',')
                    except:
                        function_type, function, self.color2 = self.newSocket_mqtt.data_rcv.split(',')

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

                elif self.newSocket.data_rcv.startswith("cosmoguirlande,rainbow") :
                    self.state = "rainbow"
                    for j in range(2):
                        self.rainbow_cycle(0.01)

                elif self.newSocket.data_rcv.startswith("cosmoguirlande,blackout"):
                    self.state = "blackout"
                    self.blackout()

                elif self.newSocket.data_rcv.startswith('cosmoguirlande,chase'):
                    self.state = "chase"
                    try:
                        function_type, function, chase_speed, chase_size = self.newSocket.data_rcv.split(',')
                    except :
                        function_type, function, chase_speed, chase_size = self.newSocket_mqtt.data_rcv.split(',')
                    try:
                        self.chase_speed = float(chase_speed)
                    except ValueError:
                        self.chase_speed = 0
                    try:
                        self.chase_size = int(chase_size)
                    except ValueError:
                        self.chase_size = 0
                    self.chase()

                elif self.newSocket.data_rcv.startswith('cosmoguirlande,comet') :
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

                elif self.newSocket.data_rcv.startswith('cosmoguirlande,pulse') :
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

                elif self.newSocket.data_rcv.startswith('cosmoguirlande,solid') :
                    self.state = "solid"
                    self.solid()
                    time.sleep(0.5)

                elif self.newSocket.data_rcv.startswith('cosmoguirlande,colorcycle') :
                    self.state = "colorcycle"
                    function_type, function, color1 , color2 = self.newSocket.data_rcv.split(',')
                    self.color1 = color1
                    self.color2 = color2
                    #☻self.colorcycle()

                elif self.newSocket.data_rcv.startswith('cosmoguirlande,dancingPiScroll') :
                    self.state = "dancingPiScroll"
                    self.blackout()
                    self.dancingPiScroll()

                elif self.newSocket.data_rcv.startswith('cosmoguirlande,dancingPiEnergy') :
                    self.state = "dancingPiEnergy"
                    self.blackout()
                    self.dancingPiEnergy()

                elif self.newSocket.data_rcv.startswith('cosmoguirlande,dancingPiSpectrum') :
                    self.state = "dancingPiSpectrum"
                    self.blackout()
                    self.dancingPiSpectrum()

                elif self.newSocket.data_rcv.startswith('cosmoguirlande,stop_dancingPiScroll') :
                    self.state = "stop_dancingPiScroll"
                    self.stop_dancingPiScroll()

                elif self.newSocket.data_rcv.startswith('cosmoguirlande,stop_dancingPiEnergy') :
                    self.state = "stop_dancingPiEnergy"
                    self.stop_dancingPiEnergy()

                elif self.newSocket.data_rcv.startswith('cosmoguirlande,stop_dancingPiSpectrum') :
                    self.state = "stop_dancingPiSpectrum"
                    self.stop_dancingPiSpectrum()

                elif self.newSocket.data_rcv.startswith("cosmoguirlande,R") :
                    self.state = "R"
                    function_type, function, self.r = self.newSocket.data_rcv.split(',')
                    self.changeColor(self.r, self.g, self.b, self.w)
                    # time.sleep(0.5) 

                elif self.newSocket.data_rcv.startswith("cosmoguirlande,G") :
                    self.state = "G"
                    function_type, function, self.g = self.newSocket.data_rcv.split(',')
                    self.changeColor(self.r, self.g, self.b, self.w)
                    # time.sleep(0.5) 

                elif self.newSocket.data_rcv.startswith("cosmoguirlande,B") :
                    self.state = "B"
                    function_type, function, self.b = self.newSocket.data_rcv.split(',')
                    self.changeColor(self.r, self.g, self.b, self.w)
                    # time.sleep(0.5) 

                elif self.newSocket.data_rcv.startswith("cosmoguirlande,W") :
                    self.state = "W"
                    function_type, function, self.w = self.newSocket.data_rcv.split(',')
                    self.changeColor(self.r, self.g, self.b, self.w)
                    # time.sleep(0.5) 
                
                elif self.newSocket.data_rcv.startswith("cosmoguirlande,colorAll2Color") :
                    self.state = "colorAll2Color"
                    function_type, function = self.newSocket.data_rcv.split(',')
                    self.colorAll2Color((int(self.r), int(self.g), int(self.b)), (255,165,0))
                    # time.sleep(0.5) 

                elif self.newSocket.data_rcv.startswith("cosmoguirlande,FadeInOut") :
                    self.state = "FadeInOut"
                    function_type, function= self.newSocket.data_rcv.split(',')
                    self.FadeInOut(self.r, self.g, self.b, 0)
                    # time.sleep(0.5) 

                elif self.newSocket.data_rcv.startswith("cosmoguirlande,Strobe") :
                    self.state = "Strobe"
                    function_type, function= self.newSocket.data_rcv.split(',')
                    self.Strobe(self.r, self.g, self.b,  10, 0, 1)
                    # time.sleep(0.5) 

                elif self.newSocket.data_rcv.startswith("cosmoguirlande,HalloweenEyes") :
                    self.state = "HalloweenEyes"
                    function_type, function = self.newSocket.data_rcv.split(',')
                    self.HalloweenEyes(self.r, self.g, self.b, 1, 1, True, 10, 1, 3)
                    # time.sleep(0.5) 

                elif self.newSocket.data_rcv.startswith("cosmoguirlande,CylonBounce") :
                    self.state = "CylonBounce"
                    function_type, function = self.newSocket.data_rcv.split(',')
                    self.CylonBounce(self.r, self.g, self.b, 2, 0, 0)
                    # time.sleep(0.5) 

                elif self.newSocket.data_rcv.startswith("cosmoguirlande,NewKITT") :
                    self.state = "NewKITT"
                    function_type, function = self.newSocket.data_rcv.split(',')
                    self.NewKITT(self.r, self.g, self.b, 4, 0, 0)
                    # time.sleep(0.5) 

                elif self.newSocket.data_rcv.startswith("cosmoguirlande,Twinkle") :
                    self.state = "Twinkle"
                    function_type, function= self.newSocket.data_rcv.split(',')
                    self.Twinkle(self.r, self.g, self.b, 10, 0.1, False)
                    # time.sleep(0.5) 

                elif self.newSocket.data_rcv.startswith("cosmoguirlande,TwinkleRandom") :
                    self.state = "TwinkleRandom"
                    function_type, function = self.newSocket.data_rcv.split(',')
                    self.TwinkleRandom(20, 0.1, False)
                    # time.sleep(0.5) 
 
                elif self.newSocket.data_rcv.startswith("cosmoguirlande,SnowSparkle") :
                    self.state = "SnowSparkle"
                    function_type, function = self.newSocket.data_rcv.split(',')
                    self.SnowSparkle(self.r, self.g, self.b, 100, 0.1, 0.3 )
                    # time.sleep(0.5) 

                elif self.newSocket.data_rcv.startswith("cosmoguirlande,*RunningLights"):
                    self.state = "RunningLights"
                    function_type, function = self.newSocket.data_rcv.split(',')
                    self.RunningLights(self.r, self.g, self.b, 0)
                    # time.sleep(0.5) 

                elif self.newSocket.data_rcv.startswith("cosmoguirlande,colorWipe") :
                    self.state = "colorWipe"
                    function_type, function = self.newSocket.data_rcv.split(',')
                    self.colorWipe(self.r, self.g, self.b, 0 )
                    # time.sleep(0.5) 

                elif self.newSocket.data_rcv.startswith("cosmoguirlande,theaterChaseRainbow") :
                    self.state = "theaterChaseRainbow"
                    function_type, function = self.newSocket.data_rcv.split(',')
                    self.theaterChaseRainbow(0.1, 30)
                    # time.sleep(0.5) 

                elif self.newSocket.data_rcv.startswith("cosmoguirlande,Fire") :
                    self.state = "Fire"
                    function_type, function = self.newSocket.data_rcv.split(',')
                    while self.newSocket.data_rcv.startswith('cosmoguirlande,Fire') or  self.newSocket_mqtt.data_rcv.startswith('cosmoguirlande,Fire'):
                        self.Fire(55, 120,0, 100)

                elif self.newSocket.data_rcv.startswith("cosmoguirlande,FireCustom") :
                    self.state = "FireCustom"
                    function_type, function = self.newSocket.data_rcv.split(',')
                    while self.newSocket.data_rcv.startswith('cosmoguirlande,FireCustom') or  self.newSocket_mqtt.data_rcv.startswith('cosmoguirlande,FireCustom'):
                        self.FireCustom(self.r, self.g, self.b )

                elif self.newSocket.data_rcv.startswith("cosmoguirlande,meteorRain")  :
                    self.state = "meteorRain"
                    function_type, function = self.newSocket.data_rcv.split(',')
                    self.meteorRain(self.r, self.g, self.b, 10, 64, True, 1, 0 )

                elif self.newSocket.data_rcv.startswith("cosmoguirlande,fadeToBlack"):
                    self.state = "fadeToBlack"
                    function_type, function= self.newSocket.data_rcv.split(',')
                    #self.fadeToBlack(self.r, self.g, self.b)

                elif self.newSocket.data_rcv.startswith("cosmoguirlande,*BouncingBalls") :
                    self.state = "BouncingBalls"
                    function_type, function = self.newSocket.data_rcv.split(',')
                    self.BouncingBalls(255, 0, 0, 3, 100) 
                    # time.sleep(0.5) 

                elif self.newSocket.data_rcv.startswith("cosmoguirlande,*BouncingColoredBalls") :
                    self.state = "BouncingColoredBalls"
                    function_type, function = self.newSocket.data_rcv.split(',')
                    self.BouncingColoredBalls(3, ((255,0,0),(0,255,0),(0,0,255)), 1000)

                elif self.newSocket.data_rcv.startswith("cosmoguirlande,Matrix") :
                    self.state = "Matrix"
                    function_type, function = self.newSocket.data_rcv.split(',')
                    self.pixels.fill((0, 0, 0))
                    self.pixels.show()
                    self.matrix(10, 0, 300) 
                    # time.sleep(0.5) 

                elif self.newSocket.data_rcv.startswith("cosmoguirlande,*Drain") :
                    self.state = "Drain"
                    function_type, function = self.newSocket.data_rcv.split(',')
                    self.drain(self.levelobjcount, 0)
                    # time.sleep(0.5) 

                elif self.newSocket.data_rcv.startswith("cosmoguirlande,Pancake"):
                    self.state = "Pancake"
                    function_type, function = self.newSocket.data_rcv.split(',')
                    self.pancake(self.levelgroups, 0)
                    # time.sleep(0.5) 

                elif self.newSocket.data_rcv.startswith("cosmoguirlande,HeartBeat") :
                    self.state = "HeatBeat"
                    function_type, function = self.newSocket.data_rcv.split(',')
                    # HeartBeat(red, green, blue, cycles):
                    self.HeartBeat(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), 2)
                    # time.sleep(0.5) 

                elif self.newSocket.data_rcv.startswith("cosmoguirlande,rainbowWithGlitter") :
                    self.state = "rainbowWithGlitter"
                    function_type, function = self.newSocket.data_rcv.split(',')
                    self.rainbowWithGlitter(0, 7, 0, 100)
                    # time.sleep(0.5) 

                elif self.newSocket.data_rcv.startswith("cosmoguirlande,Confetti")  :
                    self.state = "Confetti"
                    function_type, function = self.newSocket.data_rcv.split(',')
                    self.confetti(0.1, 1000)
                    # time.sleep(0.5) 

                elif self.newSocket.data_rcv.startswith("cosmoguirlande,Sinelon"):
                    self.state = "Sinelon"
                    function_type, function = self.newSocket.data_rcv.split(',')
                    self.sinelon(0, 230, 0, 500)
                    # time.sleep(0.5) 

                elif self.newSocket.data_rcv.startswith("cosmoguirlande,**BPM")  :
                    self.state = "BPM"
                    function_type, function = self.newSocket.data_rcv.split(',')
                    self.bpm(self.PartyColors_p, 0, 50)
                    # time.sleep(0.5) 
                '''
                ######################################################################################################################
                if self.newSocket_mqtt.data_rcv.startswith("cosmoguirlande,manual") :
                    print("manual control, do nothing while checkbox is on")
                    time.sleep(0.03)

                elif self.newSocket_mqtt.data_rcv.startswith("cosmoguirlande,strombo") :
                    self.state = "strombo"
                    self.stromboscope(self.color1, 0.05)
                    time.sleep(0.03)

                elif self.newSocket_mqtt.data_rcv.startswith('cosmoguirlande,color1') :
                    self.state = 'color1'
                    function_type, function, self.color1 = self.newSocket_mqtt.data_rcv.split(',')
        
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
                    time.sleep(0.03)

                elif self.newSocket_mqtt.data_rcv.startswith('cosmoguirlande,color2') :
                    self.state = 'color2'
                    function_type, function, self.color2 = self.newSocket_mqtt.data_rcv.split(',')

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
                    time.sleep(0.03)

                elif self.newSocket_mqtt.data_rcv.startswith("cosmoguirlande,rainbow")  :
                    self.state = "rainbow"
                    for j in range(2):
                        self.rainbow_cycle(0.01)
                    time.sleep(0.03)

                elif self.newSocket_mqtt.data_rcv.startswith("cosmoguirlande,blackout") :
                    self.state = "blackout"
                    self.blackout()
                    time.sleep(0.03)

                elif self.newSocket_mqtt.data_rcv.startswith('cosmoguirlande,chase') :
                    self.state = "chase"
                    try:
                        function_type, function, chase_speed, chase_size = self.newSocket_mqtt.data_rcv.split(',')
                    except :
                        function_type, function, chase_speed, chase_size = self.newSocket_mqtt_mqtt.data_rcv.split(',')
                    try:
                        self.chase_speed = float(chase_speed)
                    except ValueError:
                        self.chase_speed = 0
                    try:
                        self.chase_size = int(chase_size)
                    except ValueError:
                        self.chase_size = 0
                    self.chase()
                    time.sleep(0.03)

                elif self.newSocket_mqtt.data_rcv.startswith('cosmoguirlande,comet') :
                    self.state = "comet"
                    function_type, function, comet_speed, comet_tail = self.newSocket_mqtt.data_rcv.split(',')
                    try:
                        self.comet_speed = float(comet_speed)
                    except ValueError:
                        self.comet_speed = 0
                    try:
                        self.comet_tail = int(comet_tail)
                    except ValueError:
                        self.comet_tail = 0
                    self.comet()
                    time.sleep(0.03)

                elif self.newSocket_mqtt.data_rcv.startswith('cosmoguirlande,sparkle') :
                    self.state = "sparkle"
                    function_type, function, sparkle_speed, sparkle_num = self.newSocket_mqtt.data_rcv.split(',')
                    try:
                        self.sparkle_speed = float(sparkle_speed)
                    except ValueError:
                        self.sparkle_speed = 0
                    try:
                        self.sparkle_num = int(sparkle_num)
                    except ValueError:
                        self.sparkle_num = 0
                    self.sparkle()
                    time.sleep(0.03)

                elif self.newSocket_mqtt.data_rcv.startswith('cosmoguirlande,pulse') :
                    self.state = "pulse"
                    function_type, function, pulse_period, pulse_speed = self.newSocket_mqtt.data_rcv.split(',')
                    try:
                        self.pulse_period = float(pulse_period)
                    except ValueError:
                        self.pulse_period = 0
                    try:
                        self.pulse_speed = float(pulse_speed)
                    except ValueError:
                        self.pulse_speed = 0
                    self.pulse()
                    time.sleep(0.03)

                elif self.newSocket_mqtt.data_rcv.startswith('cosmoguirlande,solid') :
                    self.state = "solid"
                    self.solid()
                    time.sleep(0.05)

                elif self.newSocket_mqtt.data_rcv.startswith('cosmoguirlande,colorcycle') :
                    self.state = "colorcycle"
                    function_type, function, color1 , color2 = self.newSocket_mqtt.data_rcv.split(',')
                    self.color1 = color1
                    self.color2 = color2
                    #☻self.colorcycle()
                    time.sleep(0.03)

                elif self.newSocket_mqtt.data_rcv.startswith('cosmoguirlande,dancingPiScroll') :
                    self.state = "dancingPiScroll"
                    self.blackout()
                    self.dancingPiScroll()
                    time.sleep(0.03)

                elif self.newSocket_mqtt.data_rcv.startswith('cosmoguirlande,dancingPiEnergy') :
                    self.state = "dancingPiEnergy"
                    self.blackout()
                    self.dancingPiEnergy()
                    time.sleep(0.03)

                elif self.newSocket_mqtt.data_rcv.startswith('cosmoguirlande,dancingPiSpectrum') :
                    self.state = "dancingPiSpectrum"
                    self.blackout()
                    self.dancingPiSpectrum()
                    time.sleep(0.03)

                elif self.newSocket_mqtt.data_rcv.startswith('cosmoguirlande,stop_dancingPiScroll') :
                    self.state = "stop_dancingPiScroll"
                    self.stop_dancingPiScroll()
                    time.sleep(0.03)

                elif self.newSocket_mqtt.data_rcv.startswith('cosmoguirlande,stop_dancingPiEnergy') :
                    self.state = "stop_dancingPiEnergy"
                    self.stop_dancingPiEnergy()
                    time.sleep(0.03)

                elif self.newSocket_mqtt.data_rcv.startswith('cosmoguirlande,stop_dancingPiSpectrum') :
                    self.state = "stop_dancingPiSpectrum"
                    self.stop_dancingPiSpectrum()
                    time.sleep(0.03)

                elif self.newSocket_mqtt.data_rcv.startswith("cosmoguirlande,R") :
                    self.state = "R"
                    function_type, function, self.r = self.newSocket_mqtt.data_rcv.split(',')
                    self.changeColor(self.r, self.g, self.b, self.w)
                    # time.sleep(0.5) 

                elif self.newSocket_mqtt.data_rcv.startswith("cosmoguirlande,G") :
                    self.state = "G"
                    function_type, function, self.g = self.newSocket_mqtt.data_rcv.split(',')
                    self.changeColor(self.r, self.g, self.b, self.w)
                    # time.sleep(0.5) 

                elif self.newSocket_mqtt.data_rcv.startswith("cosmoguirlande,B") :
                    self.state = "B"
                    function_type, function, self.b = self.newSocket_mqtt.data_rcv.split(',')
                    self.changeColor(self.r, self.g, self.b, self.w)
                    # time.sleep(0.5) 

                elif self.newSocket_mqtt.data_rcv.startswith("cosmoguirlande,W") :
                    self.state = "W"
                    function_type, function, self.w = self.newSocket_mqtt.data_rcv.split(',')
                    self.changeColor(self.r, self.g, self.b, self.w)
                    # time.sleep(0.5) 
                
                elif self.newSocket_mqtt.data_rcv.startswith("cosmoguirlande,colorAll2Color"):
                    self.state = "colorAll2Color"
                    function_type, function = self.newSocket_mqtt.data_rcv.split(',')
                    self.colorAll2Color((int(self.r), int(self.g), int(self.b)), (255,165,0))
                    time.sleep(0.03)

                elif self.newSocket_mqtt.data_rcv.startswith("cosmoguirlande,FadeInOut"):
                    self.state = "FadeInOut"
                    function_type, function= self.newSocket_mqtt.data_rcv.split(',')
                    self.FadeInOut(self.r, self.g, self.b, 0)
                    # time.sleep(0.5) 

                elif self.newSocket_mqtt.data_rcv.startswith("cosmoguirlande,Strobe") :
                    self.state = "Strobe"
                    function_type, function= self.newSocket_mqtt.data_rcv.split(',')
                    self.Strobe(self.r, self.g, self.b,  10, 0, 1)
                    # time.sleep(0.5) 

                elif self.newSocket_mqtt.data_rcv.startswith("cosmoguirlande,HalloweenEyes"):
                    self.state = "HalloweenEyes"
                    function_type, function = self.newSocket_mqtt.data_rcv.split(',')
                    self.HalloweenEyes(self.r, self.g, self.b, 1, 1, True, 10, 1, 3)
                    # time.sleep(0.5) 

                elif self.newSocket_mqtt.data_rcv.startswith("cosmoguirlande,CylonBounce") :
                    self.state = "CylonBounce"
                    function_type, function = self.newSocket_mqtt.data_rcv.split(',')
                    self.CylonBounce(self.r, self.g, self.b, 2, 0, 0)
                    # time.sleep(0.5) 

                elif self.newSocket_mqtt.data_rcv.startswith("cosmoguirlande,NewKITT") :
                    self.state = "NewKITT"
                    function_type, function = self.newSocket_mqtt.data_rcv.split(',')
                    self.NewKITT(self.r, self.g, self.b, 4, 0, 0)
                    # time.sleep(0.5) 

                elif self.newSocket_mqtt.data_rcv.startswith("cosmoguirlande,Twinkle") :
                    self.state = "Twinkle"
                    function_type, function= self.newSocket_mqtt.data_rcv.split(',')
                    self.Twinkle(self.r, self.g, self.b, 10, 0.1, False)
                    # time.sleep(0.5) 

                elif self.newSocket_mqtt.data_rcv.startswith("cosmoguirlande,TwinkleRandom"):
                    self.state = "TwinkleRandom"
                    function_type, function = self.newSocket_mqtt.data_rcv.split(',')
                    self.TwinkleRandom(20, 0.1, False)
                    # time.sleep(0.5) 
 
                elif self.newSocket_mqtt.data_rcv.startswith("cosmoguirlande,SnowSparkle") :
                    self.state = "SnowSparkle"
                    function_type, function = self.newSocket_mqtt.data_rcv.split(',')
                    self.SnowSparkle(self.r, self.g, self.b, 100, 0.1, 0.3 )
                    # time.sleep(0.5) 

                elif self.newSocket_mqtt.data_rcv.startswith("cosmoguirlande,*RunningLights") :
                    self.state = "RunningLights"
                    function_type, function = self.newSocket_mqtt.data_rcv.split(',')
                    self.RunningLights(self.r, self.g, self.b, 0)
                    # time.sleep(0.5) 

                elif self.newSocket_mqtt.data_rcv.startswith("cosmoguirlande,colorWipe") :
                    self.state = "colorWipe"
                    function_type, function = self.newSocket_mqtt.data_rcv.split(',')
                    self.colorWipe(self.r, self.g, self.b, 0 )
                    # time.sleep(0.5) 

                elif self.newSocket_mqtt.data_rcv.startswith("cosmoguirlande,theaterChaseRainbow") :
                    self.state = "theaterChaseRainbow"
                    function_type, function = self.newSocket_mqtt.data_rcv.split(',')
                    self.theaterChaseRainbow(0.1, 30)
                    # time.sleep(0.5) 

                elif self.newSocket_mqtt.data_rcv.startswith("cosmoguirlande,Fire") :
                    self.state = "Fire"
                    function_type, function = self.newSocket_mqtt.data_rcv.split(',')
                    while self.newSocket_mqtt.data_rcv.startswith('cosmoguirlande,Fire') :
                        self.Fire(55, 120,0, 100)

                elif self.newSocket_mqtt.data_rcv.startswith("cosmoguirlande,FireCustom") :
                    self.state = "FireCustom"
                    function_type, function = self.newSocket_mqtt.data_rcv.split(',')
                    while self.newSocket_mqtt.data_rcv.startswith('cosmoguirlande,FireCustom'):
                        self.FireCustom(self.r, self.g, self.b )

                elif self.newSocket_mqtt.data_rcv.startswith("cosmoguirlande,meteorRain") :
                    self.state = "meteorRain"
                    function_type, function = self.newSocket_mqtt.data_rcv.split(',')
                    self.meteorRain(self.r, self.g, self.b, 10, 64, True, 1, 0 )

                elif self.newSocket_mqtt.data_rcv.startswith("cosmoguirlande,fadeToBlack") :
                    self.state = "fadeToBlack"
                    function_type, function= self.newSocket_mqtt.data_rcv.split(',')
                    #self.fadeToBlack(self.r, self.g, self.b)

                elif self.newSocket_mqtt.data_rcv.startswith("cosmoguirlande,*BouncingBalls") :
                    self.state = "BouncingBalls"
                    function_type, function = self.newSocket_mqtt.data_rcv.split(',')
                    self.BouncingBalls(255, 0, 0, 3, 100) 
                    # time.sleep(0.5) 

                elif self.newSocket_mqtt.data_rcv.startswith("cosmoguirlande,*BouncingColoredBalls") :
                    self.state = "BouncingColoredBalls"
                    function_type, function = self.newSocket_mqtt.data_rcv.split(',')
                    self.BouncingColoredBalls(3, ((255,0,0),(0,255,0),(0,0,255)), 1000)

                elif self.newSocket_mqtt.data_rcv.startswith("cosmoguirlande,Matrix") :
                    self.state = "Matrix"
                    function_type, function = self.newSocket_mqtt.data_rcv.split(',')
                    self.pixels.fill((0, 0, 0))
                    self.pixels.show()
                    self.matrix(10, 0, 300) 
                    # time.sleep(0.5) 

                elif self.newSocket_mqtt.data_rcv.startswith("cosmoguirlande,*Drain") :
                    self.state = "Drain"
                    function_type, function = self.newSocket_mqtt.data_rcv.split(',')
                    self.drain(self.levelobjcount, 0)
                    # time.sleep(0.5) 

                elif self.newSocket_mqtt.data_rcv.startswith("cosmoguirlande,Pancake"):
                    self.state = "Pancake"
                    function_type, function = self.newSocket_mqtt.data_rcv.split(',')
                    self.pancake(self.levelgroups, 0)
                    # time.sleep(0.5) 

                elif self.newSocket_mqtt.data_rcv.startswith("cosmoguirlande,HeartBeat"):
                    self.state = "HeatBeat"
                    function_type, function = self.newSocket_mqtt.data_rcv.split(',')
                    # HeartBeat(red, green, blue, cycles):
                    self.HeartBeat(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), 2)
                    # time.sleep(0.5) 

                elif self.newSocket_mqtt.data_rcv.startswith("cosmoguirlande,rainbowWithGlitter") :
                    self.state = "rainbowWithGlitter"
                    function_type, function = self.newSocket_mqtt.data_rcv.split(',')
                    self.rainbowWithGlitter(0, 7, 0, 100)
                    # time.sleep(0.5) 

                elif self.newSocket_mqtt.data_rcv.startswith("cosmoguirlande,Confetti"):
                    self.state = "Confetti"
                    function_type, function = self.newSocket_mqtt.data_rcv.split(',')
                    self.confetti(0.1, 1000)
                    # time.sleep(0.5) 

                elif self.newSocket_mqtt.data_rcv.startswith("cosmoguirlande,Sinelon"):
                    self.state = "Sinelon"
                    function_type, function = self.newSocket_mqtt.data_rcv.split(',')
                    self.sinelon(0, 230, 0, 500)
                    # time.sleep(0.5) 

                elif self.newSocket_mqtt.data_rcv.startswith("cosmoguirlande,**BPM")  :
                    self.state = "BPM"
                    function_type, function = self.newSocket_mqtt.data_rcv.split(',')
                    self.bpm(self.PartyColors_p, 0, 50)
                  

                elif self.state == "nothing":
                    #increse count if last states are "main"
                    if self.previous_state == "nothing":
                        self.watchdog_count = self.watchdog_count +1
                        print("watchdog_count :",self.watchdog_count)
                        # time.sleep(0.5) 
                    #if no messages since last 10 sec (10 "main state), start again
                    elif self.watchdog_count == 20:
                        self.watchdog_count = 0
                        self.run()
                    self.previous_state = self.state

                elif self.state == "restart":
                    self.state = "restart"
                    # Del former, create a new one and start it
                    '''self.newSocket.connexion_serveur.close()
                    self.newSocket = Cosmo_Communication(self.guirlande_number, self.pixel_number, self.tcp_ip, self.tcp_port, self.buffer_size)
                    self.newSocket.start()'''

                else:
                    print("nothing")
                    self.state = "nothing"
                    # time.sleep(1)

                self.previous_message = self.newSocket.data_rcv
                #self.newSocket_mqtt.data_rcv = ""
                #self.newSocket.close()

        except TypeError:
            print("type error")
            self.run()

        except KeyboardInterrupt:
            print("keyboard interrupt, blackout LED")
            self.state = "keyboard"
            if args.clear:
                self.pixels.fill((0, 0, 0, 0))


        for loop in range(cycles):
            #redo =random.randint(0, 255)
            #greeno = random.randint(0, 255)
            #blueo = random.randint(0, 255)
            
            #strip.setPixelColor(2, redo, greeno, blueo)
            pixels.fill((redo, greeno, blueo))
            pixels.show()
            time.sleep(.020)
            
            x = 3
            for ii in range(1,252,x): #for ( ii = 1 ; ii <252 ; ii = ii = ii + x)
                pixels.fill( brightnessRGB(redo, greeno, blueo, ii) ) #strip.setBrightness(ii)
                pixels.show()
                time.sleep(.005)

            for ii in range(252,3,-x): #for (int ii = 252 ; ii > 3 ; ii = ii - x){
                pixels.fill( brightnessRGB(redo, greeno, blueo, ii) ) #strip.setBrightness(ii)
                pixels.show()
                time.sleep(.003)

            time.sleep(.0010)
            
            y = 6
            for ii in range(1,252,y): #for (int ii = 1 ; ii <255 ; ii = ii = ii + y){
                pixels.fill( brightnessRGB(redo, greeno, blueo, ii) ) #strip.setBrightness(ii)
                pixels.show()
                time.sleep(.002)

            for ii in range(252,3,-y): #for (int ii = 255 ; ii > 1 ; ii = ii - y){
                pixels.fill( brightnessRGB(redo, greeno, blueo, ii) ) #strip.setBrightness(ii)
                pixels.show()
                time.sleep(.003)
        
            time.sleep(.050) 


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

    # Run ex: sudo python3 Desktop/Cosmo_guirlande_rpi.py 1 30 192.168.0.17 50001 1024 RGBW

    cosmo_guirlande = Cosmo_guirlande_rpi(args.guirlande_number, args.num_pixel, args.server_tcp_ip, args.tcp_port, args.buffer_size, args.RGB)

    while(True):
        try:
            cosmo_guirlande.run()
        except :
            cosmo_guirlande.run()