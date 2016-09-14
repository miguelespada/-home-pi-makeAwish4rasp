import sys
import time
import os
import audioop
import pysimpledmx
from serial.tools import list_ports

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def clear():
  os.system('cls' if os.name == 'nt' else 'clear')


def printChannels(ch1, map1, ch2, map2):
  sys.stdout.write("Channel 1:%05d -->  \033[92m%03d\033[0m \t Channel 2: %05d --> \033[92m%03d\033[0m\r" % (ch1, map1, ch2, map2) )
  sys.stdout.flush()

com = ""
for coms in list_ports.comports():
  if "SNR=EN" in coms[2]:
    com = coms
    break

if com == "":
  exit(0)

mydmx = pysimpledmx.DMXConnection(com[0])

import pyaudio

p = pyaudio.PyAudio()
devinfo = p.get_device_info_by_index(2)

clear()

print "Openning DMX ", com[2]
print "Selected device is ",devinfo.get('name')


def record_audio():
  CHUNK = 1024 * 4
  FORMAT = pyaudio.paInt16
  CHANNELS = 2
  RATE = 44100
  RECORD_SECONDS = 5
  WAVE_OUTPUT_FILENAME = "apt.wav"

  p = pyaudio.PyAudio()

  stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                input_device_index=2,
                frames_per_buffer=CHUNK)


  frames = []

  while True:
    try:
      data = stream.read(CHUNK)
      rms_1 = audioop.rms(audioop.tomono(data, 2, 1, 0), 2)
      rms_2 = audioop.rms(audioop.tomono(data, 2, 0, 1), 2) 
      map_1 = int(255 * rms_1 / 30000.)
      map_2 = int(255 * rms_2 / 30000.)
      printChannels(rms_1, map_1, rms_2, map_2)

      mydmx.setChannel(1, map_1, autorender=True)
      mydmx.setChannel(2, map_2, autorender=True)
    except Exception as e:
      print e



  print "* done\n" 

  stream.stop_stream()
  stream.close()
  p.terminate()


record_audio()