"""
Created on 15 Nov 2025

@author: Bruno Beloff (bbeloff@me.com)

python -m unittest -v messaging/test_message.py

https://realpython.com/python-testing/
https://www.jetbrains.com/help/pycharm/creating-tests.html
"""

import json

import unittest

from mrcs_core.data.json import JSONify
from mrcs_core.messaging.message import Message


# --------------------------------------------------------------------------------------------------------------------

class TestMessage(unittest.TestCase):
    def test_construct_from_jdict(self):
        obj1 = Message.construct_from_jdict(json.loads('{"routing": "TST.001.002.MPU.001.100", "body": "hello"}'))
        self.assertEqual('Message:{routing_key:PublicationRoutingKey:{source:EquipmentIdentifier:'
                         '{equipment_type:TST, sector_number:1, serial_number:2}, '
                         'target:EquipmentFilter:{equipment_type:MPU, sector_number:1, serial_number:100}}, '
                         'body:hello}', str(obj1))

    def test_jdict(self):
        obj1 = Message.construct_from_jdict(json.loads('{"routing": "TST.001.002.MPU.001.100", "body": [1, 2]}'))
        self.assertEqual({'routing': 'TST.001.002.MPU.001.100', 'body': (1, 2)}, obj1.as_jdict())

    def test_eq(self):
        obj1 = Message.construct_from_jdict(json.loads('{"routing": "TST.001.002.MPU.001.100", "body": "hello"}'))
        obj2 = Message.construct_from_jdict(json.loads('{"routing": "TST.001.002.MPU.001.100", "body": "hello"}'))
        self.assertEqual(True, obj1 == obj2)

    def test_neq(self):
        obj1 = Message.construct_from_jdict(json.loads('{"routing": "TST.001.002.MPU.001.100", "body": "hello"}'))
        obj2 = Message.construct_from_jdict(json.loads('{"routing": "TST.001.002.MPU.001.100", "body": "goodbye"}'))
        self.assertEqual(False, obj1 == obj2)

    def test_lt(self):
        obj1 = Message.construct_from_jdict(json.loads('{"routing": "TST.001.002.MPU.001.100", "body": "goodbye"}'))
        obj2 = Message.construct_from_jdict(json.loads('{"routing": "TST.001.002.MPU.001.100", "body": "hello"}'))
        self.assertEqual(True, obj1 < obj2)

    def test_nlt(self):
        obj1 = Message.construct_from_jdict(json.loads('{"routing": "TST.001.002.MPU.001.100", "body": "hello"}'))
        obj2 = Message.construct_from_jdict(json.loads('{"routing": "TST.001.002.MPU.001.100", "body": "goodbye"}'))
        self.assertEqual(False, obj1 < obj2)

    def test_as_db(self):
        obj1 = Message.construct_from_jdict(json.loads('{"routing": "TST.001.002.MPU.001.100", "body": "hello"}'))
        self.assertEqual(('TST.001.002.MPU.001.100', '"hello"'), obj1.as_db())

    def test_as_json(self):
        obj1 = Message.construct_from_jdict(json.loads('{"routing": "TST.001.002.MPU.001.100", "body": "hello"}'))
        self.assertEqual('{"routing": "TST.001.002.MPU.001.100", "body": "hello"}', JSONify.dumps(obj1))


if __name__ == "__main_":
    unittest.main()
