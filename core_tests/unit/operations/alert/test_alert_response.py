"""
Created on 20 Nov 2026

@author: Bruno Beloff (bbeloff@me.com)

python -m unittest -v unit/operations/alert/test_alert_response.py

https://realpython.com/python-testing/
https://www.jetbrains.com/help/pycharm/creating-tests.html
"""

import json
import unittest

from mrcs_core.data.json import JSONify
from mrcs_core.operations.alert.alert_action import AlertAction
from mrcs_core.operations.alert.alert_command import AlertCommand
from mrcs_core.operations.alert.alert_response import AlertResponse


# --------------------------------------------------------------------------------------------------------------------

class TestAlertResponse(unittest.TestCase):

    # --------------------------------------------------------------------------------------------------------------------

    def test_construct_error(self):
        obj1 = AlertResponse.construct_error(AlertAction.RESOLVE, Exception('this is an error'))
        self.assertEqual('AlertResponse:{action:RESOLVE, error:Exception: this is an error, payload:None}',
                         str(obj1))


    def test_json_error(self):
        obj1 = AlertResponse.construct_error(AlertAction.RESOLVE, Exception('this is an error'))
        jstr = JSONify.dumps(obj1)
        self.assertEqual('{"type": "AlertResponse", "action": "RESOLVE", "error": "Exception: this is an error"}',
                         jstr)


    def test_json_error_eq(self):
        obj1 = AlertResponse.construct_error(AlertAction.RESOLVE, Exception('this is an error'))
        jstr = JSONify.dumps(obj1)
        obj2 = AlertResponse.construct_from_jdict(json.loads(jstr))
        self.assertTrue(obj1 == obj2)


    def test_error_ack(self):
        obj1 = AlertResponse.construct_error(AlertAction.RESOLVE, Exception('this is an error'))
        self.assertFalse(obj1.is_ACK())


    def test_error_nack(self):
        obj1 = AlertResponse.construct_error(AlertAction.RESOLVE, Exception('this is an error'))
        self.assertTrue(obj1.is_NACK())


    # --------------------------------------------------------------------------------------------------------------------

    def test_construct_payload(self):
        obj1 = AlertResponse(AlertAction.RESOLVE, payload=AlertCommand.construct_DELETE_RESOLVED())
        self.assertEqual('AlertResponse:{action:RESOLVE, error:None, payload:AlertCommand:'
                         '{action:DELETE_RESOLVED, response_required:True, kwargs:{}}}', str(obj1))


    def test_json_payload(self):
        obj1 = AlertResponse(AlertAction.RESOLVE, payload=AlertCommand.construct_DELETE_RESOLVED())
        jstr = JSONify.dumps(obj1)
        self.assertEqual('{"type": "AlertResponse", "action": "RESOLVE", "payload": {"type": "AlertCommand", '
                         '"action": "DELETE_RESOLVED", "response_required": true, "kwargs": {}}}', jstr)


    def test_json_payload_eq(self):
        obj1 = AlertResponse(AlertAction.RESOLVE, payload=JSONify.as_jdict(AlertCommand.construct_DELETE_RESOLVED()))
        jstr = JSONify.dumps(obj1)
        obj2 = AlertResponse.construct_from_jdict(json.loads(jstr))
        self.assertTrue(obj1 == obj2)


    def test_payload_ack(self):
        obj1 = AlertResponse(AlertAction.RESOLVE, payload=AlertCommand.construct_DELETE_RESOLVED())
        self.assertTrue(obj1.is_ACK())


    def test_payload_nack(self):
        obj1 = AlertResponse(AlertAction.RESOLVE, payload=AlertCommand.construct_DELETE_RESOLVED())
        self.assertFalse(obj1.is_NACK())


# --------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    unittest.main()
