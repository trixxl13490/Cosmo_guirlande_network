# Simple test for NeoPixels on Raspberry Pi
import argparse
import time
import board
import neopixel
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

class Cosmo_Communication(threading.Thread):

    def __init__(self, guirlande_number, pixel_number, tcp_ip, tcp_port, buffer_size):
        threading.Thread.__init__(self)
        self.guirlande_number = guirlande_number
        self.pixel_number = pixel_number
        self.tcp_ip = str(tcp_ip)
        self.tcp_port = tcp_port
        self.buffer_size = buffer_size
        self.data_rcv = ""

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

        except ConnectionResetError:
            print("connection reset")
            time.sleep(1)
            self.run()

        except TimeoutError:
            print("Timeout Error, start again thread")
            time.sleep(1)
            self.run()

        except KeyboardInterrupt:
            print("keyboard interrupt, blackout LED")
            connexion_serveur.close()

class Cosmo_guirlande_rpi():
    def __init__(self, guirlande_number, pixel_number, tcp_ip, tcp_port, buffer_size):
        self.pixel_number = pixel_number
        self.r = '0'
        self.g = '0'
        self.b = '0'
        self.w = '0'
        self.fixed_color = False
        self.color1 = AMBER
        self.color2 = AMBER
        #Create Socket to communicate
        self.newSocket = Cosmo_Communication(guirlande_number, pixel_number, tcp_ip, tcp_port, buffer_size)
        self.newSocket.start()

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
        while self.newSocket.data_rcv.startswith('cosmoguirlande,strombo'):
            pixels.fill(color)
            pixels.show()
            time.sleep(wait_s)
            pixels.fill((0, 0, 0, 0))
            pixels.show()
            time.sleep(wait_s)

    def blackout(self):
        pixels.fill((0, 0, 0, 0))
        pixels.show()
        time.sleep(1)

    def changeColor(self, r, g, b, w):
        self.color1 = (r,g,b,w)
        pixels.fill((int(r), int(g), int(b), int(w)))
        pixels.show()
        time.sleep(0.3)

    def changeColor1String(self, color):
        self.color1 = color
        solid = Solid(pixels, color=self.color1)
        animations = AnimationSequence(
            solid,
            advance_interval=5,
            auto_clear=True,
        )
        while self.newSocket.data_rcv.startswith('cosmoguirlande,color1'):
            animations.animate()

    def changeColor2String(self, color):
        self.color2 = color
        solid = Solid(pixels, color=self.color2)
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
                pixels[i] = self.wheel(pixel_index & 255)
            pixels.show()
            time.sleep(wait)

    def comet(self):
        comet = Comet(pixels, speed=0.01, color=self.color1, tail_length=10, bounce=True)
        animations = AnimationSequence(
            comet,
            advance_interval=5,
            auto_clear=True,
        )
        while self.newSocket.data_rcv.startswith('cosmoguirlande,comet'):
            animations.animate()

    def chase(self):
        chase = Chase(pixels, speed=0.1, size=3, spacing=6, color=self.color1)
        animations = AnimationSequence(
            chase,
            advance_interval=5,
            auto_clear=True,
        )
        while self.newSocket.data_rcv.startswith('cosmoguirlande,chase'):
            animations.animate()

    def pulse(self):
        pulse = Pulse(pixels, speed=0.1, period=1, color=self.color1)
        animations = AnimationSequence(
            pulse,
            advance_interval=5,
            auto_clear=True,
        )
        while self.newSocket.data_rcv.startswith('cosmoguirlande,pulse'):
            animations.animate()
    def sparkle(self):
        sparkle = Sparkle(pixels, speed=0.1, color=self.color1, num_sparkles=10)
        animations = AnimationSequence(
            sparkle,
            advance_interval=5,
            auto_clear=True,
        )
        while self.newSocket.data_rcv.startswith('cosmoguirlande,sparkle'):
            animations.animate()


    def solid(self):
        solid = Solid(pixels, color=self.color1)
        animations = AnimationSequence(
            solid,
            advance_interval=5,
            auto_clear=True,
        )
        animations.animate()

    def colorcycle(self):
        colorcycle = ColorCycle(pixels, speed=0.4, colors=[self.color1, self.color2])
        animations = AnimationSequence(
            colorcycle,
            advance_interval=5,
            auto_clear=True,
        )
        while self.newSocket.data_rcv.startswith('cosmoguirlande,colorcycle'):
            animations.animate()

    def run(self):
        try:
            while True:
                if self.newSocket.data_rcv.startswith("cosmoguirlande,strombo"):
                    self.stromboscope(self.color1, 0.05)
                    time.sleep(0.3)

                elif self.newSocket.data_rcv.startswith('cosmoguirlande,color1'):
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
                    for j in range(2):
                        self.rainbow_cycle(0.01)

                elif self.newSocket.data_rcv.startswith("cosmoguirlande,blackout"):
                    self.blackout()

                elif self.newSocket.data_rcv.startswith('cosmoguirlande,chase'):
                    self.chase()

                elif self.newSocket.data_rcv.startswith('cosmoguirlande,comet'):
                    self.comet()

                elif self.newSocket.data_rcv.startswith('cosmoguirlande,sparkle'):
                    self.sparkle()

                elif self.newSocket.data_rcv.startswith('cosmoguirlande,pulse'):
                    self.pulse()

                elif self.newSocket.data_rcv.startswith('cosmoguirlande,solid'):
                    self.solid()

                elif self.newSocket.data_rcv.startswith('cosmoguirlande,colorcycle'):
                    self.colorcycle()

                elif self.newSocket.data_rcv.startswith("cosmoguirlande,R"):
                    function_type, function, self.r = self.newSocket.data_rcv.split(',')
                    self.changeColor(self.r, self.g, self.b, self.w)
                    time.sleep(0.5)

                elif self.newSocket.data_rcv.startswith("cosmoguirlande,G"):
                    function_type, function, self.g = self.newSocket.data_rcv.split(',')
                    self.changeColor(self.r, self.g, self.b, self.w)
                    time.sleep(0.5)

                elif self.newSocket.data_rcv.startswith("cosmoguirlande,B"):
                    function_type, function, self.b = self.newSocket.data_rcv.split(',')
                    self.changeColor(self.r, self.g, self.b, self.w)
                    time.sleep(0.5)

                elif self.newSocket.data_rcv.startswith("cosmoguirlande,W"):
                    function_type, function, self.w = self.newSocket.data_rcv.split(',')
                    self.changeColor(self.r, self.g, self.b, self.w)
                    time.sleep(0.5)

                else:
                    print("nothing")
                    time.sleep(1)
                    pass

        except KeyboardInterrupt:
            print("keyboard interrupt, blackout LED")
            if args.clear:
                pixels.fill((0, 0, 0, 0))


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
        board.D18, args.num_pixel, brightness=0.2, auto_write=False, pixel_order=neopixel.RGBW
    )
    print('Press Ctrl-C to quit.')

    # Run ex: sudo python3 Desktop/Cosmo_guirlande_rpi.py 1 30 192.168.0. 50001 1024

    cosmo_guirlande = Cosmo_guirlande_rpi(args.guirlande_number, args.num_pixel, args.server_tcp_ip, args.tcp_port, args.buffer_size)
    cosmo_guirlande.run()
