#!/usr/bin/env python
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(3, GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(5, GPIO.IN,pull_up_down=GPIO.PUD_UP)
volume = 50
prev_pin = False
while volume <= 100:
        pin_A = GPIO.input(3)
        pin_B =GPIO.input(5)
        if (pin_A == False and prev_pin == True):
            if (pin_B == True):
                volume = volume +1
                print(volume)
            else:
                volume = volume -1
                print(volume)
        prev_pin = pin_A
        time.sleep(1/1000)
