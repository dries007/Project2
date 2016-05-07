#!/bin/env python
import os
import sys
# noinspection PyUnresolvedReferences
import pygame
import socket
import time
import json
import random
import datetime
import re
import subprocess
import sched
import threading

from flask import Flask
from flask import json
from flask import Response
from flask import request

app = Flask(__name__)
VERSION = "0.1"

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

threadLocal = threading.local()

CLOCK = sched.scheduler(time.time, time.sleep)

pygame.display.init()
pygame.font.init()
pygame.mouse.set_visible(False)

FONT_XL = pygame.font.SysFont("notomono", 60)
FONT_L = pygame.font.SysFont("notomono", 36)
FONT_M = pygame.font.SysFont("notomono", 26)
FONT_S = pygame.font.SysFont("notomono", 15)

SIZE = (pygame.display.Info().current_w, pygame.display.Info().current_h)
SCREEN = pygame.display.set_mode(SIZE, pygame.FULLSCREEN)
SCREEN.fill(BLACK)

subprocess.call("killall hostapd".split(" "))
subprocess.call("create_ap --stop wlan0".split(" "))

settings = {
    "clock": {
        "format": "%H:%M:%S",
        "size": 60,
    },
    "date": {
        "format": "%Y-%m-%d",
        "size": 36
    }
}
status = {
    "network": False,
    "clock": False
}
if os.path.isfile("settings.json"):
    settings = json.load(open("settings.json"))

FONT_CLOCK = pygame.font.SysFont("notomono", settings["clock"]["size"])
FONT_DATE = pygame.font.SysFont("notomono", settings["date"]["size"])


def save():
    json.dump(settings, open('settings.json', 'w'))


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


def attempt_connect(height=0):
    # Just to be sure
    subprocess.call("killall hostapd".split(" "))
    subprocess.call("create_ap --stop wlan0".split(" "))
    height = draw_text('Connecting to %s' % settings["wifiProfile"], height=height)
    if subprocess.call(["netctl", "switch-to", settings["wifiProfile"]]) == 0:
        status["network"] = True
        height = draw_text(socket.gethostbyname(socket.gethostname()), height=height, font=FONT_M)
        height = draw_text('Syncing time & date', height=height)
        subprocess.call("systemctl restart ntpd".split(" "))
        if subprocess.call("ntp-wait -n 5".split(" ")) != 0:
            error("NTP sync failed.")
        else:
            subprocess.call("hwclock -w".split(" "))
            status["clock"] = True
    else:
        height = draw_text('Failed...', height=height)
    return height

h = draw_text('SmartClock (%s)' % VERSION, font=FONT_M)

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
    h = draw_text('SmartAlarmClock', height=h, font=FONT_M)
    h = draw_text('And browse to:', height=h)
    h = draw_text(socket.gethostbyname(socket.gethostname()), height=h, font=FONT_M)


@app.route("/")
def root():
    return "qsdsqd"


@app.route("/api/wifi", methods=['GET', 'POST'])
def api_wifi():
    if request.method == 'POST':
        status["clock"] = False
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
        save()
        attempt_connect()
        if status["network"]:
            return "OK"
        return "ERROR"
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


@app.route("/api/settings")
def debug_settings():
    return json.dumps(settings)


@app.route("/api/status")
def debug_status():
    return json.dumps(status)


def update_ip():
    threadLocal.ip = socket.gethostbyname(socket.gethostname())
    CLOCK.enter(10, 2, update_ip)


def draw_clock():
    if status["clock"]:
        height = draw_text(datetime.datetime.now().strftime(settings["clock"]["format"]), font=FONT_CLOCK)
        draw_text(datetime.datetime.now().strftime(settings["date"]["format"]), height=height, font=FONT_DATE)
        draw_text(threadLocal.ip, height=height + 60, font=FONT_S)

    CLOCK.enter(1, 1, draw_clock)


def run_clock_thread():
    threadLocal.ip = socket.gethostbyname(socket.gethostname())
    CLOCK.run()

CLOCK.enter(1, 1, draw_clock)
CLOCK.enter(10, 2, update_ip)
threading.Thread(target=run_clock_thread, name="ClockThread", daemon=True).start()

app.run(host="0.0.0.0", port=5000, debug=True, use_debugger=True, use_reloader=False)  # todo: disable debug!
