"""
Created on 15 Nov 2025

@author: Bruno Beloff (bbeloff@me.com)

python -m unittest -v messaging/test_queue.py

https://realpython.com/python-testing/
https://www.jetbrains.com/help/pycharm/creating-tests.html
https://stackoverflow.com/questions/8047736/how-to-load-data-from-a-file-for-a-unit-test-in-python
"""

import json
import os
import unittest

from mrcs_core.data.json import JSONify
from mrcs_core.messaging.queue import Queue


# --------------------------------------------------------------------------------------------------------------------

class TestQueue(unittest.TestCase):
    __filename1 = os.path.join(os.path.dirname(__file__), 'data', 'rabbitmq_queue1.json')
    with open(__filename1) as fp:
        __jdict1 = json.load(fp)

    __filename2 = os.path.join(os.path.dirname(__file__), 'data', 'rabbitmq_queue2.json')
    with open(__filename2) as fp:
        __jdict2 = json.load(fp)

    def test_construct_from_jdict(self):
        obj1 = Queue.construct_from_jdict(self.__jdict1)
        self.assertEqual('Queue:{name:log_receiver_695, queue_type:classic, durable:False, exclusive:True, '
                         'state:running, consumers:1, messages:0, messages_ready:0, messages_unacknowledged:0}',
                         str(obj1))

    def test_construct_from_none(self):
        obj1 = Queue.construct_from_jdict(None)
        self.assertEqual(None, obj1)

    def test_eq(self):
        obj1 = Queue.construct_from_jdict(self.__jdict1)
        obj2 = Queue.construct_from_jdict(self.__jdict1)
        self.assertEqual(True, obj1 == obj2)

    def test_neq(self):
        obj1 = Queue.construct_from_jdict(self.__jdict1)
        obj2 = Queue.construct_from_jdict(self.__jdict2)
        self.assertEqual(False, obj1 == obj2)

    def test_lt(self):
        obj1 = Queue.construct_from_jdict(self.__jdict1)
        obj2 = Queue.construct_from_jdict(self.__jdict2)
        self.assertEqual(True, obj1 < obj2)

    def test_nlt(self):
        obj1 = Queue.construct_from_jdict(self.__jdict2)
        obj2 = Queue.construct_from_jdict(self.__jdict1)
        self.assertEqual(False, obj1 < obj2)

    def test_as_json(self):
        obj1 = Queue.construct_from_jdict(self.__jdict1)
        self.assertEqual('{"name": "log_receiver_695", "type": "classic", "durable": false, "exclusive": true, '
                         '"state": "running", "consumers": 1, "messages": 0, "messages_ready": 0, '
                         '"messages_unacknowledged": 0}', JSONify.dumps(obj1))


if __name__ == "__main_":
    unittest.main()
