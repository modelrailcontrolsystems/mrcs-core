"""
Created on 10 Oct 2026

@author: Bruno Beloff (bbeloff@me.com)

python -m unittest -v unit/inventory/configuration_variable/test_railcom_cv.py

https://realpython.com/python-testing/
https://www.jetbrains.com/help/pycharm/creating-tests.html
"""

import json
import unittest

from mrcs_core.data.json import JSONify
from mrcs_core.equipment.conviguration_variable.cv_report import CVReport
from mrcs_core.inventory.configuration_variable.cv_address import CVAddress
from mrcs_core.inventory.configuration_variable.railcom_cv import RailcomCV


# --------------------------------------------------------------------------------------------------------------------

class TestRailcomCV(unittest.TestCase):

    def test_railcom_cv_construct(self):
        obj1 = RailcomCV(CVAddress.RAILCOM, True, True, False, False,
                         False, True)
        self.assertEqual('RailcomCV{cv_address:RAILCOM{28}, ch1_broadcast:True, ch2_broadcast:True, '
                         'auto_ch1:False, enable_addr_3l:False, current_limit:False, railcom_login:True}', str(obj1))


    def test_railcom_cv_construct_from_report(self):
        obj1 = CVReport(28, 0x83)
        obj2 = RailcomCV.construct_from_report(obj1)
        self.assertEqual('RailcomCV{cv_address:RAILCOM{28}, ch1_broadcast:True, ch2_broadcast:True, '
                         'auto_ch1:False, enable_addr_3l:False, current_limit:False, railcom_login:True}', str(obj2))


    def test_railcom_cv_report_roundtrip(self):
        obj1 = CVReport(28, 0x83)
        obj2 = RailcomCV.construct_from_report(obj1)
        obj3 = obj2.as_report()
        self.assertEqual(obj1, obj3)


    def test_railcom_cv_construct_from_report_fail(self):
        obj1 = CVReport(18, 0x83)
        with self.assertRaises(ValueError):
            RailcomCV.construct_from_report(obj1)


    def test_railcom_cv_value(self):
        obj1 = CVReport(28, 0x83)
        obj2 = RailcomCV.construct_from_report(obj1)
        self.assertEqual(0x83, obj2.value)


    def test_railcom_cv_json(self):
        obj1 = RailcomCV(CVAddress.RAILCOM, True, True, False, False,
                         False, True)
        obj2 = JSONify.dumps(obj1)
        self.assertEqual('{"type": "RailcomCV", "addr": "RAILCOM", "ch1_broadcast": true, "ch2_broadcast": true, '
                         '"auto_ch1": false, "enable_addr_3l": false, "current_limit": false, "railcom_login": true}',
                         str(obj2))


    def test_cv_json_roundtrip(self):
        obj1 = RailcomCV(CVAddress.RAILCOM, True, True, False, False,
                         False, True)
        obj2 = JSONify.dumps(obj1, indent=4)
        obj3 = RailcomCV.construct_from_jdict(json.loads(obj2))
        self.assertEqual(obj1, obj3)
