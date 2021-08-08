#!/usr/bin/env python3

# API which serves the statistics for the raspberry pi and allows for basic
# functionality such as :

from flask import Flask, jsonify, redirect, request

import json
from flask.helpers import url_for
from flask_cors import CORS, cross_origin
import psutil
import time
import datetime
import math
from fanctrl import FanController

app = Flask(__name__)
fan = FanController()
cors = CORS(app,resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

## TODO
# - Percentage of CPU
# - Percentage of Memory
# - users & other info
# - Storage left
# - Switch to websockets instead
# - Make a class object

def get_uptime():
    return time.time() - psutil.boot_time()

def convert_size(size_bytes):
   if size_bytes == 0:
       return "0B"
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size_bytes, 1024)))
   p = math.pow(1024, i)
   s = round(size_bytes / p, 2)
   return "%s %s" % (s, size_name[i])

def get_stats():

    stats = {}

    # Calculate uptime
    stats["uptime"] = str(datetime.timedelta(seconds=get_uptime()))

    # Calculate Temperature
    temps = psutil.sensors_temperatures()["cpu_thermal"][0][1]
    stats["temp"] = str(temps)

    # Calculate the Fan Speed
    stats["fanSpeed"] = float(fan.freq)
    
    # Calculate Usage : CPU
    cpu_usage = psutil.cpu_percent()

    # Calculate Usage : Mem
    mem = psutil.virtual_memory()
    mem_stats = {"total": convert_size(mem.total),
                 "used": convert_size(mem.used),
                 "percentage":mem.percent}

    # Calculate Usage : DiskSpace
    disk = psutil.disk_usage("/")
    disk_stats = {"total": convert_size(disk.total),
                  "used": convert_size(disk.used),
                  "percentage": disk.percent}

    
    # Put it all together
    stats["usage"] = {"cpu":cpu_usage,"memory":mem_stats,"disk":disk_stats}

    return stats


@app.route("/")
@cross_origin()
def temp():
    response = jsonify(get_stats())
    #response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route("/fan-update",methods=["POST"])
@cross_origin()
def fanupdate():
    newFreq = request.form["newFreq"]
    fan.changeFrequency(float(newFreq))
    print(request.data)
    resp = jsonify(success=True)
    return resp


if __name__ == "__main__":
    app.run(host="0.0.0.0")
