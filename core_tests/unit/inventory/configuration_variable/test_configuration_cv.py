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
from mrcs_core.inventory.configuration_variable.configuration_cv import ConfigurationCV
from mrcs_core.inventory.configuration_variable.cv_address import CVAddress


# --------------------------------------------------------------------------------------------------------------------

class TestConfigurationCV(unittest.TestCase):

    def test_configuration_cv_construct(self):
        obj1 = ConfigurationCV(CVAddress.CONFIGURATION, False, True, False, True,
                               False, False, False)
        self.assertEqual('ConfigurationCV{cv_address:CONFIGURATION{29}, reverse:False, speed_128:True, '
                         'analog_enabled:False, railcom_enabled:True, speed_curve:False, long_address:False, '
                         'accessory_decoder:False}', str(obj1))


    def test_configuration_cv_construct_from_report(self):
        self.maxDiff = None
        obj1 = CVReport(29, 0x06)
        obj2 = ConfigurationCV.construct_from_report(obj1)
        self.assertEqual('ConfigurationCV{cv_address:CONFIGURATION{29}, reverse:False, speed_128:True, '
                         'analog_enabled:True, railcom_enabled:False, speed_curve:False, long_address:False, '
                         'accessory_decoder:False}', str(obj2))


    def test_configuration_cv_report_roundtrip(self):
        obj1 = CVReport(29, 0x12)
        obj2 = ConfigurationCV.construct_from_report(obj1)
        obj3 = obj2.as_report()
        self.assertEqual(obj1, obj3)


    def test_configuration_cv_construct_from_report_fail(self):
        obj1 = CVReport(18, 0x83)
        with self.assertRaises(ValueError):
            ConfigurationCV.construct_from_report(obj1)


    def test_configuration_cv_value(self):
        obj1 = CVReport(29, 0x12)
        obj2 = ConfigurationCV.construct_from_report(obj1)
        self.assertEqual(0x12, obj2.value)


    def test_configuration_cv_json(self):
        obj1 = ConfigurationCV(CVAddress.CONFIGURATION, False, True, False, True,
                               False, False, False)
        obj2 = JSONify.dumps(obj1)
        self.assertEqual('{"type": "ConfigurationCV", "addr": "CONFIGURATION", "reverse": false, '
                         '"speed_128": true, "analog_enabled": false, "railcom_enabled": true, "speed_curve": false, '
                         '"long_address": false, "accessory_decoder": false}', str(obj2))


    def test_cv_json_roundtrip(self):
        obj1 = ConfigurationCV(CVAddress.CONFIGURATION, False, True, False, True,
                               False, False, False)
        obj2 = JSONify.dumps(obj1)
        obj3 = ConfigurationCV.construct_from_jdict(json.loads(obj2))
        self.assertEqual(obj1, obj3)
