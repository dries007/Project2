#!/bin/env python
import wifi

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

if __name__ == "__main__":
    app.run()