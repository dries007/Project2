#!/bin/env python
import wifi
import api_embedded

from flask import Flask
from flask import json
from flask import Response
from flask import request

app = Flask(__name__)

#todo: debug, remove!
app.debug = True

@app.errorhandler(404)
def pageNotFound(error):
    return "Method not found. ", 404

@app.route("/WiFiList", methods=['GET', 'POST'])
def wifiList():
    if request.method == 'GET':
        return Response(json.dumps(wifi.scanWifi()), mimetype='text/javascript')
    else:

        return 'OK?'

@app.route("/Verification", methods=['GET', 'POST'])
def verification():
    if request.method == 'GET':
        return Response(api_embedded.getverinfo())
    else:

        return 'OK?'

if __name__ == "__main__":
    app.run()