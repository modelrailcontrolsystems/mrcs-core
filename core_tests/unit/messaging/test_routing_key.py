"""
Created on 16 Aug 2026

@author: Bruno Beloff (bbeloff@me.com)

python -m unittest -v unit/messaging/test_message.py

https://realpython.com/python-testing/
https://www.jetbrains.com/help/pycharm/creating-tests.html
"""

import json
import unittest
from pathlib import Path

from mrcs_core.data.json import JSONify
from mrcs_core.messaging.message import Message
from mrcs_core.messaging.routing_key import PublicationRoutingKey


# --------------------------------------------------------------------------------------------------------------------

class TestRoutingKey(unittest.TestCase):
    __filename1 = Path(__file__).parent / 'data' / 'message.json'
    with open(__filename1) as fp:
        __jdict1 = json.load(fp)


    def test_routing_construct(self):
        obj1 = Message.construct_from_jdict(self.__jdict1)
        obj2 = obj1.routing_key
        self.assertEqual(
            "PublicationRoutingKey:{source:EquipmentIdentifier:{equipment_type:CRT, sector_number:None, "
            "serial_number:16}, target:EquipmentFilter:{equipment_type:None, sector_number:None, serial_number:None}}",
            str(obj2))


    def test_routing_json(self):
        obj1 = Message.construct_from_jdict(self.__jdict1)
        obj2 = obj1.routing_key
        self.assertEqual('"CRT.*.016.*.*.*"', str(JSONify.dumps(obj2)))


    def test_routing_eq(self):
        obj1 = Message.construct_from_jdict(self.__jdict1)
        obj2 = obj1.routing_key
        self.assertTrue(obj2 == obj2)


    def test_routing_lt(self):
        obj1 = Message.construct_from_jdict(self.__jdict1)
        obj2 = obj1.routing_key
        self.assertFalse(obj2 < obj2)


    def test_routing_valid(self):
        self.assertTrue(PublicationRoutingKey.is_valid('CRT.*.016.*.*.*'))


    def test_routing_not_valid(self):
        self.assertFalse(PublicationRoutingKey.is_valid('CRT.*.016.*.*'))


# --------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    unittest.main()
