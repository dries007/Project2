#!/usr/bin/env python

import requests
import json
import threading
import time
from datetime import datetime


def getverinfo():
    print("Getting necessary ID's")
    url = getjsonvalue('url')
    clientID = getjsonvalue("client_id")
    scope = getjsonvalue("scope")
    params = {'client_id': clientID, 'scope': scope}
    r = requests.post(url, data=params)
    data = json.loads(r.text)
    devicecode = data['device_code']
    interval = data['interval']
    t1 = threading.Thread(target=checkauth, args=(devicecode, clientID, interval))
    # t1.daemon = True
    t1.start()
    print(r.text)
    return r.text


def getjsonvalue(property_id):
    tekst = open('authinfo').read()
    d = json.loads(tekst)
    return d[property_id]


def getjsonaccess(prop_id):
    tekst = open('API_tokens').read()
    d = json.loads(tekst)
    return d[prop_id]


def savecal(data):
    fh = open("calendardata", "w")
    json.dump(data, fh, indent=2)
    fh.close()


# Opvragen van een code om authenticatie te bevestigen
# Refreshtoken moet nog worden opgeslagen in langdurige opslag --> zo lang mogelijk gebruiken
def checkauth(devcode, clientID, interv):
    print("Waiting for authenticaion by user")
    test = 1
    while test:
        url = "https://www.googleapis.com/oauth2/v4/token"
        grant_type = "http://oauth.net/grant_type/device/1.0"
        clientsecret = getjsonvalue("client_secret")
        params = {'client_id': clientID, 'code': devcode, 'client_secret': clientsecret, 'grant_type': grant_type}
        resp = requests.post(url, data=params)
        resp.encoding = "application/x-www-form-urlencoded"
        data = json.loads(resp.text)
        if "error" in data:
            time.sleep(interv)
        else:
            saveapiinfo(data)
            getcalevents()
            test = 0


# using the refresh token to get a new valid access token
def refreshtoke():
    clientId = getjsonvalue("client_id")
    clientsecret = getjsonvalue("client_secret")
    refreshtoken = getjsonaccess("refresh_token")
    url = "https://www.googleapis.com/oauth2/v4/token"
    grant_type = "refresh_token"
    params = {'client_id': clientId, 'client_secret': clientsecret, 'refresh_token': refreshtoken, 'grant_type': grant_type}
    resp = requests.post(url, data=params)
    next_auth = json.loads(resp.text)
    print("reading current authentication information")
    fh = open("API_tokens", "r")
    tekst = fh.read()
    fh.close()
    current_auth = json.loads(tekst)
    print("change the access_token with the new token from refresh")
    current_auth["access_token"] = next_auth["access_token"]
    ###########
    saveapiinfo(current_auth)
    # print(resp.text)


def saveapiinfo(data):
    fh = open("API_tokens", "w")
    json.dump(data, fh, indent=2)
    fh.close()


# juiste data opvragen en filteren uit de response
def getcalevents():
    acc_tok = getjsonaccess("access_token")
    acctype = getjsonaccess("token_type")
    tijd = datetime.now()
    tijd = tijd.isoformat("T") + "z"
    print("Alle evenementen na: " + tijd + " worden opgehaald")
    url = "https://www.googleapis.com/calendar/v3/calendars/primary/events"
    param = {'timeMin': tijd}
    header = {"Authorization": acctype + " " + acc_tok}
    testing = requests.get(url, headers=header, params=param)
    data = json.loads(testing.text)
    savecal(data)
    printcalevents()


def printcalevents():
    inputdata = open('calendardata').read()
    values = json.loads(inputdata)
    for item in values['items']:
        print(item['start']['dateTime'])
        print(item['summary'])


getverinfo()
