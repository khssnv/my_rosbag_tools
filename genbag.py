# -*- coding: utf-8 -*-

import rosbag
from robonomics_game_transport.msg import TransportAction, TransportActionGoal, TransportGoal

colors = ['yellow', 'green', 'blue', 'purple']
addresses = [1, 2, 3, 4]
topic = '/transport_goods/storage/goal'

for (addr, color) in [(addr, color) for addr in addresses for color in colors]:
    bag = rosbag.Bag('./storage/addr-%d_color-%s.bag' % (addr, color), 'w')
    try:
        msg = TransportActionGoal(goal=TransportGoal(address=addr, specification=color))
        bag.write(topic, msg)
    finally:
        bag.close()
