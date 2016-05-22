#!/bin/env python
# ####################################### BOOT SEQ, PART 1 - Pre
import datetime

print('Boot sequence part 1 - Pre (%s)' % datetime.datetime.now())
# ############################## Imports
import os
import subprocess
import threading
import time
import json
import sys
from enum import Enum
from enum import unique

# ############################## Definitions
VERSION = '0.1'
SETTINGS_FILE = "/root/www/settings.json"

# Main Menu enum. If setting is None, its a toggle
@unique
class Menu(Enum):
  Exit = {'name': 'Exit', 'setting': None}
  Show_IP = {'name': 'Show IP', 'setting': None}
  Set_Volume = {'name': 'Set Volume', 'setting': ('sound', 'volume')}
  Set_Brightness = {'name': 'Set Brightness', 'setting': ('brightness', 'preference')}

# Days enum.
@unique
class Days(Enum):
  Weekdays = [1, 2, 3, 4, 5]
  Weekends = [6, 7]
  Both = [1, 2, 3, 4, 5, 6, 7]

# Volatile storage
status = {'booting': True, 'network': False, 'skipped': False,
  'draw': {'clock': False, 'option': None}, 'menu': None, 'clock': False,
  'pulsing': False, 'streaming': False, 'gcal': {

  }}
# Permanent storage
settings = {'day': {'enabled': True, 'size': 40},
  'clock': {'format': '%H:%M:%S', 'size': 60},
  'date': {'enabled': True, 'format': '%d-%m-%y', 'size': 36},
  'alarm': {'offset': 60, 'min': 6 * 60, 'max': 12 * 60, 'days': Days.Weekdays,
    'stream': 'MNM Hits'}, 'sound': {'volume': 50, 'min': 15, 'step': 1, 'max': 100},
  'brightness': {'preference': 50, 'now': 100, 'target': 100, 'step': 1, 'min': 15,
    'max': 100}}
# Google Calender API app specific data
gcal = {'client_id': os.getenv('APP_GCAL_ID'),
  'client_secret': os.getenv('APP_GCAL_SECRET'),
  'scope': 'https://www.googleapis.com/auth/calendar.readonly'}
# List of pre-defined streams
streams = {'MNM': 'http://mp3.streampower.be/mnm-high.mp3',
  'MNM Hits': 'http://mp3.streampower.be/mnm_hits-high.mp3',
  'Studio Brussel': 'http://mp3.streampower.be/stubru-high.mp3',
  'Klara': 'http://mp3.streampower.be/klara-high.mp3',
  'Radio 1': 'http://mp3.streampower.be/radio1-high.mp3',
  'Radio 2 Antwerpen': 'http://mp3.streampower.be/ra2ant-high.mp3'}
# Misc globals
music_process = None

if gcal['client_id'] is None or gcal['client_secret'] is None:
  print('APP_GCAL_ID and or APP_GCAL_SECRET not set.')
  sys.exit(1)

# Required for json encoding Enums
class EnumEncoder(json.JSONEncoder):
  def default(self, obj):
    if isinstance(obj, Enum):
      return str(obj)
    return json.JSONEncoder.default(self, obj)

# Send volume to alsa
def set_volume():
  vol = (50 + (settings['sound']['volume'] / 2))
  subprocess.call(['amixer', 'sset', 'PCM,0', '%.0f%%' % vol, '-M'])

# Save settings
def save():
  json.dump(settings, open(SETTINGS_FILE, 'w'), indent=2, cls=EnumEncoder)

# Clamp value between 0 and 100 by default
def clamp(n, minn=0, maxn=100):
  return max(min(maxn, n), minn)

# Go back from "<Class>.<Name>" to actual enum instance
def as_enum(full):
  if full is None:
    return None
  name, member = full.split(".")
  return getattr(globals()[name], member)

def stream_start():
  global music_process
  if music_process is not None:
    return
  stream = streams[settings['alarm']['stream']] if settings['alarm'][
                                                     'stream'] in streams else \
  settings['alarm']['stream']
  status['streaming'] = True
  music_process = subprocess.Popen(['mpg123', '-T', stream], universal_newlines=True,
                                   bufsize=1, stderr=subprocess.PIPE)

  def stream_parser():
    re_title = re.compile(r"ICY-META: StreamTitle='(.*)';")
    while music_process is not None and music_process.poll() is None:
      line = music_process.stderr.readline()
      matcher = re_title.search(line)
      if matcher:
        status['draw']['title'] = matcher.group(1)
    if 'title' in status['draw']:
      del status['draw']['title']

  threading.Thread(target=stream_parser, name='StreamParser', daemon=True).start()

def stream_stop():
  global music_process
  if music_process is None:
    return
  if music_process.poll() is None:
    music_process.terminate()
    music_process.wait()
  status['streaming'] = False
  music_process = None

# ############################## Sequential code
# set pwm pin
# subprocess.call(['gpio', '-g', 'mode', '12', 'pwm'])
# set pwm pin sound
subprocess.call(['gpio_alt', '-p', '13', '-f', '0'])
# Kill any existing ap
subprocess.call(['create_ap', '--stop', 'wlan0'])
# Sometimes the above isn't enough
subprocess.call(['killall', 'hostapd'])

if os.getenv('SDL_FBDEV') is None:
  print('SDL_FBDEV not set.')
  sys.exit(1)

# Write to SDL_FBDEV (normally /dev/fb1)
with open(os.getenv('SDL_FBDEV'), 'wb') as outfile:
  # Raw image data of 'Booting..' centered on the lcd. Made by a little custom C program
  frame = bytearray([0x00] * 44446 + [0xff] * 6 + [0x00] * 632 + [0xff] * 10 + [0x00] * 372 + [ 0xff] * 34 + [0x00] * 224 + [0xff] * 10 + [0x00] * 372 + [0xff] * 40 + [ 0x00] * 158 + [0xff] * 4 + [0x00] * 56 + [0xff] * 10 + [0x00] * 372 + [ 0xff] * 42 + [0x00] * 154 + [0xff] * 6 + [0x00] * 56 + [0xff] * 10 + [ 0x00] * 372 + [0xff] * 44 + [0x00] * 152 + [0xff] * 6 + [0x00] * 58 + [0xff] * 6 + [ 0x00] * 374 + [0xff] * 10 + [0x00] * 22 + [0xff] * 14 + [0x00] * 150 + [ 0xff] * 6 + [0x00] * 438 + [0xff] * 10 + [0x00] * 26 + [0xff] * 10 + [ 0x00] * 150 + [0xff] * 6 + [0x00] * 438 + [0xff] * 10 + [0x00] * 28 + [ 0xff] * 10 + [0x00] * 146 + [0xff] * 8 + [0x00] * 438 + [0xff] * 10 + [ 0x00] * 28 + [0xff] * 10 + [0x00] * 146 + [0xff] * 8 + [0x00] * 438 + [ 0xff] * 10 + [0x00] * 28 + [0xff] * 10 + [0x00] * 138 + [0xff] * 38 + [ 0x00] * 416 + [0xff] * 10 + [0x00] * 28 + [0xff] * 10 + [0x00] * 28 + [ 0xff] * 16 + [0x00] * 44 + [0xff] * 16 + [0x00] * 28 + [0xff] * 44 + [0x00] * 20 + [ 0xff] * 22 + [0x00] * 36 + [0xff] * 8 + [0x00] * 10 + [0xff] * 14 + [0x00] * 42 + [ 0xff] * 32 + [0x00] * 232 + [0xff] * 10 + [0x00] * 28 + [0xff] * 10 + [ 0x00] * 24 + [0xff] * 24 + [0x00] * 36 + [0xff] * 24 + [0x00] * 24 + [0xff] * 44 + [ 0x00] * 20 + [0xff] * 22 + [0x00] * 36 + [0xff] * 8 + [0x00] * 6 + [0xff] * 22 + [ 0x00] * 34 + [0xff] * 36 + [0x00] * 232 + [0xff] * 10 + [0x00] * 28 + [ 0xff] * 10 + [0x00] * 20 + [0xff] * 30 + [0x00] * 30 + [0xff] * 30 + [0x00] * 36 + [ 0xff] * 8 + [0x00] * 42 + [0xff] * 22 + [0x00] * 36 + [0xff] * 8 + [0x00] * 4 + [ 0xff] * 28 + [0x00] * 26 + [0xff] * 40 + [0x00] * 232 + [0xff] * 10 + [ 0x00] * 26 + [0xff] * 10 + [0x00] * 20 + [0xff] * 34 + [0x00] * 26 + [0xff] * 34 + [ 0x00] * 34 + [0xff] * 8 + [0x00] * 56 + [0xff] * 8 + [0x00] * 36 + [0xff] * 8 + [ 0x00] * 2 + [0xff] * 30 + [0x00] * 26 + [0xff] * 12 + [0x00] * 6 + [0xff] * 14 + [ 0x00] * 240 + [0xff] * 10 + [0x00] * 26 + [0xff] * 10 + [0x00] * 20 + [ 0xff] * 10 + [0x00] * 16 + [0xff] * 10 + [0x00] * 24 + [0xff] * 10 + [0x00] * 16 + [ 0xff] * 10 + [0x00] * 32 + [0xff] * 8 + [0x00] * 56 + [0xff] * 8 + [0x00] * 36 + [ 0xff] * 16 + [0x00] * 14 + [0xff] * 12 + [0x00] * 22 + [0xff] * 10 + [0x00] * 14 + [ 0xff] * 10 + [0x00] * 240 + [0xff] * 10 + [0x00] * 22 + [0xff] * 12 + [ 0x00] * 20 + [0xff] * 10 + [0x00] * 20 + [0xff] * 10 + [0x00] * 20 + [0xff] * 10 + [ 0x00] * 20 + [0xff] * 10 + [0x00] * 30 + [0xff] * 8 + [0x00] * 56 + [0xff] * 8 + [ 0x00] * 36 + [0xff] * 14 + [0x00] * 18 + [0xff] * 10 + [0x00] * 22 + [0xff] * 8 + [ 0x00] * 18 + [0xff] * 8 + [0x00] * 240 + [0xff] * 40 + [0x00] * 22 + [0xff] * 10 + [ 0x00] * 24 + [0xff] * 10 + [0x00] * 16 + [0xff] * 10 + [0x00] * 24 + [0xff] * 10 + [ 0x00] * 28 + [0xff] * 8 + [0x00] * 56 + [0xff] * 8 + [0x00] * 36 + [0xff] * 12 + [ 0x00] * 22 + [0xff] * 10 + [0x00] * 18 + [0xff] * 10 + [0x00] * 18 + [0xff] * 10 + [ 0x00] * 238 + [0xff] * 34 + [0x00] * 28 + [0xff] * 10 + [0x00] * 24 + [ 0xff] * 10 + [0x00] * 16 + [0xff] * 10 + [0x00] * 24 + [0xff] * 10 + [0x00] * 28 + [ 0xff] * 8 + [0x00] * 56 + [0xff] * 8 + [0x00] * 36 + [0xff] * 10 + [0x00] * 24 + [ 0xff] * 10 + [0x00] * 18 + [0xff] * 8 + [0x00] * 22 + [0xff] * 8 + [0x00] * 238 + [ 0xff] * 38 + [0x00] * 24 + [0xff] * 8 + [0x00] * 28 + [0xff] * 8 + [0x00] * 16 + [ 0xff] * 8 + [0x00] * 28 + [0xff] * 8 + [0x00] * 28 + [0xff] * 8 + [0x00] * 56 + [ 0xff] * 8 + [0x00] * 36 + [0xff] * 10 + [0x00] * 24 + [0xff] * 10 + [0x00] * 18 + [ 0xff] * 8 + [0x00] * 22 + [0xff] * 8 + [0x00] * 238 + [0xff] * 42 + [0x00] * 18 + [ 0xff] * 10 + [0x00] * 28 + [0xff] * 10 + [0x00] * 12 + [0xff] * 10 + [0x00] * 28 + [ 0xff] * 10 + [0x00] * 26 + [0xff] * 8 + [0x00] * 56 + [0xff] * 8 + [0x00] * 36 + [ 0xff] * 10 + [0x00] * 26 + [0xff] * 8 + [0x00] * 18 + [0xff] * 8 + [0x00] * 22 + [ 0xff] * 8 + [0x00] * 238 + [0xff] * 10 + [0x00] * 22 + [0xff] * 14 + [0x00] * 14 + [ 0xff] * 10 + [0x00] * 28 + [0xff] * 10 + [0x00] * 12 + [0xff] * 10 + [0x00] * 28 + [ 0xff] * 10 + [0x00] * 26 + [0xff] * 8 + [0x00] * 56 + [0xff] * 8 + [0x00] * 36 + [ 0xff] * 10 + [0x00] * 26 + [0xff] * 8 + [0x00] * 18 + [0xff] * 8 + [0x00] * 22 + [ 0xff] * 8 + [0x00] * 238 + [0xff] * 10 + [0x00] * 26 + [0xff] * 12 + [0x00] * 12 + [ 0xff] * 10 + [0x00] * 28 + [0xff] * 10 + [0x00] * 12 + [0xff] * 10 + [0x00] * 28 + [ 0xff] * 10 + [0x00] * 26 + [0xff] * 8 + [0x00] * 56 + [0xff] * 8 + [0x00] * 36 + [ 0xff] * 10 + [0x00] * 26 + [0xff] * 8 + [0x00] * 18 + [0xff] * 10 + [0x00] * 18 + [ 0xff] * 10 + [0x00] * 238 + [0xff] * 10 + [0x00] * 28 + [0xff] * 10 + [ 0x00] * 12 + [0xff] * 10 + [0x00] * 28 + [0xff] * 10 + [0x00] * 12 + [0xff] * 10 + [ 0x00] * 28 + [0xff] * 10 + [0x00] * 26 + [0xff] * 8 + [0x00] * 56 + [0xff] * 8 + [ 0x00] * 36 + [0xff] * 8 + [0x00] * 28 + [0xff] * 8 + [0x00] * 18 + [0xff] * 10 + [ 0x00] * 18 + [0xff] * 10 + [0x00] * 238 + [0xff] * 10 + [0x00] * 30 + [ 0xff] * 10 + [0x00] * 10 + [0xff] * 10 + [0x00] * 28 + [0xff] * 10 + [0x00] * 12 + [ 0xff] * 10 + [0x00] * 28 + [0xff] * 10 + [0x00] * 26 + [0xff] * 8 + [0x00] * 56 + [ 0xff] * 8 + [0x00] * 36 + [0xff] * 8 + [0x00] * 28 + [0xff] * 8 + [0x00] * 20 + [ 0xff] * 10 + [0x00] * 14 + [0xff] * 10 + [0x00] * 240 + [0xff] * 10 + [ 0x00] * 30 + [0xff] * 10 + [0x00] * 10 + [0xff] * 10 + [0x00] * 28 + [0xff] * 10 + [ 0x00] * 12 + [0xff] * 10 + [0x00] * 28 + [0xff] * 10 + [0x00] * 26 + [0xff] * 8 + [ 0x00] * 56 + [0xff] * 8 + [0x00] * 36 + [0xff] * 8 + [0x00] * 28 + [0xff] * 8 + [ 0x00] * 20 + [0xff] * 12 + [0x00] * 10 + [0xff] * 10 + [0x00] * 242 + [ 0xff] * 10 + [0x00] * 30 + [0xff] * 10 + [0x00] * 10 + [0xff] * 10 + [0x00] * 28 + [ 0xff] * 10 + [0x00] * 12 + [0xff] * 10 + [0x00] * 28 + [0xff] * 10 + [0x00] * 26 + [ 0xff] * 8 + [0x00] * 56 + [0xff] * 8 + [0x00] * 36 + [0xff] * 8 + [0x00] * 28 + [ 0xff] * 8 + [0x00] * 22 + [0xff] * 30 + [0x00] * 242 + [0xff] * 10 + [0x00] * 30 + [ 0xff] * 10 + [0x00] * 10 + [0xff] * 10 + [0x00] * 28 + [0xff] * 10 + [0x00] * 12 + [ 0xff] * 10 + [0x00] * 28 + [0xff] * 10 + [0x00] * 26 + [0xff] * 8 + [0x00] * 56 + [ 0xff] * 8 + [0x00] * 36 + [0xff] * 8 + [0x00] * 28 + [0xff] * 8 + [0x00] * 24 + [ 0xff] * 24 + [0x00] * 246 + [0xff] * 10 + [0x00] * 30 + [0xff] * 10 + [ 0x00] * 10 + [0xff] * 10 + [0x00] * 28 + [0xff] * 10 + [0x00] * 12 + [0xff] * 10 + [ 0x00] * 28 + [0xff] * 10 + [0x00] * 26 + [0xff] * 8 + [0x00] * 56 + [0xff] * 8 + [ 0x00] * 36 + [0xff] * 8 + [0x00] * 28 + [0xff] * 8 + [0x00] * 26 + [0xff] * 18 + [ 0x00] * 250 + [0xff] * 10 + [0x00] * 30 + [0xff] * 10 + [0x00] * 12 + [0xff] * 8 + [ 0x00] * 28 + [0xff] * 8 + [0x00] * 16 + [0xff] * 8 + [0x00] * 28 + [0xff] * 8 + [ 0x00] * 28 + [0xff] * 8 + [0x00] * 56 + [0xff] * 8 + [0x00] * 36 + [0xff] * 8 + [ 0x00] * 28 + [0xff] * 8 + [0x00] * 22 + [0xff] * 8 + [0x00] * 264 + [0xff] * 10 + [ 0x00] * 30 + [0xff] * 10 + [0x00] * 12 + [0xff] * 10 + [0x00] * 24 + [0xff] * 10 + [ 0x00] * 16 + [0xff] * 10 + [0x00] * 24 + [0xff] * 10 + [0x00] * 28 + [0xff] * 10 + [ 0x00] * 54 + [0xff] * 8 + [0x00] * 36 + [0xff] * 8 + [0x00] * 28 + [0xff] * 8 + [ 0x00] * 22 + [0xff] * 6 + [0x00] * 266 + [0xff] * 10 + [0x00] * 28 + [0xff] * 10 + [ 0x00] * 14 + [0xff] * 10 + [0x00] * 24 + [0xff] * 10 + [0x00] * 16 + [0xff] * 10 + [ 0x00] * 24 + [0xff] * 10 + [0x00] * 28 + [0xff] * 10 + [0x00] * 54 + [0xff] * 8 + [ 0x00] * 36 + [0xff] * 8 + [0x00] * 28 + [0xff] * 8 + [0x00] * 20 + [0xff] * 8 + [ 0x00] * 64 + [0xff] * 8 + [0x00] * 52 + [0xff] * 8 + [0x00] * 52 + [0xff] * 8 + [ 0x00] * 74 + [0xff] * 10 + [0x00] * 26 + [0xff] * 12 + [0x00] * 16 + [0xff] * 10 + [ 0x00] * 20 + [0xff] * 10 + [0x00] * 20 + [0xff] * 10 + [0x00] * 20 + [0xff] * 10 + [ 0x00] * 32 + [0xff] * 10 + [0x00] * 52 + [0xff] * 8 + [0x00] * 36 + [0xff] * 8 + [ 0x00] * 28 + [0xff] * 8 + [0x00] * 20 + [0xff] * 8 + [0x00] * 64 + [0xff] * 10 + [ 0x00] * 50 + [0xff] * 10 + [0x00] * 50 + [0xff] * 10 + [0x00] * 72 + [0xff] * 10 + [ 0x00] * 22 + [0xff] * 14 + [0x00] * 20 + [0xff] * 10 + [0x00] * 16 + [0xff] * 10 + [ 0x00] * 24 + [0xff] * 10 + [0x00] * 16 + [0xff] * 10 + [0x00] * 34 + [0xff] * 28 + [ 0x00] * 34 + [0xff] * 8 + [0x00] * 36 + [0xff] * 8 + [0x00] * 28 + [0xff] * 8 + [ 0x00] * 20 + [0xff] * 10 + [0x00] * 60 + [0xff] * 14 + [0x00] * 46 + [0xff] * 14 + [ 0x00] * 46 + [0xff] * 14 + [0x00] * 70 + [0xff] * 46 + [0x00] * 22 + [0xff] * 34 + [ 0x00] * 26 + [0xff] * 34 + [0x00] * 36 + [0xff] * 26 + [0x00] * 34 + [0xff] * 8 + [ 0x00] * 36 + [0xff] * 8 + [0x00] * 28 + [0xff] * 8 + [0x00] * 20 + [0xff] * 32 + [ 0x00] * 38 + [0xff] * 14 + [0x00] * 46 + [0xff] * 14 + [0x00] * 46 + [0xff] * 14 + [ 0x00] * 70 + [0xff] * 42 + [0x00] * 28 + [0xff] * 30 + [0x00] * 30 + [0xff] * 30 + [ 0x00] * 40 + [0xff] * 24 + [0x00] * 18 + [0xff] * 42 + [0x00] * 18 + [0xff] * 8 + [ 0x00] * 28 + [0xff] * 8 + [0x00] * 22 + [0xff] * 34 + [0x00] * 34 + [0xff] * 14 + [ 0x00] * 46 + [0xff] * 14 + [0x00] * 46 + [0xff] * 14 + [0x00] * 70 + [0xff] * 40 + [ 0x00] * 32 + [0xff] * 24 + [0x00] * 36 + [0xff] * 24 + [0x00] * 48 + [0xff] * 18 + [ 0x00] * 20 + [0xff] * 42 + [0x00] * 18 + [0xff] * 8 + [0x00] * 28 + [0xff] * 8 + [ 0x00] * 24 + [0xff] * 34 + [0x00] * 32 + [0xff] * 14 + [0x00] * 46 + [0xff] * 14 + [ 0x00] * 46 + [0xff] * 14 + [0x00] * 70 + [0xff] * 34 + [0x00] * 42 + [0xff] * 16 + [ 0x00] * 44 + [0xff] * 16 + [0x00] * 90 + [0xff] * 42 + [0x00] * 18 + [0xff] * 8 + [ 0x00] * 28 + [0xff] * 8 + [0x00] * 20 + [0xff] * 40 + [0x00] * 32 + [0xff] * 10 + [ 0x00] * 50 + [0xff] * 10 + [0x00] * 50 + [0xff] * 10 + [0x00] * 434 + [ 0xff] * 10 + [0x00] * 24 + [0xff] * 12 + [0x00] * 30 + [0xff] * 10 + [0x00] * 50 + [ 0xff] * 10 + [0x00] * 50 + [0xff] * 10 + [0x00] * 434 + [0xff] * 8 + [0x00] * 28 + [ 0xff] * 10 + [0x00] * 592 + [0xff] * 10 + [0x00] * 30 + [0xff] * 8 + [ 0x00] * 592 + [0xff] * 8 + [0x00] * 32 + [0xff] * 8 + [0x00] * 592 + [0xff] * 8 + [ 0x00] * 32 + [0xff] * 8 + [0x00] * 592 + [0xff] * 8 + [0x00] * 30 + [0xff] * 10 + [ 0x00] * 592 + [0xff] * 10 + [0x00] * 26 + [0xff] * 10 + [0x00] * 596 + [ 0xff] * 10 + [0x00] * 22 + [0xff] * 12 + [0x00] * 596 + [0xff] * 18 + [0x00] * 2 + [ 0xff] * 22 + [0x00] * 600 + [0xff] * 38 + [0x00] * 604 + [0xff] * 32 + [ 0x00] * 614 + [0xff] * 20 + [0x00] * 77662)
  outfile.write(frame)
  outfile.close()

# ####################################### BOOT SEQ, PART 2 - GPIO
print('Boot sequence part 2 - GPIO (%s)' % datetime.datetime.now())
# ############################## Imports
# noinspection PyUnresolvedReferences
import RPi.GPIO as GPIO

# ############################## Definitions
RE_A = 16
RE_B = 5
RE_S = 6
ALARM_S = 27
PWM_BG = 12

# Set PWM of LCD background LED via gpio program because the GPIO python module
def set_brightness(percent=100):
  p.ChangeDutyCycle(percent)
  # subprocess.call(['gpio', '-g', 'pwm', '12', '%.0f' % (clamp(percent) * 10.23)])

# While booting, ramp up the LCD backlight from 0 to 100% over 2 seconds
def pre_boot_pwm():
  i = 0
  while status['booting'] and i < 100:
    set_brightness(i)
    time.sleep(0.2)
    i += 1
  set_brightness(100)

# 'Interrupt' handler of alarm button
def int_btn_alarm(chan):
  print('BTN: ALARM')
  if 'alarm' in status and not status['skipped']:
    ts_alarm = status['alarm'].replace(second=0, microsecond=0).timestamp()
    ts_now = datetime.datetime.now().replace(second=0, microsecond=0).timestamp()
    if int(ts_alarm - ts_now) < 600:
      status['skipped'] = True
      if 'alarm' in status['draw']:
        del status['draw']['alarm']
      if status['streaming']:
        stream_stop()
        del status['alarm']
        next_event()
      return
  if status['streaming']:
    stream_stop()
  else:
    stream_start()

# 'Interrupt' handler button of rot encoder
def int_btn_ok(chan):
  print('BTN: OK')
  if not status['draw']['clock']:
    return
  if status['menu']:
    status['draw']['option'] = None if status['menu'] == Menu.Exit else status['menu']
    status['menu'] = None
  elif status['draw']['option']:
    status['draw']['option'] = None
    save()
  else:
    status['menu'] = Menu.Show_IP

# 'Interrupt' handler for A of rotary encoder
def int_rot(chan):
  a = GPIO.input(RE_A)
  # Since A triggers on falling edge, it should be 0, if not, debounce
  if a:
    return
  # To get the direction, pull B
  b = GPIO.input(RE_B)
  print('Rotate: %s' % ('Right,+' if b else 'Left,-'))
  # If we are in menu, go left or right
  if status['menu']:
    items = list(Menu)
    i = items.index(status['menu'])
    status['menu'] = items[(i + (1 if b else -1)) % len(items)]
  # If we are doing a setting
  elif status['draw']['option']:
    if status['draw']['option'].value['setting']:
      setting = status['draw']['option'].value['setting']
      current = settings
      # Go down the the sencond to last object and property name, so it can be set
      for key in setting[:-1]:
        current = current[key]
      current[setting[-1]] = clamp(current[setting[-1]] + (1 if b else -1))
      set_volume()

# ############################## Sequential code
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup([RE_A, RE_B, RE_S, ALARM_S], GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(PWM_BG, GPIO.OUT)
p = GPIO.PWM(PWM_BG, 250)
p.start(0)
GPIO.add_event_detect(RE_A, GPIO.FALLING, callback=int_rot, bouncetime=25)
GPIO.add_event_detect(RE_S, GPIO.FALLING, callback=int_btn_ok, bouncetime=500)
GPIO.add_event_detect(ALARM_S, GPIO.FALLING, callback=int_btn_alarm, bouncetime=500)
# Start the preboot LCD backlight ramp up
threading.Thread(target=pre_boot_pwm, name='PreBootPWM', daemon=True).start()

# ####################################### BOOT SEQ, PART 3 - Pygame
print('Boot sequence part 3 - Pygame (%s)' % datetime.datetime.now())
# ############################## Imports
# noinspection PyUnresolvedReferences
import pygame
import requests
import socket
import re
import urllib
import sched
import dateutil.parser
import signal
# ############################## Definitions

# Required to avoid pygame.display.init hanging on a second boot
def signal_handler(signal, frame):
  print('EXIT: SIGTERM or SIGINT (%s)' % datetime.datetime.now())
  time.sleep(1)
  pygame.quit()
  p.stop()
  # last, because its possible it may throw up, if GPIO hasn't imported yet. That is
  # fine, if it happens after pygame.quit
  GPIO.cleanup()
  sys.exit(0)

# ############################## Sequential code
# Handle kill command
signal.signal(signal.SIGTERM, signal_handler)
# Handle Control-C
signal.signal(signal.SIGINT, signal_handler)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

print('Init pygame... (%s)' % datetime.datetime.now())
# This call takes a while, it can also hang if pygame wasn't quited last time,
# hence the kill/^C handling
pygame.display.init()
# Instead of initing all pygame subsystems, we only do display and font to cut the
# loading time by a lot
pygame.font.init()
pygame.mouse.set_visible(False)

# Monospace fonts
FONT_XL = pygame.font.SysFont('notomono', 60)
FONT_L = pygame.font.SysFont('notomono', 36)
FONT_M = pygame.font.SysFont('notomono', 26)
FONT_S = pygame.font.SysFont('notomono', 15)
FONT_ICO = pygame.font.SysFont('fontawesome', 15)

# Screen size
SIZE = (pygame.display.Info().current_w, pygame.display.Info().current_h)
# Screen surface
SCREEN = pygame.display.set_mode(SIZE, pygame.FULLSCREEN)
# Clear screen
SCREEN.fill(BLACK)
print('Done init pygame & clear ... (%s)' % datetime.datetime.now())

if os.path.isfile(SETTINGS_FILE):
  try:
    settings.update(json.load(open(SETTINGS_FILE)))
    settings['alarm']['days'] = as_enum(settings['alarm']['days'])
    set_volume()
  except json.decoder.JSONDecodeError:
    print('Config file unreadable, lets just throw it away and start fresh')
else:
  save()

# ####################################### BOOT SEQ, PART 4 - Scheduler
print('Boot sequence part 4 - Scheduler (%s)' % datetime.datetime.now())
# ############################## Definitions

# Draw text on screen, below other height, in font & color, centered by default
def draw_text(message, font=FONT_S, color=WHITE, height=0, center=True):
  # if height is 0, assume the screen needs clearing
  if height == 0:
    SCREEN.fill(BLACK)
  # Render the text on a new surface
  text = font.render(message, False, color)
  x = 0
  # Center the text
  if center:
    x = (SCREEN.get_width() - text.get_width()) / 2
  # Draw the text surface on the screen
  SCREEN.blit(text, (x, height))
  # 'Commit' the changes
  pygame.display.update()
  # Return the new height
  return height + text.get_height()

# Special message display, used for 'fatal crashes'
def error(message):
  SCREEN.fill(BLACK)
  height = draw_text('SmartAlarmClock (%s)' % VERSION, FONT_M)
  height = draw_text('Fatal Error', color=RED, height=height)
  draw_text(message, height=height)
  # Goodbye cruel world. We can't exit because it would clear the screen.
  while True:
    time.sleep(1)

# Task to periodically update the IP to be displayed
def task_update_ip():
  threadLocal.ip = socket.gethostbyname(socket.gethostname())
  CLOCK.enter(10, 10, task_update_ip)

# To make the font objects updatable, but not waste resources
def task_update_font():
  threadLocal.font_day = pygame.font.SysFont('notomono', settings['day']['size'])
  threadLocal.font_clock = pygame.font.SysFont('notomono', settings['clock']['size'])
  threadLocal.date_clock = pygame.font.SysFont('notomono', settings['date']['size'])

# Task to do the background brightness, handles pulsing effect if required
def task_update_pwm():
  if status['streaming']:
    set_brightness(100)
  else:
    bgt = settings['brightness']
    bgt['target'] = clamp(bgt['target'], bgt['min'], bgt['max'])
    # If we are drawing the brightness slider, give instant feedback
    if status['draw']['option'] == Menu.Set_Brightness:
      set_brightness(bgt['preference'])
    # If not drawing the brightness slider
    else:
      # If we are not at target level brightness
      if bgt['target'] != bgt['now']:
        # Deviate predetermined step size from the current brightness towards the

        if bgt['target'] < bgt['now']:
          bgt['now'] = max(bgt['target'], bgt['now'] - bgt['step'], bgt['min'], 0)
        else:
          bgt['now'] = min(bgt['target'], bgt['now'] + bgt['step'], bgt['max'], 100)
        set_brightness(bgt['now'])
      # if we are at target brightness
      else:
        # if pulsing
        if status['pulsing']:
          if bgt['target'] <= bgt['min']:
            bgt['target'] = bgt['max']
          else:
            bgt['target'] = bgt['min']
        # if not pulsing
        else:
          bgt['target'] = bgt['preference']
  CLOCK.enter(0.1, 2, task_update_pwm)

def truncate_scroll_text(string, length=30):
  if len(string) <= length:
    return string
  td = int(datetime.datetime.now().timestamp() * 2) % (len(string) - length + 1)
  return string[td:td + length]

# Task that draws to the LCD
def task_draw_clock():
  # To make adding code easy, leftover/unnecessary height assignments are left!
  height = 0
  # draw the main clock
  if status['draw']['clock']:
    if settings['day']['enabled']:
      height = draw_text(datetime.datetime.now().strftime('%A'), height=height,
                         font=threadLocal.font_day)
      height -= (threadLocal.font_day.get_height() * 0.1)
    height = draw_text(datetime.datetime.now().strftime(settings['clock']['format']),
                       height=height, font=threadLocal.font_clock)
    height -= (threadLocal.font_clock.get_height() * 0.1)
    if settings['date']['enabled']:
      height = draw_text(datetime.datetime.now().strftime(settings['date']['format']),
                         height=height, font=threadLocal.date_clock)
  # if we need to register the devie with gcal
  if 'user_code' in status['gcal']:
    height = draw_text(status['gcal']['verification_url'], height=height, font=FONT_S)
    height = draw_text('Code: ' + status['gcal']['user_code'], height=height, font=FONT_S)
  # If the menu needs drawing
  if status['menu']:
    height = draw_text('Menu', height=height, font=FONT_S)
    height = draw_text(status['menu'].value['name'], height=height, font=FONT_S)
  # if we have a menu option selected
  elif status['draw']['option']:
    if status['draw']['option'] == Menu.Show_IP:
      height = draw_text(threadLocal.ip, height=height, font=FONT_S)
    # If the option is tied to a setting
    elif status['draw']['option'].value['setting']:
      setting = status['draw']['option'].value['setting']
      current = settings
      # Move down the list of keys: ('foo', 'bar') => settings['foo']['bar]
      for key in setting:
        current = current[key]
      height = draw_text(status['draw']['option'].value['name'] + ': %d%%' % current,
                         height=height, font=FONT_S)
      # Draw the rectangle below the text and % value
      pygame.draw.rect(SCREEN, WHITE, (0, height, SIZE[0] * (current / 100), 5))
      # Need to move 5 px down manually
      height += 5
  else:
    if 'alarm' in status['draw']:
      draw_text('\uf0a1', height=height, font=FONT_ICO, center=False)
      height = draw_text(status['draw']['alarm'], height=height, font=FONT_S)
    if 'next' in status['draw']:
      draw_text('\uf133', height=height, font=FONT_ICO, center=False)
      height = draw_text(truncate_scroll_text(status['draw']['next']), height=height,
                         font=FONT_S)
    if 'title' in status['draw']:
      draw_text('\uf001', height=height, font=FONT_ICO, center=False)
      height = draw_text(truncate_scroll_text(status['draw']['title']), height=height,
                         font=FONT_S)
  # Actually commit the LCD
  pygame.display.update()
  CLOCK.enter(0.5, 1, task_draw_clock)

def task_check_gcal():
  print('Checking gcal (%s)' % datetime.datetime.now())
  gcal_get_events()
  CLOCK.enter(60 * 30, 2, task_check_gcal)

# Helper method, to run the task once manually before passing it off to the scheduler
def run_clock_thread():
  # We are now out of booting
  status['booting'] = False
  task_update_font()
  task_update_ip()
  task_update_pwm()
  task_draw_clock()
  task_check_gcal()
  task_alarm_check()
  CLOCK.run()

def task_alarm_check():
  if 'alarm' in status:
    print('Alarm poll')
    ts_alarm = status['alarm'].replace(second=0, microsecond=0).timestamp()
    ts_now = datetime.datetime.now().replace(second=0, microsecond=0).timestamp()
    if int(ts_alarm - ts_now) == 600:
      print('10 minute mark')
      status['pulsing'] = True
    if int(ts_alarm - ts_now) == 0:
      print('alarm time')
      if status['skipped']:
        status['skipped'] = False
        del status['alarm']
        next_event()
      else:
        stream_start()
      if 'alarm' in status['draw']:
        del status['draw']['alarm']
  CLOCK.enter(30, 1, task_alarm_check)

# Try to connect to the wifi network set via settings['wifiProfile']
def attempt_connect(height=0):
  # Just to be sure

  subprocess.call(['killall', 'hostapd'])
  subprocess.call(['create_ap', '--stop', 'wlan0'])
  height = draw_text('Connecting to %s' % settings['wifiProfile'], height=height)
  # Use switch to make sure no other network is using wlan0
  if subprocess.call(['netctl', 'switch-to', settings['wifiProfile']]) == 0:
    # Congratulations, we have liftoff
    status['network'] = True
    # Draw the IP in screen to make accessing the web interface easy
    ip = socket.gethostbyname(socket.gethostname())
    height = draw_text(ip, height=height, font=FONT_M)
    height = draw_text('Syncing time & date', height=height)
    # Use NTP to get internet time
    subprocess.call(['systemctl', 'restart', 'ntpd'])
    # Make sure we actually have NTP time
    if subprocess.call(['ntp-wait', '-n', '5']) != 0:
      error('NTP sync failed.')
    else:
      # Write to RTC
      subprocess.call(['hwclock', '-w'])
      # Now we can start rendering the clock
      status['draw']['clock'] = True
  # Connecting to wifi failed
  else:
    height = draw_text('Failed...', height=height)
    status['network'] = False
  return height

# Refresh our token
def gcal_refresh():
  if not status['network'] or 'refresh_token' not in settings['gcal']:
    return
  out = json.loads(requests.post('https://www.googleapis.com/oauth2/v4/token',
                                 data={'refresh_token': settings['gcal']['refresh_token'],
                                   'client_id': gcal['client_id'],
                                   'client_secret': gcal['client_secret'],
                                   'grant_type': 'refresh_token'}).text)
  status['gcal'] = out
  if 'expires_in' in out:
    status['gcal']['expires'] = datetime.datetime.now() + \
                                datetime.timedelta(seconds=out['expires_in'] - 10)

# Poll with device token to see if user has granted us permission yet
def gcal_poll():
  out = json.loads(requests.post('https://www.googleapis.com/oauth2/v4/token',
                                 data={'client_id': gcal['client_id'],
                                   'client_secret': gcal['client_secret'],
                                   'code': status['gcal']['device_code'],
                                   'grant_type':
                                         'http://oauth.net/grant_type/device/1.0'}).text)
  # Some information, 'authorization_pending' is normal
  if "error" in out:
    print(out['error'])
  # No error = good
  else:
    status['gcal'] = out
    # 10 sec for safety
    status['gcal']['expires'] = datetime.datetime.now() + \
                                datetime.timedelta(seconds=out['expires_in'] - 10)
    # Store the token, and make the primary calendar default
    settings['gcal'] = {'refresh_token': out['refresh_token'], 'calendar_id': 'primary'}
    # Save the new settings
    save()
    # Fetch the upcoming events
    gcal_get_events()
    # to prevent re-registering
    return

  # if the token request is expired, drop it
  if datetime.datetime.now() > status['gcal']['expires']:
    print('Token request expired. (%s)' % datetime.datetime.now())
    status['gcal'] = {}
  # Poll at the rate requested by Google
  else:
    CLOCK.enter(status['gcal']['interval'], 3, gcal_poll)

# Do a new token request, overrides all old gcal data, except for appointments
def gcal_request_token():
  out = json.loads(requests.post('https://accounts.google.com/o/oauth2/device/code',
                                 data={'client_id': gcal['client_id'],
                                   'scope': gcal['scope']}).text)
  status['gcal'] = {}
  status['gcal']['device_code'] = out['device_code']
  status['gcal']['interval'] = out['interval']
  status['gcal']['user_code'] = out['user_code']
  status['gcal']['verification_url'] = out['verification_url']
  # 10 sec for safety
  status['gcal']['expires'] = datetime.datetime.now() + \
                              datetime.timedelta(seconds=out['expires_in'] - 10)
  if 'gcal' in settings:
    del settings['gcal']
    save()
  CLOCK.enter(out['interval'], 3, gcal_poll)

# Pull in new events, if token is expired / missing it will request a new one.
def gcal_get_events():
  if not status['network'] or 'gcal' not in settings:
    return
  if 'calendar_id' not in status['gcal'] or \
          datetime.datetime.now() > status['gcal']['expires']:
    gcal_refresh()
  if 'access_token' not in status['gcal']:
    # Something exploded.
    return
  out = json.loads(requests.get(
    'https://www.googleapis.com/calendar/v3/calendars/%s/events' % settings['gcal'][
      'calendar_id'], headers={
      'Authorization': status['gcal']['token_type'] + ' ' + status['gcal'][
        'access_token']}, params={
      'timeMin': datetime.datetime.now(datetime.timezone.utc).astimezone().isoformat('T'),
      'timeMax': (datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(
        days=7)).astimezone().isoformat('T'), 'singleEvents': True,
      'orderBy': 'startTime'}).text)
  if 'items' not in out:
    print('No items in response gcal_get_events')
    print(out)
    status['items'] = None
    return False
  status['items'] = out['items']
  next_event()

def next_event():
  for item in status['items']:
    alarm = dateutil.parser.parse(item['start']['dateTime'])
    status['draw']['next'] = item['summary'] + ' ' + \
                  dateutil.parser.parse(item['start']['dateTime']).strftime('%a at %H:%M')
    if alarm.isoweekday() not in settings['alarm']['days'].value:
      print('Event not in target days, skipping. %s' % item['summary'])
      continue
    alarm -= datetime.timedelta(minutes=settings['alarm']['offset'])
    if settings['alarm']['min'] != -1 and \
                (alarm.hour * 60) + alarm.minute < settings['alarm']['min']:
      alarm = alarm.replace(hour=settings['alarm']['min'] // 60,
                            minute=settings['alarm']['min'] % 60)
    if settings['alarm']['max'] != -1 and \
                (alarm.hour * 60) + alarm.minute > settings['alarm']['max']:
      alarm = alarm.replace(hour=settings['alarm']['max'] // 60,
                            minute=settings['alarm']['max'] % 60)
    if alarm.timestamp() < datetime.datetime.now().timestamp():
      print('Alarm time passed, skipping. %s' % item['summary'])
      continue
    status['alarm'] = alarm
    status['draw']['alarm'] = alarm.strftime('%a at %H:%M')
    return
    # Only get here if no (correct) items

  if 'alarm' in status:
    del status['alarm']
  if 'alarm' in status['draw']:
    del status['draw']['alarm']

# ############################## Sequential code
# Network adapter not plugged in => panic
if not os.path.exists('/sys/class/net/wlan0'):
  error('No wifi interface')

# For the IP & fonts
threadLocal = threading.local()
# Make the scheguler
CLOCK = sched.scheduler(time.time, time.sleep)
# Start the 'main' thread
threading.Thread(target=run_clock_thread, name='ClockThread', daemon=True).start()
# Draw name & version
h = draw_text('SmartClock (%s)' % VERSION, font=FONT_M)

# If we have a wifi network saved, try to connect
if 'wifiProfile' in settings and settings['wifiProfile'] != '':
  h = attempt_connect(h)

# if we have connected
if status['network']:
  if 'gcal' in settings:
    # if we have some gcal stuff saved, update the event list
    gcal_get_events()
  else:
    # Start the token procedure
    gcal_request_token()
# If we don't have network
else:
  # Pull in the clock/date from the RTC, if it got reset, it'll be at 1 jan 2000
  subprocess.call(['hwclock', '-s'])
  h = draw_text('Starting AP', height=h)
  subprocess.call(['create_ap', '-n', '--daemon', '--redirect-to-localhost', 'wlan0',
                   'SmartAlarmClock'])
  # Give the adapter some time
  time.sleep(5)
  h = draw_text('Connect to wifi network for setup:', height=h)
  h = draw_text('SmartAlarmClock', height=h, font=FONT_M)
  h = draw_text('And browse to:', height=h)
  # Display IP
  h = draw_text(socket.gethostbyname(socket.gethostname()), height=h, font=FONT_M)

# ####################################### BOOT SEQ, PART 5 - Flask
print('Boot sequence part 5 - Flask (%s)' % datetime.datetime.now())
# ############################## Imports
from flask import Flask
from flask import json
from flask import Response
from flask import request
from flask import url_for
# ############################## Definitions
app = Flask(__name__)

# List of possible access points
@app.route('/')
def api():
  output = []
  for rule in app.url_map.iter_rules():
    options = {}
    for arg in rule.arguments:
      options[arg] = '[%s]' % arg
    output.append({'name': rule.endpoint, 'methods': ','.join(rule.methods),
                   'url': '/api' + urllib.parse.unquote(
                     url_for(rule.endpoint, **options))})
  return Response(json.dumps(output, cls=EnumEncoder), mimetype='text/javascript')

# Get the list of wifi networks OR set the wifi profile settings (ssid & pass) (via POST)
@app.route('/wifi', methods=['GET', 'POST'])
def api_wifi():
  # Set wifi settings by making a profile file for it, so we can (ab)use netctl
  if request.method == 'POST':
    # stop drawing the clock for a second
    status['draw']['clock'] = False
    text = "Description='Automatically generated profile by python'\n"
    text += 'Interface=wlan0\n'
    text += 'Connection=wireless\n'
    text += 'IP=dhcp\n'
    text += "ESSID='%s'\n" % request.form['ssid']
    if 'pass' in request.form and request.form['pass'] != '':
      text += "Security=wpa\nKey='%s'" % request.form['pass']
    else:
      text += 'Security=none'
    settings['wifiProfile'] = 'GEN-wlan0-%s' % request.form['ssid']
    # Write the file
    f = open('/etc/netctl/%s' % settings['wifiProfile'], 'w')
    f.write(text)
    f.close()
    save()
    attempt_connect()
    if 'gcal' in settings:
      # if we have some gcal stuff saved, update the event list
      gcal_get_events()
    else:
      # Start the token procedure
      gcal_request_token()
    # Return a readable value
    if status['network']:
      return 'OK'
    return 'ERROR'
  # GET
  else:
    # Regex yey
    re_cell = re.compile(r'Cell \d+')
    re_mac = re.compile(r'Address: (?P<Address>.*)')
    re_ssid = re.compile(r'ESSID:"(?P<SSID>.*)"')
    re_quality = re.compile(r'Quality=(?P<Quality>\d+)/100')
    re_signal = re.compile(r'Signal level=(?P<SignalLevel>\d+)/100')
    re_encrypted = re.compile(r'Encryption key:(?P<Protected>on|off)')
    re_encryption = re.compile(r'IE: (?P<Protection>.*)')
    re_authentication = re.compile(
      r'Authentication Suites \(1\) : (?P<Authentication>.*)')
    proc = subprocess.Popen(['iwlist', 'wlan0', 'scan'], stdout=subprocess.PIPE,
                            universal_newlines=True)
    out, err = proc.communicate()
    # data array
    data = []
    # Used to remeber the last object we are working on
    cell = None
    for line in out.split('\n'):
      # strip whitespace
      line = line.strip()
      matcher = re_cell.search(line)
      # if this is the start of a new network
      if matcher:
        # if cell wasn't None, add it to the data list
        if cell:
          data.append(cell)
        cell = {}
      for regex in [re_mac, re_ssid, re_quality, re_signal, re_encrypted, re_encryption,
                    re_authentication]:
        matcher = regex.search(line)
        # if this regex matched
        if matcher:
          # add the match to the list of properties in the dict
          cell.update(matcher.groupdict())
    return Response(json.dumps(data, cls=EnumEncoder), mimetype='text/javascript')

# GET: Dump the settings POST: Set settings
@app.route('/settings', methods=['GET', 'POST'])
def api_settings():
  if request.method == 'GET':
    return Response(json.dumps(settings, cls=EnumEncoder), mimetype='text/javascript')
  else:
    settings.update(request.get_json())
    settings['alarm']['days'] = as_enum(settings['alarm']['days'])
    CLOCK.enter(0, 1, task_update_font)
    set_volume()
    next_event()
    save()
    return 'OK'

# Reset (and restart) the gcal linking process
@app.route('/pollgcal', methods=['POST'])
def api_pollgcal():
  gcal_get_events()
  return 'OK'

# Reset (and restart) the gcal linking process
@app.route('/resetgcal', methods=['POST'])
def api_resetgcal():
  gcal_request_token()
  return 'OK'

# GET: Dump the status POST: Set status
@app.route('/status', methods=['GET', 'POST'])
def api_status():
  if request.method == 'GET':
    return Response(json.dumps(status, cls=EnumEncoder), mimetype='text/javascript')
  else:
    status.update(request.get_json())
    status['draw']['option'] = as_enum(status['draw']['option'])
    status['menu'] = as_enum(status['menu'])
    save()
    return 'OK'

# ############################## Sequential code
print('Starting webserver... (%s)' % datetime.datetime.now())
# Blocking call!
app.run(host='127.0.0.1', port=5000, use_reloader=False)

print('EXIT: Flask died (%s)' % datetime.datetime.now())
pygame.quit()
GPIO.cleanup()
