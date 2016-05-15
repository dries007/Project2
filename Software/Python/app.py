#!/bin/env python
# ####################################### BOOT SEQ, PART 1 - Pre
import datetime
print('Boot sequence part 1 - Pre (%s)' % datetime.datetime.now())
# ############################## Imports
import os
import subprocess
import threading
import time

# ############################## Definitions
status = {
    'booting': True,
    'network': False,
    'draw': {
        'clock': False,
        'option': None
    },
    'menu': None,
    'clock': False,
    'pulsing': False
}
settings = {
    'day': {
        'format': '%A',
        'size': 40
    },
    'clock': {
        'format': '%H:%M:%S',
        'size': 60
    },
    'date': {
        'format': '%Y-%m-%d',
        'size': 36
    },
    'sound': {
        'volume': .50
    },
    'brightness': {
        'preference': 0.5,
        'now': 1,
        'target': 1,
        'step': 0.01,
        'min': 0.15,
        'max': 1
    }
}


def clamp(n, minn=0, maxn=1):
    return max(min(maxn, n), minn)


def set_brightness(percent=1):
    subprocess.call(['gpio', '-g', 'pwm', '12', '%.0f' % (clamp(percent) * 1023)])


def pre_boot_pwm():
    i = 0
    while status['booting'] and i < 1024:
        subprocess.call(['gpio', '-g', 'pwm', '12', str(i)])
        time.sleep(0.1)
        i += 1
    subprocess.call(['gpio', '-g', 'pwm', '12', '1023'])

# ############################## Sequential code
subprocess.call(['gpio', '-g', 'mode', '12', 'pwm'])  # set pwm pin
set_brightness(0)
subprocess.call(['create_ap', '--stop', 'wlan0'])  # Kill any existing ap
subprocess.call(['killall', 'hostapd'])  # Sometimes the above isn't enough

with open(os.getenv('SDL_FBDEV'), 'wb') as outfile:
    # Raw image data of 'Booting..' centered on the 320 x 240 lcd. Made by a little custom C program
    frame = bytearray([0x00] * 44446 + [0xff] * 6 + [0x00] * 632 + [0xff] * 10 + [0x00] * 372 + [0xff] * 34 + [0x00] * 224 + [0xff] * 10 + [0x00] * 372 + [0xff] * 40 + [0x00] * 158 + [0xff] * 4 + [0x00] * 56 + [0xff] * 10 + [0x00] * 372 + [0xff] * 42 + [0x00] * 154 + [0xff] * 6 + [0x00] * 56 + [0xff] * 10 + [0x00] * 372 + [0xff] * 44 + [0x00] * 152 + [0xff] * 6 + [0x00] * 58 + [0xff] * 6 + [0x00] * 374 + [0xff] * 10 + [0x00] * 22 + [0xff] * 14 + [0x00] * 150 + [0xff] * 6 + [0x00] * 438 + [0xff] * 10 + [0x00] * 26 + [0xff] * 10 + [0x00] * 150 + [0xff] * 6 + [0x00] * 438 + [0xff] * 10 + [0x00] * 28 + [0xff] * 10 + [0x00] * 146 + [0xff] * 8 + [0x00] * 438 + [0xff] * 10 + [0x00] * 28 + [0xff] * 10 + [0x00] * 146 + [0xff] * 8 + [0x00] * 438 + [0xff] * 10 + [0x00] * 28 + [0xff] * 10 + [0x00] * 138 + [0xff] * 38 + [0x00] * 416 + [0xff] * 10 + [0x00] * 28 + [0xff] * 10 + [0x00] * 28 + [0xff] * 16 + [0x00] * 44 + [0xff] * 16 + [0x00] * 28 + [0xff] * 44 + [0x00] * 20 + [0xff] * 22 + [0x00] * 36 + [0xff] * 8 + [0x00] * 10 + [0xff] * 14 + [0x00] * 42 + [0xff] * 32 + [0x00] * 232 + [0xff] * 10 + [0x00] * 28 + [0xff] * 10 + [0x00] * 24 + [0xff] * 24 + [0x00] * 36 + [0xff] * 24 + [0x00] * 24 + [0xff] * 44 + [0x00] * 20 + [0xff] * 22 + [0x00] * 36 + [0xff] * 8 + [0x00] * 6 + [0xff] * 22 + [0x00] * 34 + [0xff] * 36 + [0x00] * 232 + [0xff] * 10 + [0x00] * 28 + [0xff] * 10 + [0x00] * 20 + [0xff] * 30 + [0x00] * 30 + [0xff] * 30 + [0x00] * 36 + [0xff] * 8 + [0x00] * 42 + [0xff] * 22 + [0x00] * 36 + [0xff] * 8 + [0x00] * 4 + [0xff] * 28 + [0x00] * 26 + [0xff] * 40 + [0x00] * 232 + [0xff] * 10 + [0x00] * 26 + [0xff] * 10 + [0x00] * 20 + [0xff] * 34 + [0x00] * 26 + [0xff] * 34 + [0x00] * 34 + [0xff] * 8 + [0x00] * 56 + [0xff] * 8 + [0x00] * 36 + [0xff] * 8 + [0x00] * 2 + [0xff] * 30 + [0x00] * 26 + [0xff] * 12 + [0x00] * 6 + [0xff] * 14 + [0x00] * 240 + [0xff] * 10 + [0x00] * 26 + [0xff] * 10 + [0x00] * 20 + [0xff] * 10 + [0x00] * 16 + [0xff] * 10 + [0x00] * 24 + [0xff] * 10 + [0x00] * 16 + [0xff] * 10 + [0x00] * 32 + [0xff] * 8 + [0x00] * 56 + [0xff] * 8 + [0x00] * 36 + [0xff] * 16 + [0x00] * 14 + [0xff] * 12 + [0x00] * 22 + [0xff] * 10 + [0x00] * 14 + [0xff] * 10 + [0x00] * 240 + [0xff] * 10 + [0x00] * 22 + [0xff] * 12 + [0x00] * 20 + [0xff] * 10 + [0x00] * 20 + [0xff] * 10 + [0x00] * 20 + [0xff] * 10 + [0x00] * 20 + [0xff] * 10 + [0x00] * 30 + [0xff] * 8 + [0x00] * 56 + [0xff] * 8 + [0x00] * 36 + [0xff] * 14 + [0x00] * 18 + [0xff] * 10 + [0x00] * 22 + [0xff] * 8 + [0x00] * 18 + [0xff] * 8 + [0x00] * 240 + [0xff] * 40 + [0x00] * 22 + [0xff] * 10 + [0x00] * 24 + [0xff] * 10 + [0x00] * 16 + [0xff] * 10 + [0x00] * 24 + [0xff] * 10 + [0x00] * 28 + [0xff] * 8 + [0x00] * 56 + [0xff] * 8 + [0x00] * 36 + [0xff] * 12 + [0x00] * 22 + [0xff] * 10 + [0x00] * 18 + [0xff] * 10 + [0x00] * 18 + [0xff] * 10 + [0x00] * 238 + [0xff] * 34 + [0x00] * 28 + [0xff] * 10 + [0x00] * 24 + [0xff] * 10 + [0x00] * 16 + [0xff] * 10 + [0x00] * 24 + [0xff] * 10 + [0x00] * 28 + [0xff] * 8 + [0x00] * 56 + [0xff] * 8 + [0x00] * 36 + [0xff] * 10 + [0x00] * 24 + [0xff] * 10 + [0x00] * 18 + [0xff] * 8 + [0x00] * 22 + [0xff] * 8 + [0x00] * 238 + [0xff] * 38 + [0x00] * 24 + [0xff] * 8 + [0x00] * 28 + [0xff] * 8 + [0x00] * 16 + [0xff] * 8 + [0x00] * 28 + [0xff] * 8 + [0x00] * 28 + [0xff] * 8 + [0x00] * 56 + [0xff] * 8 + [0x00] * 36 + [0xff] * 10 + [0x00] * 24 + [0xff] * 10 + [0x00] * 18 + [0xff] * 8 + [0x00] * 22 + [0xff] * 8 + [0x00] * 238 + [0xff] * 42 + [0x00] * 18 + [0xff] * 10 + [0x00] * 28 + [0xff] * 10 + [0x00] * 12 + [0xff] * 10 + [0x00] * 28 + [0xff] * 10 + [0x00] * 26 + [0xff] * 8 + [0x00] * 56 + [0xff] * 8 + [0x00] * 36 + [0xff] * 10 + [0x00] * 26 + [0xff] * 8 + [0x00] * 18 + [0xff] * 8 + [0x00] * 22 + [0xff] * 8 + [0x00] * 238 + [0xff] * 10 + [0x00] * 22 + [0xff] * 14 + [0x00] * 14 + [0xff] * 10 + [0x00] * 28 + [0xff] * 10 + [0x00] * 12 + [0xff] * 10 + [0x00] * 28 + [0xff] * 10 + [0x00] * 26 + [0xff] * 8 + [0x00] * 56 + [0xff] * 8 + [0x00] * 36 + [0xff] * 10 + [0x00] * 26 + [0xff] * 8 + [0x00] * 18 + [0xff] * 8 + [0x00] * 22 + [0xff] * 8 + [0x00] * 238 + [0xff] * 10 + [0x00] * 26 + [0xff] * 12 + [0x00] * 12 + [0xff] * 10 + [0x00] * 28 + [0xff] * 10 + [0x00] * 12 + [0xff] * 10 + [0x00] * 28 + [0xff] * 10 + [0x00] * 26 + [0xff] * 8 + [0x00] * 56 + [0xff] * 8 + [0x00] * 36 + [0xff] * 10 + [0x00] * 26 + [0xff] * 8 + [0x00] * 18 + [0xff] * 10 + [0x00] * 18 + [0xff] * 10 + [0x00] * 238 + [0xff] * 10 + [0x00] * 28 + [0xff] * 10 + [0x00] * 12 + [0xff] * 10 + [0x00] * 28 + [0xff] * 10 + [0x00] * 12 + [0xff] * 10 + [0x00] * 28 + [0xff] * 10 + [0x00] * 26 + [0xff] * 8 + [0x00] * 56 + [0xff] * 8 + [0x00] * 36 + [0xff] * 8 + [0x00] * 28 + [0xff] * 8 + [0x00] * 18 + [0xff] * 10 + [0x00] * 18 + [0xff] * 10 + [0x00] * 238 + [0xff] * 10 + [0x00] * 30 + [0xff] * 10 + [0x00] * 10 + [0xff] * 10 + [0x00] * 28 + [0xff] * 10 + [0x00] * 12 + [0xff] * 10 + [0x00] * 28 + [0xff] * 10 + [0x00] * 26 + [0xff] * 8 + [0x00] * 56 + [0xff] * 8 + [0x00] * 36 + [0xff] * 8 + [0x00] * 28 + [0xff] * 8 + [0x00] * 20 + [0xff] * 10 + [0x00] * 14 + [0xff] * 10 + [0x00] * 240 + [0xff] * 10 + [0x00] * 30 + [0xff] * 10 + [0x00] * 10 + [0xff] * 10 + [0x00] * 28 + [0xff] * 10 + [0x00] * 12 + [0xff] * 10 + [0x00] * 28 + [0xff] * 10 + [0x00] * 26 + [0xff] * 8 + [0x00] * 56 + [0xff] * 8 + [0x00] * 36 + [0xff] * 8 + [0x00] * 28 + [0xff] * 8 + [0x00] * 20 + [0xff] * 12 + [0x00] * 10 + [0xff] * 10 + [0x00] * 242 + [0xff] * 10 + [0x00] * 30 + [0xff] * 10 + [0x00] * 10 + [0xff] * 10 + [0x00] * 28 + [0xff] * 10 + [0x00] * 12 + [0xff] * 10 + [0x00] * 28 + [0xff] * 10 + [0x00] * 26 + [0xff] * 8 + [0x00] * 56 + [0xff] * 8 + [0x00] * 36 + [0xff] * 8 + [0x00] * 28 + [0xff] * 8 + [0x00] * 22 + [0xff] * 30 + [0x00] * 242 + [0xff] * 10 + [0x00] * 30 + [0xff] * 10 + [0x00] * 10 + [0xff] * 10 + [0x00] * 28 + [0xff] * 10 + [0x00] * 12 + [0xff] * 10 + [0x00] * 28 + [0xff] * 10 + [0x00] * 26 + [0xff] * 8 + [0x00] * 56 + [0xff] * 8 + [0x00] * 36 + [0xff] * 8 + [0x00] * 28 + [0xff] * 8 + [0x00] * 24 + [0xff] * 24 + [0x00] * 246 + [0xff] * 10 + [0x00] * 30 + [0xff] * 10 + [0x00] * 10 + [0xff] * 10 + [0x00] * 28 + [0xff] * 10 + [0x00] * 12 + [0xff] * 10 + [0x00] * 28 + [0xff] * 10 + [0x00] * 26 + [0xff] * 8 + [0x00] * 56 + [0xff] * 8 + [0x00] * 36 + [0xff] * 8 + [0x00] * 28 + [0xff] * 8 + [0x00] * 26 + [0xff] * 18 + [0x00] * 250 + [0xff] * 10 + [0x00] * 30 + [0xff] * 10 + [0x00] * 12 + [0xff] * 8 + [0x00] * 28 + [0xff] * 8 + [0x00] * 16 + [0xff] * 8 + [0x00] * 28 + [0xff] * 8 + [0x00] * 28 + [0xff] * 8 + [0x00] * 56 + [0xff] * 8 + [0x00] * 36 + [0xff] * 8 + [0x00] * 28 + [0xff] * 8 + [0x00] * 22 + [0xff] * 8 + [0x00] * 264 + [0xff] * 10 + [0x00] * 30 + [0xff] * 10 + [0x00] * 12 + [0xff] * 10 + [0x00] * 24 + [0xff] * 10 + [0x00] * 16 + [0xff] * 10 + [0x00] * 24 + [0xff] * 10 + [0x00] * 28 + [0xff] * 10 + [0x00] * 54 + [0xff] * 8 + [0x00] * 36 + [0xff] * 8 + [0x00] * 28 + [0xff] * 8 + [0x00] * 22 + [0xff] * 6 + [0x00] * 266 + [0xff] * 10 + [0x00] * 28 + [0xff] * 10 + [0x00] * 14 + [0xff] * 10 + [0x00] * 24 + [0xff] * 10 + [0x00] * 16 + [0xff] * 10 + [0x00] * 24 + [0xff] * 10 + [0x00] * 28 + [0xff] * 10 + [0x00] * 54 + [0xff] * 8 + [0x00] * 36 + [0xff] * 8 + [0x00] * 28 + [0xff] * 8 + [0x00] * 20 + [0xff] * 8 + [0x00] * 64 + [0xff] * 8 + [0x00] * 52 + [0xff] * 8 + [0x00] * 52 + [0xff] * 8 + [0x00] * 74 + [0xff] * 10 + [0x00] * 26 + [0xff] * 12 + [0x00] * 16 + [0xff] * 10 + [0x00] * 20 + [0xff] * 10 + [0x00] * 20 + [0xff] * 10 + [0x00] * 20 + [0xff] * 10 + [0x00] * 32 + [0xff] * 10 + [0x00] * 52 + [0xff] * 8 + [0x00] * 36 + [0xff] * 8 + [0x00] * 28 + [0xff] * 8 + [0x00] * 20 + [0xff] * 8 + [0x00] * 64 + [0xff] * 10 + [0x00] * 50 + [0xff] * 10 + [0x00] * 50 + [0xff] * 10 + [0x00] * 72 + [0xff] * 10 + [0x00] * 22 + [0xff] * 14 + [0x00] * 20 + [0xff] * 10 + [0x00] * 16 + [0xff] * 10 + [0x00] * 24 + [0xff] * 10 + [0x00] * 16 + [0xff] * 10 + [0x00] * 34 + [0xff] * 28 + [0x00] * 34 + [0xff] * 8 + [0x00] * 36 + [0xff] * 8 + [0x00] * 28 + [0xff] * 8 + [0x00] * 20 + [0xff] * 10 + [0x00] * 60 + [0xff] * 14 + [0x00] * 46 + [0xff] * 14 + [0x00] * 46 + [0xff] * 14 + [0x00] * 70 + [0xff] * 46 + [0x00] * 22 + [0xff] * 34 + [0x00] * 26 + [0xff] * 34 + [0x00] * 36 + [0xff] * 26 + [0x00] * 34 + [0xff] * 8 + [0x00] * 36 + [0xff] * 8 + [0x00] * 28 + [0xff] * 8 + [0x00] * 20 + [0xff] * 32 + [0x00] * 38 + [0xff] * 14 + [0x00] * 46 + [0xff] * 14 + [0x00] * 46 + [0xff] * 14 + [0x00] * 70 + [0xff] * 42 + [0x00] * 28 + [0xff] * 30 + [0x00] * 30 + [0xff] * 30 + [0x00] * 40 + [0xff] * 24 + [0x00] * 18 + [0xff] * 42 + [0x00] * 18 + [0xff] * 8 + [0x00] * 28 + [0xff] * 8 + [0x00] * 22 + [0xff] * 34 + [0x00] * 34 + [0xff] * 14 + [0x00] * 46 + [0xff] * 14 + [0x00] * 46 + [0xff] * 14 + [0x00] * 70 + [0xff] * 40 + [0x00] * 32 + [0xff] * 24 + [0x00] * 36 + [0xff] * 24 + [0x00] * 48 + [0xff] * 18 + [0x00] * 20 + [0xff] * 42 + [0x00] * 18 + [0xff] * 8 + [0x00] * 28 + [0xff] * 8 + [0x00] * 24 + [0xff] * 34 + [0x00] * 32 + [0xff] * 14 + [0x00] * 46 + [0xff] * 14 + [0x00] * 46 + [0xff] * 14 + [0x00] * 70 + [0xff] * 34 + [0x00] * 42 + [0xff] * 16 + [0x00] * 44 + [0xff] * 16 + [0x00] * 90 + [0xff] * 42 + [0x00] * 18 + [0xff] * 8 + [0x00] * 28 + [0xff] * 8 + [0x00] * 20 + [0xff] * 40 + [0x00] * 32 + [0xff] * 10 + [0x00] * 50 + [0xff] * 10 + [0x00] * 50 + [0xff] * 10 + [0x00] * 434 + [0xff] * 10 + [0x00] * 24 + [0xff] * 12 + [0x00] * 30 + [0xff] * 10 + [0x00] * 50 + [0xff] * 10 + [0x00] * 50 + [0xff] * 10 + [0x00] * 434 + [0xff] * 8 + [0x00] * 28 + [0xff] * 10 + [0x00] * 592 + [0xff] * 10 + [0x00] * 30 + [0xff] * 8 + [0x00] * 592 + [0xff] * 8 + [0x00] * 32 + [0xff] * 8 + [0x00] * 592 + [0xff] * 8 + [0x00] * 32 + [0xff] * 8 + [0x00] * 592 + [0xff] * 8 + [0x00] * 30 + [0xff] * 10 + [0x00] * 592 + [0xff] * 10 + [0x00] * 26 + [0xff] * 10 + [0x00] * 596 + [0xff] * 10 + [0x00] * 22 + [0xff] * 12 + [0x00] * 596 + [0xff] * 18 + [0x00] * 2 + [0xff] * 22 + [0x00] * 600 + [0xff] * 38 + [0x00] * 604 + [0xff] * 32 + [0x00] * 614 + [0xff] * 20 + [0x00] * 77662)
    outfile.write(frame)
    outfile.close()

if os.path.exists('/sys/class/net/wlan1'):  # todo: remove (also remove the profile!)
    print('Debug wifi connection (%s)' % datetime.datetime.now())
    subprocess.call(['netctl', 'start', 'wlan1-Kennes'])
    print('Connected to Kennes on wlan1 (%s)' % datetime.datetime.now())

threading.Thread(target=pre_boot_pwm, name='PreBootPWM', daemon=True).start()

# ####################################### BOOT SEQ, PART 2 - Pygame
print('Boot sequence part 2 - Pygame (%s)' % datetime.datetime.now())
# ############################## Imports
# noinspection PyUnresolvedReferences
import pygame
import socket
import json
import re
import urllib
import sched
import sys
import signal

from enum import Enum
from enum import unique

# ############################## Definitions


def save():  # save settings
    json.dump(settings, open(SETTINGS_FILE, 'w'))


def signal_handler(signal, frame):  # Required to avoid pygame.display.init hanging on a second boot
    print('EXIT: SIGTERM or SIGINT (%s)' % datetime.datetime.now())
    time.sleep(1)
    pygame.quit()
    GPIO.cleanup()  # last, because its possible it may throw up, if GPIO hasn't imported yet. That is fine, if it happens after pygame.quit
    sys.exit(0)


@unique
class Menu(Enum):  # Main Menu enum. If setting is None, its a toggle
    Exit = {'name': 'Exit', 'setting': None}
    Show_IP = {'name': 'Show IP', 'setting': None}
    Set_Volume = {'name': 'Set Volume', 'setting': ('sound', 'volume')}
    Set_Brightness = {'name': 'Set Brightness', 'setting': ('brightness', 'preference')}

# ############################## Sequential code
signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)

VERSION = '0.1'
SETTINGS_FILE = "/root/www/settings.json"

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
RE_A = 16
RE_B = 5
RE_S = 6

print('Init pygame... (%s)' % datetime.datetime.now())
pygame.display.init()
pygame.font.init()
pygame.mouse.set_visible(False)

FONT_XL = pygame.font.SysFont('notomono', 60)
FONT_L = pygame.font.SysFont('notomono', 36)
FONT_M = pygame.font.SysFont('notomono', 26)
FONT_S = pygame.font.SysFont('notomono', 15)

SIZE = (pygame.display.Info().current_w, pygame.display.Info().current_h)
SCREEN = pygame.display.set_mode(SIZE, pygame.FULLSCREEN)
SCREEN.fill(BLACK)
print('Done init pygame & clear ... (%s)' % datetime.datetime.now())

if os.path.isfile(SETTINGS_FILE):
    settings = json.load(open(SETTINGS_FILE))

FONT_DAY = pygame.font.SysFont('notomono', settings['day']['size'])
FONT_CLOCK = pygame.font.SysFont('notomono', settings['clock']['size'])
FONT_DATE = pygame.font.SysFont('notomono', settings['date']['size'])

# ####################################### BOOT SEQ, PART 3 - Scheduler
print('Boot sequence part 3 - Scheduler (%s)' % datetime.datetime.now())
# ############################## Definitions


def draw_text(message, font=FONT_S, color=WHITE, height=0, center=True):
    if height == 0:
        SCREEN.fill(BLACK)
    text = font.render(message, False, color)
    x = 0
    if center:
        x = (SCREEN.get_width() - text.get_width()) / 2
    SCREEN.blit(text, (x, height))
    pygame.display.update()
    return height + text.get_height()


def error(message):
    SCREEN.fill(BLACK)
    height = draw_text('SmartClock (%s)' % VERSION, FONT_M)
    height = draw_text('Fatal Error', color=RED, height=height)
    draw_text(message, height=height)
    while True:  # Goodbye cruel world. We can't exit because it would clear the screen.
        time.sleep(1)


def task_update_ip():
    threadLocal.ip = socket.gethostbyname(socket.gethostname())
    CLOCK.enter(10, 3, task_update_ip)


def task_update_pwm():
    bgt = settings['brightness']
    if status['draw']['option'] == Menu.Set_Brightness:
        subprocess.call(['gpio', '-g', 'pwm', '12', '%.0f' % (bgt['preference'] * 1023)])
    else:
        if bgt['target'] != bgt['now']:
            if bgt['target'] < bgt['now']:
                bgt['now'] = max(bgt['target'], bgt['now'] - bgt['step'], bgt['min'], 0)
            else:
                bgt['now'] = min(bgt['target'], bgt['now'] + bgt['step'], bgt['max'], 1)
            subprocess.call(['gpio', '-g', 'pwm', '12', '%.0f' % (bgt['now'] * 1023)])
        else:
            if status['pulsing']:
                if bgt['target'] <= bgt['min']:
                    bgt['target'] = bgt['max']
                else:
                    bgt['target'] = bgt['min']
            else:
                bgt['target'] = bgt['preference']
    CLOCK.enter(0.1, 2, task_update_pwm)


def task_draw_clock():
    height = 0
    if status['draw']['clock']:
        height = draw_text(datetime.datetime.now().strftime(settings['day']['format']), height=height, font=FONT_DAY)
        height = draw_text(datetime.datetime.now().strftime(settings['clock']['format']), height=height, font=FONT_CLOCK)
        height = draw_text(datetime.datetime.now().strftime(settings['date']['format']), height=height, font=FONT_DATE)
    if status['menu']:
        height = draw_text("Menu", height=height, font=FONT_S)
        height = draw_text(status['menu'].value['name'], height=height, font=FONT_S)
    if status['draw']['option'] == Menu.Show_IP:
        height = draw_text(threadLocal.ip, height=height, font=FONT_S)
    elif status['draw']['option'] == Menu.Set_Volume:
        height = draw_text('Volume: %.0f%%' % (100 * settings['sound']['volume']), height=height, font=FONT_S)
        pygame.draw.rect(SCREEN, WHITE, (0, height, SIZE[0] * settings['sound']['volume'], 5))
        height += 5
    elif status['draw']['option'] == Menu.Set_Brightness:
        height = draw_text('Brightness preference: %.0f%%' % (100 * settings['brightness']['preference']), height=height, font=FONT_S)
        pygame.draw.rect(SCREEN, WHITE, (0, height, SIZE[0] * settings['brightness']['preference'], 5))
        height += 5
    pygame.display.update()
    CLOCK.enter(0.1, 1, task_draw_clock)


def run_clock_thread():
    threadLocal.ip = socket.gethostbyname(socket.gethostname())
    task_update_ip()
    task_update_pwm()
    task_draw_clock()
    CLOCK.run()


def attempt_connect(height=0):
    # Just to be sure
    subprocess.call(['killall', 'hostapd'])
    subprocess.call(['create_ap', '--stop', 'wlan0'])
    height = draw_text('Connecting to %s' % settings['wifiProfile'], height=height)
    if subprocess.call(['netctl', 'switch-to', settings['wifiProfile']]) == 0:
        status['network'] = True
        height = draw_text(socket.gethostbyname(socket.gethostname()), height=height, font=FONT_M)
        height = draw_text('Syncing time & date', height=height)
        subprocess.call(['systemctl', 'restart', 'ntpd'])
        if subprocess.call(['ntp-wait', '-n', '5']) != 0:
            error('NTP sync failed.')
        else:
            subprocess.call(['hwclock', '-w'])
            status['draw']['clock'] = True
    else:
        height = draw_text('Failed...', height=height)
    return height

# ############################## Sequential code
if not os.path.exists('/sys/class/net/wlan0'):
    error('No wifi interface')

threadLocal = threading.local()
CLOCK = sched.scheduler(time.time, time.sleep)
status['booting'] = False
threading.Thread(target=run_clock_thread, name='ClockThread', daemon=True).start()
h = draw_text('SmartClock (%s)' % VERSION, font=FONT_M)

if 'wifiProfile' in settings and settings['wifiProfile'] != '':
    h = attempt_connect(h)

if not status['network']:
    subprocess.call(['hwclock', '-s'])
    h = draw_text('Starting AP', height=h)
    subprocess.call(['create_ap', '-n', '--daemon', '--redirect-to-localhost', 'wlan0', 'SmartAlarmClock'])
    time.sleep(5)
    h = draw_text('Connect to wifi network for setup:', height=h)
    h = draw_text('SmartAlarmClock', height=h, font=FONT_M)
    h = draw_text('And browse to:', height=h)
    h = draw_text(socket.gethostbyname(socket.gethostname()), height=h, font=FONT_M)


# ####################################### BOOT SEQ, PART 4 - GPIO
print('Boot sequence part 4 - GPIO (%s)' % datetime.datetime.now())
# ############################## Imports
# noinspection PyUnresolvedReferences
import RPi.GPIO as GPIO
# ############################## Definitions


def int_btn_ok(chan):
    print('BTN: OK')
    if not status['draw']['clock']:
        return
    if status['menu']:
        status['draw']['option'] = None if status['menu'] == Menu.Exit else status['menu']
        status['menu'] = None
    elif status['draw']['option']:
        status['draw']['option'] = None
    else:
        status['menu'] = Menu.Show_IP


def int_rot(chan):
    a = GPIO.input(RE_A)
    if a:
        return
    b = GPIO.input(RE_B)
    print('Rotate: %s' % ('Right,+' if b else 'Left,-'))
    if status['menu']:
        items = list(Menu)
        i = items.index(status['menu'])
        status['menu'] = items[(i + (1 if b else -1)) % len(items)]
    elif status['draw']['option']:
        if status['draw']['option'].value['setting']:
            setting = status['draw']['option'].value['setting']
            current = settings
            for key in setting[:-1]:
                current = current[key]
            current[setting[-1]] = clamp(current[setting[-1]] + (0.01 if b else -0.01))
            save()

# ############################## Sequential code
GPIO.setmode(GPIO.BCM)
GPIO.setup([RE_A, RE_B, RE_S], GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(RE_A, GPIO.FALLING, callback=int_rot, bouncetime=25)
GPIO.add_event_detect(RE_S, GPIO.FALLING, callback=int_btn_ok, bouncetime=200)

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


@app.route('/')
def api():
    output = []
    for rule in app.url_map.iter_rules():
        options = {}
        for arg in rule.arguments:
            options[arg] = '[%s]' % arg
        output.append({'name': rule.endpoint, 'methods': ','.join(rule.methods), 'url': urllib.parse.unquote(url_for(rule.endpoint, **options))})
    return Response(json.dumps(output), mimetype='text/javascript')


@app.route('/wifi', methods=['GET', 'POST'])
def api_wifi():
    if request.method == 'POST':
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
        f = open('/etc/netctl/%s' % settings['wifiProfile'], 'w')
        f.write(text)
        f.close()
        save()
        attempt_connect()
        if status['network']:
            return 'OK'
        return 'ERROR'
    else:
        re_cell = re.compile(r'Cell \d+')
        re_mac = re.compile(r'Address: (?P<Address>.*)')
        re_ssid = re.compile(r'ESSID:"(?P<SSID>.*)"')
        re_quality = re.compile(r'Quality=(?P<Quality>\d+)/100')
        re_signal = re.compile(r'Signal level=(?P<SignalLevel>\d+)/100')
        re_encrypted = re.compile(r'Encryption key:(?P<Protected>on|off)')
        re_encryption = re.compile(r'IE: (?P<Protection>.*)')
        re_authentication = re.compile(r'Authentication Suites \(1\) : (?P<Authentication>.*)')

        proc = subprocess.Popen(['iwlist', 'wlan0', 'scan'], stdout=subprocess.PIPE, universal_newlines=True)
        out, err = proc.communicate()

        data = []
        cell = None
        for line in out.split('\n'):
            line = line.strip()
            matcher = re_cell.search(line)
            if matcher:
                if cell:
                    data.append(cell)
                cell = {}
            for regex in [re_mac, re_ssid, re_quality, re_signal, re_encrypted, re_encryption, re_authentication]:
                matcher = regex.search(line)
                if matcher:
                    cell.update(matcher.groupdict())
        return Response(json.dumps(data), mimetype='text/javascript')


@app.route('/settings')
def api_settings():
    return Response(json.dumps(settings), mimetype='text/javascript')


@app.route('/status')
def api_status():
    return Response(json.dumps(status), mimetype='text/javascript')

# ############################## Sequential code
print('Starting webserver... (%s)' % datetime.datetime.now())
app.run(host='0.0.0.0', port=5000, debug=True, use_debugger=True, use_reloader=False)  # Blocking call! todo: disable debug!


print('EXIT: Flask died(%s)' % datetime.datetime.now())
GPIO.cleanup()
