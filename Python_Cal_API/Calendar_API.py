#!/usr/bin/python
"""
This is sample code from the google calendar api for python to get som calendar events. The code is modified to suit our needs for
a smartclock.
"""
from __future__ import print_function
import httplib2
import os

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

import datetime

try:
    import argparse
    flag = argparse.ArgumentParser(parents=[tools.argparser]).parse_args();
except ImportError:
    flag = None;

#scope url for read/write naar calendar data.
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
#client secret file generated and downloaded from google developper and saved in working dir
CLIENT_SECRET_FILE = 'Calender_credentials.json'
#The name of the application
APPLICATION_NAME = 'Get calendar events'

#Get the credentials for OAuth2.
def getCredentials():
    #Give the home dir from the current user
    home_dir = os.path.expanduser('~')
    #Make the path to the credentials folder in the home directory
    credential_dir = os.path.join(home_dir, '.credentials')
    print(credential_dir)
    #Check if the credential folder exists --> create if not
    if (not os.path.exists(credential_dir)):
        os.makedirs(credential_dir)
    #Make the path to the credentials json file
    credential_path = os.path.join(credential_dir,'Calender_credentials.json')
    print(credential_path)
    #Make a variable store and select this as the storage dir for the credentials
    store = oauth2client.file.Storage(credential_path)
    #try to get the credentials from the store dir
    credent = store.get()
    #if there are  no (valid) credentials --> start the flow to get some
    if not credent or credent.invalid:
        #start the flow to get credentials --> get credentials
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)

        flow.user_agent = APPLICATION_NAME
        if flag:
            credent = tools.run_flow(flow, store, flag)
        else: # Needed only for compatibility with Python 2.6
            credent = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    #Return the credentials to the main function
    return credent


def main():
    """Shows basic usage of the Google Calendar API.

    Creates a Google Calendar API service object and outputs a list of the next
    10 events on the user's calendar.
    """
    #Store the valid credentials
    credential = getCredentials()
    #create and authorize an httplib2.Http object to handle the http request
    http = credential.authorize(httplib2.Http())
    #create a API service object to make API calls --> Give param of service, authorized http object (See above)
    service_calendar = discovery.build('calendar', 'v3', http=http)
    #Get the current date and time
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    #save the returned values from the API call
    eventsResult = service_calendar.events().list(
        calendarId='primary', timeMin=now, maxResults=15, singleEvents=True,
        orderBy='startTime').execute()
    #Strip the actual useful data containent within []
    events = eventsResult.get('items', [])
    #If there are no events print a message to say so.
    if not events:
        print('No upcoming events found.')
    #If there are events print for every one of them the startdate/time and the summary
    for event in events:
        #Get the date and time from the start list ('start': {'dateTime': '2016-03-05T09:00:00+01:00'})
        start = event['start'].get('dateTime')
        print(start, event['summary'])


if __name__ == '__main__':
    getCredentials()
    main()