# -*- coding: utf-8 -*-

import rosbag
from std_msgs.msg import String


bag = rosbag.Bag('./mybag.bag', 'w')
msg = String(data='mystring')

try:
    bag.write(topic, msg)
finally:
    bag.close()
