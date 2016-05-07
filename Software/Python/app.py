#!/bin/env python
import os
# noinspection PyUnresolvedReferences
import pygame
import socket
import time
import json
import random
import datetime
import re
import subprocess

from flask import Flask
from flask import json
from flask import Response
from flask import request

app = Flask(__name__)
VERSION = "0.1"

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

pygame.display.init()
pygame.font.init()
pygame.mouse.set_visible(False)

FONT_100 = pygame.font.Font(None, 100)
FONT_50 = pygame.font.Font(None, 50)
FONT_25 = pygame.font.Font(None, 25)

SIZE = (pygame.display.Info().current_w, pygame.display.Info().current_h)
SCREEN = pygame.display.set_mode(SIZE, pygame.FULLSCREEN)
SCREEN.fill(BLACK)

subprocess.call("killall hostapd".split(" "))
subprocess.call("create_ap --stop wlan0".split(" "))

settings = {}
status = {
    "network": False
}
if os.path.isfile("settings.json"):
    settings = json.load(open("settings.json"))


def draw_text(message, font=FONT_25, color=WHITE, height=0):
    if height == 0:
        SCREEN.fill(BLACK)
    tmp = font.render(message, False, color)
    SCREEN.blit(tmp, (0, height))
    pygame.display.update()
    return height + tmp.get_height()


def error(message):
    SCREEN.fill(BLACK)
    height = draw_text('SmartClock (%s)' % VERSION, FONT_50)
    height = draw_text('Fatal Error', color=RED, height=height)
    draw_text(message, height=height)


def attempt_connect(height=0):
    # Just to be sure
    subprocess.call("killall hostapd".split(" "))
    subprocess.call("create_ap --stop wlan0".split(" "))
    height = draw_text('Connecting to %s' % settings["wifiProfile"], height=height)
    if subprocess.call(["netctl", "switch-to", settings["wifiProfile"]]) == 0:
        status["network"] = True
#        time.sleep(5)
        height = draw_text(socket.gethostbyname(socket.gethostname()), height=height)
        height = draw_text('Syncing date & time', height=height)
        subprocess.call("systemctl restart ntpd".split(" "))
        if subprocess.call("ntp-wait -n 5".split(" ")) != 0:
            error("NTP sync failed.")
        subprocess.call("hwclock -w".split(" "))
        height = draw_text(datetime.datetime.now(), height=height)
    else:
        height = draw_text('Failed...', height=height)
    return height

h = draw_text('SmartClock (%s)' % VERSION, font=FONT_50)

if not os.path.exists("/sys/class/net/wlan0"):
    error("No wifi interface")

if "wifiProfile" in settings and settings["wifiProfile"] != "":
    h = attempt_connect(h)

if not status["network"]:
    subprocess.call("hwclock -s".split(" "))
    h = draw_text('Starting AP', height=h)
    subprocess.call("create_ap -n --daemon --redirect-to-localhost wlan0 SmartAlarmClock".split(" "))
    time.sleep(5)
    h = draw_text('Connect to wifi network for setup:', height=h)
    h = draw_text('SmartAlarmClock', height=h, font=FONT_50)
    h = draw_text('And browse to:', height=h)
    h = draw_text(socket.gethostbyname(socket.gethostname()), height=h, font=FONT_50)


@app.route("/")
def root():
    return "qsdsqd"


@app.route("/api/wifi", methods=['GET', 'POST'])
def api_wifi():
    if request.method == 'POST':
        text = "Description='Automatically generated profile by python'\n"
        text += "Interface=wlan0\n"
        text += "Connection=wireless\n"
        text += "IP=dhcp\n"
        text += "ESSID='%s'\n" % request.form['ssid']

        if "pass" in request.form:
            text += "Security=wpa\nKey='%s'" % request.form["pass"]
        else:
            text += "Security=none"

        settings["wifiProfile"] = "GEN-wlan0-%s" % request.form["ssid"]
        f = open("/etc/netctl/%s" % settings["wifiProfile"], "w")
        f.write(text)
        f.close()
        attempt_connect()
        if status["network"]:
            return "YES"
        return "NO"
    else:
        re_cell = re.compile(r'Cell \d+')
        re_mac = re.compile(r'Address: (?P<Address>.*)')
        re_ssid = re.compile(r'ESSID:"(?P<SSID>.*)"')
        re_quality = re.compile(r'Quality=(?P<Quality>\d+)/100')
        re_signal = re.compile(r'Signal level=(?P<SignalLevel>\d+)/100')
        re_encrypted = re.compile(r'Encryption key:(?P<Protected>on|off)')
        re_encryption = re.compile(r'IE: (?P<Protection>.*)')
        re_authentication = re.compile(r'Authentication Suites \(1\) : (?P<Authentication>.*)')

        proc = subprocess.Popen(["iwlist", "wlan0", "scan"], stdout=subprocess.PIPE, universal_newlines=True)
        out, err = proc.communicate()

        data = []
        cell = None
        for line in out.split("\n"):
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


@app.route("/debug/settings")
def debug_settings():
    return json.dumps(settings)


@app.route("/debug/status")
def debug_status():
    return json.dumps(status)

app.run(host="0.0.0.0", port=5000)  # todo: disable debug!

