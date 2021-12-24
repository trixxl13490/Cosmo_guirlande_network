import PySimpleGUI as sg
import pyaudio
import numpy as np
from scipy import signal

""" RealTime Audio Waveform plot """

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
          [sg.ProgressBar(400000, orientation='h',
                          size=(20, 20), key='-PROG2-')],
          [sg.ProgressBar(400000, orientation='h',
                          size=(20, 20), key='-PROG3-')],
          [sg.ProgressBar(400000, orientation='h',
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
    step = 100/CHUNK
    gain = 1

    # MIN MAX Scaled :
    # mn, mx = np.min(_VARS['audioData']), np.max(_VARS['audioData'])
    # x_scaled = ((_VARS['audioData'] - mn) / (mx - mn))*100

    # Scaled/Centered for display (change to suit signal):
    #x_scaled = ((_VARS['audioData']/100)*gain)+50
    x_scaled = _VARS['fftData']
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
    '''
    #print("fftData: ", _VARS['fftData'])
    print("len fftData: ", len(_VARS['fftData']))
    print("fftData:[:10] ", _VARS['fftData'][:10])
    print("fftData'][100:300]: ", _VARS['fftData'][100:300])
    print("fftData'][350:512]: ", _VARS['fftData'][350:512])

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
    _VARS['window']['-PROG3-'].update(np.amax(_VARS['fftData'][100:300]))
    _VARS['window']['-PROG4-'].update(np.amax(_VARS['fftData'][350:512]))
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

