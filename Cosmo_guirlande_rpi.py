# Simple test for NeoPixels on Raspberry Pi
import argparse
import time
import board
import neopixel
import threading
import socket


class Cosmo_guirlande_rpi():
    def __init__(self,guirlande_number,pixel_number,tcp_ip, tcp_port, buffer_size):
        self.guirlande_number = guirlande_number
        self.pixel_number = pixel_number
        self.tcp_ip = str(tcp_ip)
        self.tcp_port = tcp_port
        self.buffer_size = buffer_size
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


    def rainbow_cycle(self,wait):
        for j in range(255):
            for i in range(self.pixel_number):
                pixel_index = (i * 256 // self.pixel_number) + j
                pixels[i] = self.wheel(pixel_index & 255)
            pixels.show()
            time.sleep(wait)


    def theaterChase(self, color, wait_ms=50, iterations=10):
        """Movie theater light style chaser animation."""
        for j in range(iterations):
            for q in range(3):
                for i in range(0, self.pixel_number, 3):
                    pixels[i] = (i + q, color)
                pixels.show()
                time.sleep(wait_ms / 1000.0)
                for i in range(0, self.pixel_number, 3):
                    pixels[i] = (i + q, 0)


    def stromboscope(self, color, wait_s):
        pixels.fill(color)
        pixels.show()
        time.sleep(wait_s)
        pixels.fill((0, 0, 0, 0))
        pixels.show()
        time.sleep(wait_s)


    '''
    def theaterChase(self, strip, color, wait_ms=50, iterations=10):
        """Movie theater light style chaser animation."""
        for j in range(iterations):
            for q in range(3):
                for i in range(0, strip.numPixels(), 3):
                    strip.setPixelColor(i + q, color)
                strip.show()
                time.sleep(wait_ms / 1000.0)
                for i in range(0, strip.numPixels(), 3):
                    strip.setPixelColor(i + q, 0)
    
    def theaterChaseRainbow(self, strip, wait_ms=50):
        """Rainbow movie theater light style chaser animation."""
        for j in range(256):
            for q in range(3):
                for i in range(0, strip.numPixels(), 3):
                    strip.setPixelColor(i + q, wheel((i + j) % 255))
                strip.show()
                time.sleep(wait_ms / 1000.0)
                for i in range(0, strip.numPixels(), 3):
                    strip.setPixelColor(i + q, 0)
    
    
    def multiColorWipe(self, color1, color2, wait_ms=5):
        """Wipe color across multiple LED strips a pixel at a time."""
        global strip
    
        for i in range(strip.numPixels()):
            if i % 2:
                # even number
                strip.setPixelColor(i, color1)
                strip.show()
                time.sleep(wait_ms / 1000.0)
    
            else:
                # odd number
                strip.setPixelColor(i, color1)
                strip.show()
                time.sleep(wait_ms / 1000.0)
    
        time.sleep(1)
        '''
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
                line = str("cosmoguirlande_" + str(self.guirlande_number) + "," + str(self.pixel_number) + "," + self.tcp_ip + "," + str(self.tcp_port))
                print(line)
                line = line.encode()
                connexion_serveur.send(line)
                data_rcv = connexion_serveur.recv(self.buffer_size)
                data_rcv = data_rcv.decode()
                print(data_rcv)

                ##fermeture connexion
                connexion_serveur.close()

                for j in range(10):
                    self.stromboscope((0, 150, 150, 0), 0.05)
                    time.sleep(0.2)
                for j in range(2):
                    self.rainbow_cycle(0.01)

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
    pixels = neopixel.NeoPixel(
        board.D18, args.num_pixel, brightness=0.2, auto_write=False, pixel_order=neopixel.RGBW
    )
    print('Press Ctrl-C to quit.')

    #Run ex: sudo python3
    cosmo_guirlande = Cosmo_guirlande_rpi(args.guirlande_number,args.num_pixel, args.server_tcp_ip, args.tcp_port, args.buffer_size)
    cosmo_guirlande.run()


