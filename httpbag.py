#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# 21-11-2017, Alisher A. Khassanov for Airalab, alisher@aira.life
# http response with rosbag file content


import sys
if sys.version_info[0] > 2:
    raise ImportError('Only python2 supported due to rosbag demands')
import os
import json
from datetime import date, timedelta
from flask import Flask
from flask import request
import rosbag

app = Flask(__name__)

def bag_to_str(path):
    bag = rosbag.Bag(path)
    out = ""
    for topic, msg, t in bag.read_messages():
        msg = str(msg).replace('\n', ', ')
        out = out + ', ' + json.dumps({'topic': topic, 'msg': msg, 'time': t.to_time()})
    out = '{' + out[2:] + '}'
    bag.close()
    return out

def str_to_dates(ds): # dates string
    """
    Expected URL example: http://.../?date=18.11.2017+11%3A15+-+21.11.2017+11%3A15
    """
    since = date(int(ds[6:10]), int(ds[3:5]), int(ds[0:2])) # (yy, mm, dd)
    until = date(int(ds[25:29]), int(ds[22:24]), int(ds[19:21]))
    return [since, until]

@app.route('/')
def main():
    """
    Expected bag files path: <PATH>/<yyyy>/<mm>/<dd>/<hh>.bag
    """
    dates = str_to_dates(request.args.get('date'))
    get_days = lambda d1, d2: [d1 + timedelta(days=x) for x in range((d2-d1).days + 1)]
    days = get_days(dates[0], dates[1])
    paths = []
    for d in days:
        p = path + '/' + str(d.year) + '/' + str(d.month) + '/' + str(d.day)
        if os.path.exists(p): # if directory exists
            for h in range(1, 25):
                pp = p + '/' + str(h) + '.bag'
                if os.path.isfile(pp): # if file exists
                    paths.append(pp)
    content = ''
    for p in paths:
        content = content + bag_to_str(p)
    return content

if __name__ == '__main__':
    try:
        path = os.path.abspath(sys.argv[1])
    except IndexError as e:
        e.message = 'ERROR: root path not specified. Usage: "$ ./httpbag.py <PATH>"'
        raise
    if not os.path.exists(path):
        raise RuntimeError('ERROR: path ' + path + ' not exist')
    app.run()
