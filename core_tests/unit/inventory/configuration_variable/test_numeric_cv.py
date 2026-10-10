"""
Created on 10 Oct 2026

@author: Bruno Beloff (bbeloff@me.com)

python -m unittest -v unit/inventory/configuration_variable/test_numeric_cv_address.py

https://realpython.com/python-testing/
https://www.jetbrains.com/help/pycharm/creating-tests.html
"""

import json
import unittest

from mrcs_core.data.json import JSONify
from mrcs_core.equipment.conviguration_variable.cv_report import CVReport
from mrcs_core.inventory.configuration_variable.cv_address import CVAddress
from mrcs_core.inventory.configuration_variable.numeric_cv import NumericCV


# --------------------------------------------------------------------------------------------------------------------

class TestNumericCV(unittest.TestCase):

    def test_numeric_cv_construct(self):
        obj1 = NumericCV(CVAddress.ACCELERATION, 5)
        self.assertEqual('NumericCV{cv_address:ACCELERATION{3}, value:5}', str(obj1))


    def test_numeric_cv_construct_from_report(self):
        obj1 = CVReport(3, 5)
        obj2 = NumericCV.construct_from_report(obj1)
        self.assertEqual('NumericCV{cv_address:ACCELERATION{3}, value:5}', str(obj2))


    def test_numeric_cv_report_roundtrip(self):
        obj1 = CVReport(3, 0x12)
        obj2 = NumericCV.construct_from_report(obj1)
        obj3 = obj2.as_report()
        self.assertEqual(obj1, obj3)


    def test_numeric_cv_json(self):
        obj1 = NumericCV(CVAddress.ACCELERATION, 5)
        obj2 = JSONify.dumps(obj1)
        self.assertEqual('{"type": "NumericCV", "addr": "ACCELERATION", "value": 5}', str(obj2))


    def test_numeric_cv_json_roundtrip(self):
        obj1 = NumericCV(CVAddress.ACCELERATION, 5)
        obj2 = JSONify.dumps(obj1, indent=4)
        obj3 = NumericCV.construct_from_jdict(json.loads(obj2))
        self.assertEqual(obj1, obj3)
