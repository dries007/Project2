#!/bin/env python
import datetime
from time import sleep

START_TIME = datetime.datetime.now()
print("Starting... (%s)" % START_TIME)

sleep(25)

print("Done... (%s)" % START_TIME)
