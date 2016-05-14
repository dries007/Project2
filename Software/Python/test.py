#!/bin/env python
import datetime
import time
# noinspection PyUnresolvedReferences
import RPi.GPIO as GPIO

RE_A = 16
RE_B = 5
RE_S = 6


def rot(chan):
    a = GPIO.input(RE_A)
    if a:
        return
    b = GPIO.input(RE_B)
    print("A: %s B: %s" % (a, b))

GPIO.setmode(GPIO.BCM)
GPIO.setup([RE_A, RE_B, RE_S], GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.add_event_detect(RE_A, GPIO.FALLING, callback=rot, bouncetime=25)

input("Press enter for exit\n")
