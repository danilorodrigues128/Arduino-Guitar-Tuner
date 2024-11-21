import serial
import numpy as np
import threading
from scipy.fft import fft
import math
import os
import sys

SERIAL_PORT = "COM1" # Default COM Port
EXEC_PERIOD = 500    # [us]
BUFFER_SIZE = 16384  # samples

if len(sys.argv) > 1:
    SERIAL_PORT = str(sys.argv[1]).upper()

NOTES_ARRAY = [
    " C2",
    "C#2",
    " D2",
    "D#2",
    " E2",
    " F2",
    "F#2",
    " G2",
    "G#2",
    " A2",
    "A#2",
    " B2",
    " C3",
    "C#3",
    " D3",
    "D#3",
    " E3",
    " F3",
    "F#3",
    " G3",
    "G#3",
    " A3",
    "A#3",
    " B3",
    " C4",
    "C#4",
    " D4",
    "D#4",
    " E4",
    " F4",
    "F#4",
    " G4",
    "G#4",
    " A4",
    "A#4",
    " B4"
]

try:
    ser = serial.Serial(port=SERIAL_PORT, baudrate=115200)
except:
    print("Invalid Serial Port ("+SERIAL_PORT+")")
    exit(0)

soundBuffer = np.zeros((BUFFER_SIZE,))
soundFlag = False

SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")

def getNote():
    threading.Timer(0.5, getNote).start()

    global soundFlag

    freq_step = (0.5/(EXEC_PERIOD*1e-6))/(BUFFER_SIZE/2)
    main_freq = freq_step*np.argmax(np.split(np.abs(fft(soundBuffer)),2)[0][10:])

    if main_freq < 60 or main_freq > 500:
        soundFlag = False
    
    main_freq = np.clip(main_freq, 65.406, 493.880)

    note_id = 12*math.log2(main_freq/65.406)
    currentNote = NOTES_ARRAY[round(note_id)]
    
    printTuner(currentNote, note_id-round(note_id))

def printTuner(note, shift):
    n_blackDots = math.floor(10*(shift+0.5)) if soundFlag else 0
    n_whiteDots = 10 - n_blackDots

    dotsLabel = n_blackDots * "●" + n_whiteDots * "○"
    noteLabel = note[0:2] + note[-1].translate(SUB) if soundFlag else " ♪ "

    tunerLabel = dotsLabel[:5] + " |" + noteLabel + "| " + dotsLabel[-5:]

    if soundFlag:
        color = "\033[91m" if n_blackDots != 5 else "\033[92m"
    else:
        color = ""


    print(17*" " + color + tunerLabel + "\033[0m", end="\r")

os.system("cls")
print("SEM0142 - Sensores e Sistemas de Medidas | Grupo 03")
print(13*" "+"Trabalho Final - Afinador\n")
getNote()

while True:
    try:
        sound = int(ser.readline())
    except:
        continue

    soundBuffer = np.roll(soundBuffer, -1)
    soundBuffer[-1] = sound

    if np.any(soundBuffer[-150:] > 450.0):
        soundFlag = True
    else:
        soundFlag = False