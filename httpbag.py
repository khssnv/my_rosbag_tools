#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 21-11-2017, Alisher A. Khassanov for Airalab, alisher@aira.life
# http response with rosbag file content


from datetime import date, timedelta
from dateutil.parser import parse
from flask import Flask
from flask import request
from flask_cors import CORS
import rosbag, json, os

app = Flask(__name__)
CORS(app)

def bag_to_str(path):
    bag = rosbag.Bag(path)
    out = ""
    for topic, msg, t in bag.read_messages():
        msg = str(msg).replace('\n', ', ')
        out = out + ', ' + json.dumps({'topic': topic, 'msg': msg, 'time': t.to_time()})
    out = '{' + out[2:] + '}'
    bag.close()
    return out

@app.route('/api/v0/bag/<bag_from>/<bag_to>')
def main(bag_from, bag_to):
    """
    Expected bag files like 2017-12-13-14-24-38.bag
    """
    d1 = parse(bag_from)
    d2 = parse(bag_to)
    days = [d1 + timedelta(days=x) for x in range((d2-d1).days + 1)]
    paths = [ '{0}-{1}-{2}-{3}-{4}-{5}.bag'.format(d.year, d.month, d.day, h, m, s)
                for d in days for h in range(24) for m in range(60) for s in range(60) ]
    content = [ bag_to_str(p) for p in paths if os.path.isfile(p) ]
    return ''.join(content)

if __name__ == '__main__':
    app.run()
