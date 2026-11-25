"""
Created on 20 Nov 2026

@author: Bruno Beloff (bbeloff@me.com)

python -m unittest -v unit/operations/alert/test_alert_command.py

https://realpython.com/python-testing/
https://www.jetbrains.com/help/pycharm/creating-tests.html
"""

import json
import unittest

from mrcs_core.data.json import JSONify
from mrcs_core.operations.alert.alert_command import AlertCommand


# --------------------------------------------------------------------------------------------------------------------

class TestAlertCommand(unittest.TestCase):

    # --------------------------------------------------------------------------------------------------------------------
    # construct_RESOLVE

    def test_construct_RESOLVE(self):
        obj1 = AlertCommand.construct_RESOLVE(1, response_required=False)
        self.assertEqual('AlertCommand:{action:RESOLVE, response_required:False, kwargs:{id: 1}}', str(obj1))


    def test_kwarg(self):
        obj1 = AlertCommand.construct_RESOLVE(1, response_required=False)
        self.assertEqual(1, obj1.kwarg('id'))


    def test_json(self):
        obj1 = AlertCommand.construct_RESOLVE(1, response_required=False)
        jstr = JSONify.dumps(obj1)
        self.assertEqual('{"type": "AlertCommand", "action": "RESOLVE", "response_required": false, '
                         '"kwargs": {"id": 1}}', jstr)


    def test_json_eq(self):
        obj1 = AlertCommand.construct_RESOLVE(1, response_required=False)
        jstr = JSONify.dumps(obj1)
        obj2 = AlertCommand.construct_from_jdict(json.loads(jstr))
        self.assertTrue(obj1 == obj2)


    # --------------------------------------------------------------------------------------------------------------------
    # construct others

    def test_construct_RESOLVE_ALL(self):
        obj1 = AlertCommand.construct_RESOLVE_ALL(response_required=False)
        self.assertEqual('AlertCommand:{action:RESOLVE_ALL, response_required:False, kwargs:{}}', str(obj1))


    def test_construct_LIST_UNRESOLVED(self):
        obj1 = AlertCommand.construct_LIST_UNRESOLVED(response_required=False)
        self.assertEqual('AlertCommand:{action:LIST_UNRESOLVED, response_required:False, kwargs:{}}', str(obj1))


    def test_construct_LIST_RESOLVED(self):
        obj1 = AlertCommand.construct_LIST_LATEST(10, response_required=False)
        self.assertEqual('AlertCommand:{action:LIST_LATEST, response_required:False, kwargs:{limit: 10}}', str(obj1))


    def test_construct_CLEAR_RESOLVED(self):
        obj1 = AlertCommand.construct_DELETE_RESOLVED()
        self.assertEqual('AlertCommand:{action:DELETE_RESOLVED, response_required:True, kwargs:{}}', str(obj1))


# --------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    unittest.main()
