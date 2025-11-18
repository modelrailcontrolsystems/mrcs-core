"""
Created on 16 Nov 2025

@author: Bruno Beloff (bbeloff@me.com)

python -m unittest -v operations/message/test_message_persistence.py

https://realpython.com/python-testing/
https://www.jetbrains.com/help/pycharm/creating-tests.html
"""

import json
import unittest

from setup import Setup

from mrcs_core.messaging.message import Message
from mrcs_core.operations.recorder.message_record import MessageRecord


# --------------------------------------------------------------------------------------------------------------------

class TestMessagePersistence(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Setup.dbSetup()

    def test_recreate(self):
        MessageRecord.drop_tables()
        MessageRecord.create_tables()

        records = list(MessageRecord.find_all())
        self.assertEqual(len(records), 0)

    def test_construct(self):
        MessageRecord.drop_tables()
        MessageRecord.create_tables()

        obj1 = Message.construct_from_jdict(json.loads('{"routing": "TST.001.002.MPU.001.100", "body": "hello"}'))
        obj1.save()

        records = list(MessageRecord.find_all())
        obj2 = records[0]

        self.assertEqual(obj2.routing_key, obj1.routing_key)
        self.assertEqual(obj2.body, obj1.body)


if __name__ == "__main_":
    unittest.main()
