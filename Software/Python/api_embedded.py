#!/usr/bin/env python
import requests
import json
import threading
import time
from datetime import datetime


def getverinfo():
    url = "https://accounts.google.com/o/oauth2/device/code"
    clientID = "806788990556-i96frm71oem88mn63qvsudbmvhrusesf.apps.googleusercontent.com"
    scope = "https://www.googleapis.com/auth/calendar.readonly"
    params = {'client_id': clientID, 'scope': scope}
    r = requests.post(url, data=params)
    data = json.loads(r.text)
    devicecode = data['device_code']
    interval = data['interval']
    t1 = threading.Thread(target=checkauth, args=(devicecode, clientID, interval))
    t1.daemon = True
    t1.start()
    return r.text

#Opvragen van een code om authenticatie te bevestigen
# Refreshtoken moet nog worden opgeslagen in langdurige opslag --> zo lang mogelijk gebruiken
def checkauth(devcode, clientID, interv):
    test = 1
    while (test):
        url = "https://www.googleapis.com/oauth2/v4/token"
        grant_type = "http://oauth.net/grant_type/device/1.0"
        clientsecret = "MFDHJWCHUl_CHAwokNvPXyR4"
        params = {'client_id': clientID, 'code': devcode, 'client_secret': clientsecret, 'grant_type': grant_type}
        resp = requests.post(url, data=params)
        resp.encoding = "application/x-www-form-urlencoded"
        data = json.loads(resp.text)
        if ( "error" in data):
            print(resp.text)
            time.sleep(interv)
        else:
            savevalues(data)
            test = 0

# using the refresh token to get a new valid access token
def refreshtoke(clientId, clientsecret, refreshtoken):
    url = "https://www.googleapis.com/oauth2/v4/token"
    grant_type="refresh_token"
    params = {'client_id': clientId, 'client_secret': clientsecret, 'refresh_token': refreshtoken, 'grant_type': grant_type}
    resp = requests.post(url, data=params)
    print ("testing")
    print(resp.text)

# juiste data opvragen en filteren uit de response
def savevalues(data):
    acc_tok = data["access_token"]
    tokenty = data["token_type"]
    expire = data["expires_in"]
    refresh = data["refresh_token"]
    tijd = datetime.now()
    tijd = tijd.isoformat("T") + "Z"
    print (tijd)
    url = "https://www.googleapis.com/calendar/v3/calendars/primary/events?access_token=" + acc_tok+"&timeMin="+tijd
    testing = requests.get(url)
    data = json.loads(testing.text)
    for item in data['items']:
        print(item['start']['dateTime'])
        print(item['summary'])
    refreshtoke("806788990556-i96frm71oem88mn63qvsudbmvhrusesf.apps.googleusercontent.com", "MFDHJWCHUl_CHAwokNvPXyR4", refresh)

