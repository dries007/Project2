#!/bin/env python
import datetime
import os

START_TIME = datetime.datetime.now()
print('Loading libs... (%s)' % START_TIME)
os.putenv('SDL_FBDEV', '/dev/fb1')
# os.putenv('SDL_VIDEODRIVER', 'fbcon')

# noinspection PyUnresolvedReferences
import pygame
# noinspection PyUnresolvedReferences
import RPi.GPIO as GPIO
import socket
import time
import json
import re
import urllib
import subprocess
import sched
import threading

from flask import Flask
from flask import json
from flask import Response
from flask import request
from flask import url_for

from enum import Enum, unique


@unique
class Menu(Enum):
    Exit = {'name': 'Exit', 'setting': None}
    Show_IP = {'name': 'Show IP', 'setting': None}
    Set_Volume = {'name': 'Set Volume', 'setting': ('sound', 'volume')}
    Set_Brightness = {'name': 'Set Brightness', 'setting': ('brightness', 'preference')}

print('Defining functions ... (%s)' % (datetime.datetime.now() - START_TIME))

app = Flask(__name__)

VERSION = '0.1'
SETTINGS_FILE = "/root/www/settings.json"

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

threadLocal = threading.local()

CLOCK = sched.scheduler(time.time, time.sleep)

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

subprocess.call(['killall', 'hostapd'])
subprocess.call(['create_ap', '--stop', 'wlan0'])

RE_A = 16
RE_B = 5
RE_S = 6

GPIO.setmode(GPIO.BCM)
GPIO.setup([RE_A, RE_B, RE_S], GPIO.IN, pull_up_down=GPIO.PUD_UP)
subprocess.call(['gpio', '-g', 'mode', '12', 'pwm'])
subprocess.call(['gpio', '-g', 'pwm', '12', '1023'])


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
status = {
    'network': False,
    'draw': {
        'clock': False,
        'option': None
    },
    'menu': None,
    'clock': False,
    'pulsing': False
}

if os.path.isfile(SETTINGS_FILE):
    settings = json.load(open(SETTINGS_FILE))

FONT_DAY = pygame.font.SysFont('notomono', settings['day']['size'])
FONT_CLOCK = pygame.font.SysFont('notomono', settings['clock']['size'])
FONT_DATE = pygame.font.SysFont('notomono', settings['date']['size'])


##############################################################################
#                           Functions
##############################################################################


def clamp(n, minn=0, maxn=1):
    return max(min(maxn, n), minn)


def save():
    json.dump(settings, open(SETTINGS_FILE, 'w'))


def btn(chan):
    if not status['draw']['clock']:
        return
    if status['menu']:
        status['draw']['option'] = status['menu']
        status['menu'] = None
    elif status['draw']['option']:
        status['draw']['option'] = None
    else:
        status['menu'] = Menu.Show_IP


def rot(chan):
    a = GPIO.input(RE_A)
    if a:
        return
    b = GPIO.input(RE_B)
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


def update_ip():
    threadLocal.ip = socket.gethostbyname(socket.gethostname())
    CLOCK.enter(10, 3, update_ip)


def update_pwm():
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
    CLOCK.enter(0.1, 2, update_pwm)


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


def draw_clock():
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
    CLOCK.enter(0.1, 1, draw_clock)


def run_clock_thread():
    threadLocal.ip = socket.gethostbyname(socket.gethostname())
    update_ip()
    update_pwm()
    draw_clock()
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

##############################################################################
#                           Sequential code
##############################################################################

GPIO.add_event_detect(RE_A, GPIO.FALLING, callback=rot, bouncetime=25)
GPIO.add_event_detect(RE_S, GPIO.FALLING, callback=btn, bouncetime=200)

threading.Thread(target=run_clock_thread, name='ClockThread', daemon=True).start()
h = draw_text('SmartClock (%s)' % VERSION, font=FONT_M)

if not os.path.exists('/sys/class/net/wlan0'):
    error('No wifi interface')

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


##############################################################################
#                           Flask Routes
##############################################################################

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

##############################################################################
#                           Sequential code
##############################################################################

print('Starting webserver... (%s)' % (datetime.datetime.now() - START_TIME))
app.run(host='0.0.0.0', port=5000, debug=True, use_debugger=True, use_reloader=False)  # todo: disable debug!

GPIO.cleanup()
