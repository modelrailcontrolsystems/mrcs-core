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


# --------------------------------------------------------------------------------------------------------------------

class TestMessage(unittest.TestCase):
    __filename1 = Path(__file__).parent / 'data' / 'message.json'
    with open(__filename1) as fp:
        __jdict1 = json.load(fp)


    def test_message_construct(self):
        obj1 = Message.construct_from_jdict(self.__jdict1)
        self.assertEqual("Message:{origin:fe6114f0-c054, "
                         "routing_key:PublicationRoutingKey:{source:EquipmentIdentifier:"
                         "{equipment_type:CRT, sector_number:None, serial_number:16}, target:EquipmentFilter:"
                         "{equipment_type:None, sector_number:None, serial_number:None}}, "
                         "body:{'type': 'TurnoutReport', 'addr': 2, 'position': 'P1'}}", str(obj1))


    def test_message_json(self):
        obj1 = Message.construct_from_jdict(self.__jdict1)
        jdict = obj1.as_jdict()
        self.assertEqual(self.__jdict1, jdict)


    def test_message_eq(self):
        obj1 = Message.construct_from_jdict(self.__jdict1)
        self.assertTrue(obj1 == obj1)


    def test_message_lt(self):
        obj1 = Message.construct_from_jdict(self.__jdict1)
        self.assertFalse(obj1 < obj1)


    def test_payload(self):
        obj1 = Message.construct_from_jdict(self.__jdict1)
        payload = obj1.payload
        self.assertEqual(
            "Message.Payload:{origin:fe6114f0-c054, body:{'type': 'TurnoutReport', 'addr': 2, 'position': 'P1'}}",
            str(payload))


    def test_message_construct_callback(self):
        obj1 = Message.construct_from_jdict(self.__jdict1)
        routing = obj1.routing_key
        payload = JSONify.dumps(obj1.payload)
        obj2 = Message.construct_from_callback(routing, payload.encode())
        self.assertEqual("Message:{origin:fe6114f0-c054, "
                         "routing_key:PublicationRoutingKey:{source:EquipmentIdentifier:"
                         "{equipment_type:CRT, sector_number:None, serial_number:16}, target:EquipmentFilter:"
                         "{equipment_type:None, sector_number:None, serial_number:None}}, "
                         "body:{'type': 'TurnoutReport', 'addr': 2, 'position': 'P1'}}", str(obj2))


    def test_payload_json(self):
        obj1 = Message.construct_from_jdict(self.__jdict1)
        payload = obj1.payload
        jdict = payload.as_jdict()
        self.assertEqual(
            "{'origin': 'fe6114f0-c054', 'body': {'type': 'TurnoutReport', 'addr': 2, 'position': 'P1'}}",
            str(jdict))


# --------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    unittest.main()
