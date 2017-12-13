#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 21-11-2017, Alisher A. Khassanov for Airalab, alisher@aira.life
# http response with rosbag file content


from datetime import date, timedelta
from flask import Flask
from flask import request
import rosbag, json, os

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
    Expected bag files like 2017-12-13-14-24-38.bag
    """
    d1, d2 = str_to_dates(request.args.get('date'))
    days = [ d1 + timedelta(days=x) for x in range((d2 - d1).days + 1) ]
    paths = [ '{0}-{1}-{2}-{3}-{4}-{5}.bag'.format(d.year, d.month, d.day, h, m, s)
                for d in days for h in range(0, 24) for m in range(0, 60) for s in range(0, 60) ]
    content = [ bag_to_str(p) for p in paths if os.path.isfile(p) ]
    return ''.join(content)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=30000)
