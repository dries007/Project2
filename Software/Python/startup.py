#!/usr/bin/env python

import os
import pygame
import time
import json
import random

from subprocess import call

VERSION = "0.1"

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

pygame.display.init()
pygame.mouse.set_visible(False)
pygame.font.init()

FONT_100 = pygame.font.Font(None, 100)
FONT_50 = pygame.font.Font(None, 50)
FONT_25 = pygame.font.Font(None, 25)

SIZE = (pygame.display.Info().current_w, pygame.display.Info().current_h)
SCREEN = pygame.display.set_mode(SIZE, pygame.FULLSCREEN)
SCREEN.fill(BLACK)

settings = {}
status = {
    "network": False
}
if os.path.isfile("settings.json"):
    settings = json.load(open("settings.json"))


def draw_text(message, font=FONT_25, color=WHITE, height=0):
    tmp = font.render(message, False, color)
    SCREEN.blit(tmp, (0, h))
    pygame.display.update()
    return height + tmp.get_height()


def hang(message):
    """Goodbye cruel world."""
    SCREEN.fill(BLACK)
    h = draw_text('SmartClock (%s)' % VERSION, FONT_50)
    h = draw_text('Fatal Error', color=RED, height=h)
    draw_text(message, height=h)
    while True:
        time.sleep(60)


h = draw_text('SmartClock (%s)' % VERSION)
h = draw_text('Booting...', height=h)

if not os.path.exists("/sys/class/net/wlan0"):
    hang("No wifi interface")

if os.path.exists("/sys/class/i2c-adapter/i2c-1/1-0068/"):
    call("echo 0x68 > /sys/class/i2c-adapter/i2c-1/delete_device".split(" "), shell=True)

call("echo ds3231 0x68 > /sys/class/i2c-adapter/i2c-1/new_device".split(" "), shell=True)

if settings.wifiProfile:
    h = draw_text('Connecting to %s' % settings.wifiProfile, height=h)
    call(["netctl", "stop-all"])
    if call(["netctl", "start", settings.wifiProfile]) == 0:
        hasNetwork = True
        h = draw_text('Syncing date & time', height=h)
        if call("ntp-wait -n 5".split(" ")) != 0:
            hang("NTP sync failed.")
    else:
        h = draw_text('Failed...', height=h)

if not status["network"]:
    call("hwclock -s".split(" "))
    h = draw_text('Starting AP', height=h)
    call("systemctl start create_ap".split(" "))

print(settings)
