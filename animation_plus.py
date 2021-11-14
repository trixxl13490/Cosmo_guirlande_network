import neopixel
import time
import board
import argparse
from random import randrange

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
#parser.add_argument('guirlande_number', metavar='guirlande_number', type=int, help='Cosmo Guirlande NUmber')
parser.add_argument('num_pixel', metavar='num_pixel', type=int, help='Number of pixel')
#parser.add_argument('server_tcp_ip', metavar='server_tcp_ip', type=str, help='Server IP')
#parser.add_argument('tcp_port', metavar='tcp_port', type=int, help='Tcp Port')
#parser.add_argument('buffer_size', metavar='buffer_size', type=int, help='Buffer Size')
args = parser.parse_args()

#Led strip init
pixels = neopixel.NeoPixel(
        board.D18, args.num_pixel, brightness=0.2, auto_write=False, pixel_order=neopixel.GRBW
    )

def Fire( Cooling, Sparking, SpeedDelay): #int int int
    cooldown = 0
    y = 0
    num_pixel = int(args.num_pixel)
    heat = [0] * num_pixel  #static byte heat[NUM_LEDS]

    # Step 1.  Cool down every cell a little
    for i in range(num_pixel):
        heat[i] = randrange(0, 254)

    for i in range(num_pixel):
        cooldown = randrange(0, int(((Cooling * 10) / num_pixel) + 2))
        if (cooldown > heat[i]):
            heat[i] = 0
        else:
            heat[i] = heat[i] - cooldown

    # Step 2.  Heat from each cell drifts 'up' and diffuses a little
    #for (k= args.num_pixel - 1; k >= 2; k--):
    for k in range(num_pixel-1, 2, -1):
        heat[k] = (heat[k - 1] + heat[k - 2] + heat[k - 2]) / 3


    # Step 3.  Randomly ignite new 'sparks' near the bottom
    if (randrange(255) < Sparking):
        y = randrange(7)
        heat[y] = heat[y] + randrange(160, 255)

    # Step 4.  Convert heat to LED colors
    for  j in range(num_pixel):
        setPixelHeatColor(j, heat[j])
        pixels.show()
    time.sleep(SpeedDelay)


def setPixelHeatColor(Pixel, temperature):
    # Scale 'heat' down from 0-255 to 0-191
    t192 = round((temperature / 255.0) * 191) #byte t192
    t192 = t192 % 191

    # calculate ramp up from
    heatramp = t192 & 0x3F #byte 0..63
    heatramp <<= 2  # scale up to 0..252

    # figure out which third of the spectrum we're in:
    if (t192 > 0x80):  # hottest
        #setPixel(Pixel, 255, 255, heatramp)
        pixels[Pixel] = (255, 255, heatramp, 0)
    elif(t192 > 0x40):  # middle
        #setPixel(Pixel, 255, heatramp, 0)
        pixels[Pixel] = (255, heatramp,0, 0)
    else:  # coolest
        #setPixel(Pixel, heatramp, 0, 0)
        pixels[Pixel] = (heatramp, 0, 0, 0)

while(True):
    Fire(55,120,0.01)
