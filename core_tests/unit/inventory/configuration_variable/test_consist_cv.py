"""
Created on 10 Oct 2026

@author: Bruno Beloff (bbeloff@me.com)

python -m unittest -v unit/inventory/configuration_variable/test_cv_address.py

https://realpython.com/python-testing/
https://www.jetbrains.com/help/pycharm/creating-tests.html
"""

import json
import unittest

from mrcs_core.data.json import JSONify
from mrcs_core.equipment.conviguration_variable.cv_report import CVReport
from mrcs_core.inventory.configuration_variable.consist_cv import ConsistCV
from mrcs_core.inventory.configuration_variable.cv_address import CVAddress


# --------------------------------------------------------------------------------------------------------------------

class TestConsistCV(unittest.TestCase):

    def test_consist_cv_construct(self):
        obj1 = ConsistCV(CVAddress.CONSIST_ADDRESS, True, 27)
        self.assertEqual('ConsistCV{cv_address:CONSIST_ADDRESS{19}, reverse:True, consist_address:27}', str(obj1))


    def test_consist_cv_construct_from_report(self):
        obj1 = CVReport(19, 0x9b)
        obj2 = ConsistCV.construct_from_report(obj1)
        self.assertEqual('ConsistCV{cv_address:CONSIST_ADDRESS{19}, reverse:True, consist_address:27}', str(obj2))


    def test_consist_cv_construct_from_report_fail(self):
        obj1 = CVReport(18, 0x9b)
        with self.assertRaises(ValueError):
            ConsistCV.construct_from_report(obj1)


    def test_consist_cv_report_roundtrip(self):
        obj1 = CVReport(19, 0x9b)
        obj2 = ConsistCV.construct_from_report(obj1)
        obj3 = obj2.as_report()
        self.assertEqual(obj1, obj3)


    def test_consist_cv_value(self):
        obj1 = CVReport(19, 0x9b)
        obj2 = ConsistCV.construct_from_report(obj1)
        self.assertEqual(0x9b, obj2.value)


    def test_consist_cv_json(self):
        obj1 = ConsistCV(CVAddress.CONSIST_ADDRESS, True, 27)
        obj2 = JSONify.dumps(obj1)
        self.assertEqual('{"type": "ConsistCV", "addr": "CONSIST_ADDRESS", "reverse": true, "consist_address": 27}',
                         str(obj2))


    def test_cv_json_roundtrip(self):
        obj1 = ConsistCV(CVAddress.CONSIST_ADDRESS, True, 27)
        obj2 = JSONify.dumps(obj1, indent=4)
        obj3 = ConsistCV.construct_from_jdict(json.loads(obj2))
        self.assertEqual(obj1, obj3)
