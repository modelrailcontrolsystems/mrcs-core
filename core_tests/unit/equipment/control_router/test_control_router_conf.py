"""
Created on 28 Jun 2026

@author: Bruno Beloff (bbeloff@me.com)

python -m unittest -v unit/equipment/control_router/test_control_router_conf.py

https://realpython.com/python-testing/
https://www.jetbrains.com/help/pycharm/creating-tests.html
"""

import json
import unittest

from mrcs_control.dcc.z21.command.broadcast import Broadcast
from mrcs_core.data.json import JSONify
from mrcs_core.equipment.control_router.control_router_conf import ControlRouterConf
from mrcs_core.equipment.control_router.control_router_subscription import ControlRouterSubscription
from mrcs_core.sys.host import Host
from mrcs_core.sys.ipv4_address import IPv4Address


# --------------------------------------------------------------------------------------------------------------------

class TestControlRouterConf(unittest.TestCase):

    @staticmethod
    def __sample_control_router_conf():
        ip_address = IPv4Address.construct('192.168.1.111')
        port = 21105
        timeout = 1.2
        subsription = ControlRouterSubscription(Broadcast.TRACK, Broadcast.CAN_DETECTOR, Broadcast.X_LOCO_INFO_ALL)

        return ControlRouterConf(ip_address, port, timeout, subsription)


    def test_control_router(self):
        obj1 = self.__sample_control_router_conf()
        self.assertEqual('ControlRouterConf:{ip_address:IPv4Address:{192.168.1.111}, port:21105, timeout:1.2, '
                         'subscription:ControlRouterSubscription:{flags:[CAN_DETECTOR, TRACK, X_LOCO_INFO_ALL]}}',
                         str(obj1))


    def test_control_router_json(self):
        obj1 = self.__sample_control_router_conf()
        jstr = JSONify.dumps(obj1)
        self.assertEqual('{"ip_address": "192.168.1.111", "port": 21105, "timeout": 1.2, '
                         '"subscription": {"flags": ["CAN_DETECTOR", "TRACK", "X_LOCO_INFO_ALL"]}}',
                         jstr)


    def test_control_router_json_eq(self):
        obj1 = self.__sample_control_router_conf()
        jstr = JSONify.dumps(obj1)
        obj2 = ControlRouterConf.construct_from_jdict(json.loads(jstr))
        self.assertEqual(obj1, obj2)


    def test_control_router_json_persistence(self):
        obj1 = self.__sample_control_router_conf()
        obj1.save(Host)
        obj2 = ControlRouterConf.load(Host)
        self.assertEqual(obj1, obj2)


# --------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    unittest.main()
