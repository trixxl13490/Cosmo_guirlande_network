# Simple test for NeoPixels on Raspberry Pi
import argparse
import time
import board
import neopixel
import threading
import socket


class Cosmo_guirlande_rpi():

    def __init__(self, guirlande_number, pixel_number, tcp_ip, tcp_port, buffer_size):
        self.guirlande_number = guirlande_number
        self.pixel_number = pixel_number
        self.tcp_ip = str(tcp_ip)
        self.tcp_port = tcp_port
        self.buffer_size = buffer_size
        self.r = '0'
        self.g = '0'
        self.b = '0'
        self.w = '0'
        self.fixed_color = False

        print("Cosmo Guirlande Number: " + str(self.guirlande_number))
        print("TCP ip server: " + str(self.tcp_ip))
        print("TCP port : " + str(self.tcp_port))
        print("TCP buffer size: " + str(self.buffer_size))

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

    def rainbow_cycle(self, wait):
        for j in range(255):
            for i in range(self.pixel_number):
                pixel_index = (i * 256 // self.pixel_number) + j
                pixels[i] = self.wheel(pixel_index & 255)
            pixels.show()
            time.sleep(wait)

    def stromboscope(self, color, wait_s):
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
        pixels.fill((int(r), int(g), int(b), int(w)))
        pixels.show()
        time.sleep(0.3)

    def theaterChase(self, color, wait_ms=50, iterations=10):
        """Movie theater light style chaser animation."""
        for j in range(iterations):
            for q in range(3):
                for i in range(0, self.pixel_number, 3):
                    pixel_index = i + q
                    pixels[pixel_index] = color
                pixels.show()
                time.sleep(wait_ms / 1000.0)
                for i in range(0, self.pixel_number, 3):
                    pixels[i] = 0

    def theaterChaseRainbow(self, wait_ms=50):
        """Rainbow movie theater light style chaser animation."""
        for j in range(256):
            for q in range(3):
                for i in range(0, self.pixel_number, 3):
                    pixel_index = (i * 256 // self.pixel_number) + j
                    pixels[pixel_index] = (self.wheel((i + j) % 255))
                pixels.show()
                time.sleep(wait_ms / 1000.0)
                for i in range(0, self.pixel_number, 3):
                    pixels[i] = (i + q, 0)

    def multiColorWipe(self, color1, color2, wait_ms=5):
        """Wipe color across multiple LED strips a pixel at a time."""
        for i in range(self.pixel_number):
            if i % 2:
                # even number
                pixels[i] = color1
                pixels.show()
                time.sleep(wait_ms / 1000.0)
            else:
                # odd number
                pixels[i] = color1
                pixels.show()
                time.sleep(wait_ms / 1000.0)

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
                data_rcv = connexion_serveur.recv(self.buffer_size)
                data_rcv = data_rcv.decode()
                print("data_rcv : ", data_rcv)

                ##fermeture connexion
                connexion_serveur.close()

                if data_rcv.startswith("cosmoguirlande,strombo"):
                    self.stromboscope((int(self.r), int(self.g), int(self.b), int(self.w)), 0.01)
                    time.sleep(0.1)
                elif data_rcv.startswith("cosmoguirlande,rainbow"):
                    for j in range(2):
                        self.rainbow_cycle(0.01)

                elif data_rcv.startswith("cosmoguirlande,blackout"):
                    self.blackout()

                elif data_rcv.startswith("cosmoguirlande,theaterChase"):
                    self.theaterChase((int(self.r), int(self.g), int(self.b), int(self.w)))

                elif data_rcv.startswith("cosmoguirlande,theaterChaseRainbow"):
                    self.theaterChaseRainbow()

                elif data_rcv.startswith("cosmoguirlande,multiColorWipe"):
                    self.multiColorWipe((int(self.r), int(self.g), int(self.b), int(self.w)), (int(self.r)+256, int(self.g)+256, int(self.b)+256, int(self.w)+256))

                elif data_rcv.startswith("cosmoguirlande,R"):
                    function_type, function, self.r = data_rcv.split(',')
                    self.changeColor(self.r, self.g, self.b, self.w)
                    time.sleep(0.5)

                elif data_rcv.startswith("cosmoguirlande,G"):
                    function_type, function, self.g = data_rcv.split(',')
                    self.changeColor(self.r, self.g, self.b, self.w)
                    time.sleep(0.5)

                elif data_rcv.startswith("cosmoguirlande,B"):
                    function_type, function, self.b = data_rcv.split(',')
                    self.changeColor(self.r, self.g, self.b, self.w)
                    time.sleep(0.5)

                elif data_rcv.startswith("cosmoguirlande,W"):
                    function_type, function, self.w = data_rcv.split(',')
                    self.changeColor(self.r, self.g, self.b, self.w)
                    time.sleep(0.5)

                else:
                    print("nothing")
                    time.sleep(1)
                    pass

        except ConnectionResetError:
            print("connection reset")
            time.sleep(1)
            self.run()

        except KeyboardInterrupt:
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
    cosmo_guirlande = Cosmo_guirlande_rpi(args.guirlande_number, args.num_pixel, args.server_tcp_ip, args.tcp_port,
                                          args.buffer_size)
    cosmo_guirlande.run()
