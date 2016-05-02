#!/usr/bin/env python

import re
import subprocess


def scanWifi(interface="wlan0"):
    re_cell = re.compile(r'Cell \d+')
    re_mac = re.compile(r'Address: (?P<Address>.*)')
    re_ssid = re.compile(r'ESSID:"(?P<SSID>.*)"')
    re_quality = re.compile(r'Quality=(?P<Quality>\d+)/100')
    re_signal = re.compile(r'Signal level=(?P<SignalLevel>\d+)/100')
    re_encrypted = re.compile(r'Encryption key:(?P<Protected>on|off)')
    re_encryption = re.compile(r'IE: (?P<Protection>.*)')
    re_authentication = re.compile(r'Authentication Suites \(1\) : (?P<Authentication>.*)')

    proc = subprocess.Popen(["iwlist", interface, "scan"], stdout=subprocess.PIPE, universal_newlines=True)
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

    return data
