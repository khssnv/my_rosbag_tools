#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 21-11-2017, Alisher A. Khassanov for Airalab, alisher@aira.life
# http response with rosbag file content

from datetime import date, timedelta
from dateutil.parser import parse
from flask import Flask
from flask import request
from flask import jsonify
from flask_cors import CORS
from message_converter import convert_ros_message_to_dictionary
import rosbag, json, os

app = Flask(__name__)
CORS(app)

def read_messages(path):
    with rosbag.Bag(path) as bag:
        return [{'topic': topic, 'msg': convert_ros_message_to_dictionary(msg), 'time': t.to_time()}
                for topic, msg, t in bag.read_messages()]

@app.route('/api/v0/bag/<bag_from>/<bag_to>')
def main(bag_from, bag_to):
    """
    Expected bag files like 2017-12-13-14-24-38_0.bag
    """
    d1 = parse(bag_from)
    d2 = parse(bag_to)
    days = [d1 + timedelta(days=x) for x in range((d2-d1).days + 1)]
    paths = [ '{0}-{1}-{2}-{3}-{4}-{5}.bag'.format(d.year, d.month, d.day, h, m, s)
                for d in days for h in range(0, 25) for m in range(0, 60) for s in range(0, 60) ]
    content = [ read_messages(p) for p in paths if os.path.isfile(p) ]
    return jsonify(sum(content, []))

if __name__ == '__main__':
    app.run()
