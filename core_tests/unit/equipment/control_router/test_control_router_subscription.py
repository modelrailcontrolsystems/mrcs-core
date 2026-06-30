"""
Created on 29 Jun 2026

@author: Bruno Beloff (bbeloff@me.com)

python -m unittest -v unit/equipment/control_router/test_control_router_subscription.py

https://realpython.com/python-testing/
https://www.jetbrains.com/help/pycharm/creating-tests.html
"""

import json
import unittest

from mrcs_control.dcc.z21.command.broadcast import Broadcast
from mrcs_core.data.json import JSONify
from mrcs_core.equipment.control_router.control_router_subscription import ControlRouterSubscription


# --------------------------------------------------------------------------------------------------------------------

class TestControlRouterSubscription(unittest.TestCase):

    def test_control_router_subscription(self):
        flags = [Broadcast.TRACK, Broadcast.CAN_DETECTOR, Broadcast.X_LOCO_INFO_ALL]
        obj1 = ControlRouterSubscription(*flags)
        self.assertEqual('ControlRouterSubscription:{flags:[CAN_DETECTOR, TRACK, X_LOCO_INFO_ALL]}', str(obj1))


    def test_control_router_subscription_json(self):
        flags = [Broadcast.TRACK, Broadcast.CAN_DETECTOR, Broadcast.X_LOCO_INFO_ALL]
        obj1 = ControlRouterSubscription(*flags)
        jstr = JSONify.dumps(obj1)
        self.assertEqual('{"flags": ["CAN_DETECTOR", "TRACK", "X_LOCO_INFO_ALL"]}', jstr)


    def test_control_router_subscription_json_eq(self):
        flags = [Broadcast.TRACK, Broadcast.CAN_DETECTOR, Broadcast.X_LOCO_INFO_ALL]
        obj1 = ControlRouterSubscription(*flags)
        jstr = JSONify.dumps(obj1)
        obj2 = ControlRouterSubscription.construct_from_jdict(json.loads(jstr))
        self.assertEqual(obj1, obj2)


    def test_control_router_subscription_value(self):
        flags = [Broadcast.TRACK, Broadcast.CAN_DETECTOR, Broadcast.X_LOCO_INFO_ALL]
        obj1 = ControlRouterSubscription(*flags)
        val1 = obj1.value
        self.assertEqual('0x00090001', f'0x{val1:08x}')


    def test_control_router_subscription_value_none(self):
        flags = []
        obj1 = ControlRouterSubscription(*flags)
        val1 = obj1.value
        self.assertEqual('0x00000000', f'0x{val1:08x}')


# --------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    unittest.main()
