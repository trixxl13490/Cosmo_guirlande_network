import PySimpleGUI as sg
import pyaudio
import numpy as np
from scipy import signal
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
import Cosmo_guirlande_rpi

""" RealTime Audio Waveform + fft + High bar + Mid bar + Low bar plot """


# VARS CONSTS:
_VARS = {'window': False,
         'stream': False,
         'audioData': np.array([]),
         'filter_fftData': np.array([]),
         'fftData': np.array([])}

# pysimpleGUI INIT:
AppFont = 'Any 16'
sg.theme('Black')
CanvasSizeWH = 500

layout = [[sg.Graph(canvas_size=(CanvasSizeWH, CanvasSizeWH),
                    graph_bottom_left=(-16, -16),
                    graph_top_right=(116, 116),
                    background_color='#B9B9B9',
                    key='graph')],
          [sg.ProgressBar(4000, orientation='h',
                          size=(20, 20), key='-PROG-')],
          [sg.ProgressBar(400000, orientation='h',
                          size=(20, 20), key='-PROG1-')],
          [sg.ProgressBar(40000, orientation='h',
                          size=(20, 20), key='-PROG2-')],
          [sg.ProgressBar(40000, orientation='h',
                          size=(20, 20), key='-PROG3-')],
          [sg.ProgressBar(40000, orientation='h',
                          size=(20, 20), key='-PROG4-')],
          [sg.Button('Listen', font=AppFont),
           sg.Button('Stop', font=AppFont, disabled=True),
           sg.Button('Exit', font=AppFont)]]
_VARS['window'] = sg.Window('Mic to waveform plot + Max Level',
                            layout, finalize=True)

graph = _VARS['window']['graph']

# INIT vars:
CHUNK = 1024  # Samples: 1024,  512, 256, 128
RATE = 44100  # Equivalent to Human Hearing at 40 kHz
INTERVAL = 0.5  # Sampling Interval in Seconds ie Interval to listen
TIMEOUT = 10  # In ms for the event loop
pAud = pyaudio.PyAudio()

# FUNCTIONS:


def drawAxis():
    graph.DrawLine((0, 50), (100, 50))  # Y Axis
    graph.DrawLine((0, 0), (0, 100))  # X Axis


def drawTicks():

    divisionsX = 12
    multi = int(CHUNK/divisionsX)
    offsetX = int(100/divisionsX)

    divisionsY = 10
    offsetY = int(100/divisionsY)

    for x in range(0, divisionsX+1):
        # print('x:', x)
        graph.DrawLine((x*offsetX, -3), (x*offsetX, 3))
        graph.DrawText(int(x*multi), (x*offsetX, -10), color='black')

    for y in range(0, divisionsY+1):
        graph.DrawLine((-3, y*offsetY), (3, y*offsetY))


def drawAxesLabels():
    graph.DrawText('SAMPLES CHUNK', (50, 10), color='black')
    graph.DrawText('Norm Scaled AUDIO', (-5, 50), color='black', angle=90)


def drawPlot():
    step = 100/CHUNK*2
    gain = 0.001

    # MIN MAX Scaled :
    # mn, mx = np.min(_VARS['audioData']), np.max(_VARS['audioData'])
    # x_scaled = ((_VARS['audioData'] - mn) / (mx - mn))*100

    # Scaled/Centered for display (change to suit signal):
    #x_scaled = ((_VARS['audioData']/100)*gain)+50
    x_scaled = _VARS['fftData'] * gain
    for x in range(513):
        graph.DrawCircle((x*step, (x_scaled[x])),
                         0.4, line_color='black', fill_color='black')

# PYAUDIO STREAM :


def stop():
    if _VARS['stream']:
        _VARS['stream'].stop_stream()
        _VARS['stream'].close()
        _VARS['window']['-PROG-'].update(0)
        _VARS['window']['-PROG1-'].update(0)
        _VARS['window']['-PROG2-'].update(0)
        _VARS['window']['-PROG3-'].update(0)
        _VARS['window']['-PROG4-'].update(0)
        _VARS['window'].FindElement('Stop').Update(disabled=True)
        _VARS['window'].FindElement('Listen').Update(disabled=False)


def callback(in_data, frame_count, time_info, status):
    _VARS['audioData'] = np.frombuffer(in_data, dtype=np.int16)
    _VARS['fftData'] = np.abs(np.fft.rfft(np.frombuffer(in_data, dtype=np.int16))).astype(int)
    '''
    fftTime=np.fft.rfftfreq(CHUNK, 1./RATE)

    b, a = signal.butter(1, 100, 'low', analog=True)
    w, h = signal.freqs(b, a)

    #_VARS['filter_fftData'] = signal.filtfilt(b,a,_VARS['fftData'])
    _VARS['filter_fftData'] = signal.filtfilt(b,a,_VARS['audioData'])

    
    print("audioData: ", _VARS['audioData'])
    print("type audioData: ", type(_VARS['audioData']))
    print("type audioData[0]: ", type(_VARS['audioData'][0]))
    print("len audioData: ", len(_VARS['audioData']))

    print("fftData: ", _VARS['fftData'])
    print("type fftData: ", type(_VARS['fftData']))
    print("type fftData[0]: ", type(_VARS['fftData'][0]))
    print("len fftData: ", len(_VARS['fftData']))

    print("filter_fftData: ", _VARS['filter_fftData'])
    print("type filter_fftData: ", type(_VARS['filter_fftData']))
    print("type filter_fftData[0]: ", type(_VARS['filter_fftData'][0]))
    print("len filter_fftData: ", len(_VARS['filter_fftData']))
    
    print("fftData'][:10]: ", _VARS['fftData'][:10])

    file2write = open("filename.txt", 'a')
    file2write.write(str(_VARS['fftData'][:10]))
    file2write.write("\n")
    file2write.close()

    print("fftData: ", _VARS['fftData'])
    print("len fftData: ", len(_VARS['fftData']))
    print("fftData:[:10] ", _VARS['fftData'][:10])
    print("fftData'][100:300]: ", _VARS['fftData'][100:300])
    print("fftData'][350:512]: ", _VARS['fftData'][350:512])

    print("mean fftData:[:10] ", np.mean(_VARS['fftData'][:10]))
    print("mean fftData'][100:300]: ", np.mean(_VARS['fftData'][100:300]))
    print("mean fftData'][350:512]: ", np.mean(_VARS['fftData'][350:512]))
    '''
    return (in_data, pyaudio.paContinue)


def listen():
    _VARS['window'].FindElement('Stop').Update(disabled=False)
    _VARS['window'].FindElement('Listen').Update(disabled=True)
    _VARS['stream'] = pAud.open(format=pyaudio.paInt16,
                                channels=1,
                                rate=RATE,
                                input=True,
                                frames_per_buffer=CHUNK,
                                stream_callback=callback)
    _VARS['stream'].start_stream()


def updateUI():
    # Uodate volumne meter
    _VARS['window']['-PROG-'].update(np.amax(_VARS['audioData']))
    _VARS['window']['-PROG1-'].update(np.amax(_VARS['fftData']))
    _VARS['window']['-PROG2-'].update(np.amax(_VARS['fftData'][:10]))
    _VARS['window']['-PROG3-'].update(np.mean(_VARS['fftData'][10:170]))
    _VARS['window']['-PROG4-'].update(np.mean(_VARS['fftData'][170:512]))
        
    if np.amax(_VARS['fftData'][:10]) > 10000:
        
        '''not ok
        cosmo_guirlande.pulse_period = 0.15
        cosmo_guirlande.pulse_speed = 0.1
        cosmo_guirlande.color1= 'ORANGE'
        cosmo_guirlande.pulse()'''

        '''ok
        pixels.fill((100, 0, 0, 0))
        pixels.show()
        time.sleep(0.2)
        pixels.fill((0, 0, 0, 0))
        pixels.show()'''

        '''not ok
        pulse = Pulse(pixels, speed=0.1, color=AMBER, period=0.3)
        pulse.animate()'''

        comet = Comet(pixels, speed=0.01, color='ORANGE', tail_length=10, bounce=True)
        animations = AnimationSequence(
            comet,
            advance_interval=5,
            auto_clear=True,
        )
        animations.animate()


    # Redraw plot
    graph.erase()
    drawAxis()
    drawTicks()
    drawAxesLabels()
    drawPlot()


# INIT:
drawAxis()
drawTicks()
drawAxesLabels()

# Configuration des LED
pixels = neopixel.NeoPixel(
    board.D18, 30, brightness=0.99, auto_write=False, pixel_order=neopixel.GRBW
)
print('Press Ctrl-C to quit.')

cosmo_guirlande = Cosmo_guirlande_rpi.Cosmo_guirlande_rpi(pixels, 3, 30, '192.168.0.21', 50003, 1024)

# MAIN LOOP
while True:
    event, values = _VARS['window'].read(timeout=TIMEOUT)
    if event == sg.WIN_CLOSED or event == 'Exit':
        stop()
        pAud.terminate()
        break
    if event == 'Listen':
        listen()
    if event == 'Stop':
        stop()
    elif _VARS['audioData'].size != 0:
        updateUI()


_VARS['window'].close()