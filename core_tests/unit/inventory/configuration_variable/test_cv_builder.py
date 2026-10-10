"""
Created on 10 Oct 2026

@author: Bruno Beloff (bbeloff@me.com)

python -m unittest -v unit/inventory/configuration_variable/test_cv_builder.py

https://realpython.com/python-testing/
https://www.jetbrains.com/help/pycharm/creating-tests.html
"""

import json
import unittest

from mrcs_core.equipment.conviguration_variable.cv_report import CVReport
from mrcs_core.inventory.configuration_variable.cv_builder import CVBuilder


# --------------------------------------------------------------------------------------------------------------------

class TestCVBuilder(unittest.TestCase):

    def test_cv_builder_report_configuration(self):
        obj1 = CVReport(29, 0x06)
        obj2 = CVBuilder.construct_from_report(obj1)
        self.assertEqual('ConfigurationCV{cv_address:CONFIGURATION{29}, reverse:False, speed_128:True, '
                         'analog_enabled:True, railcom_enabled:False, speed_curve:False, long_address:False, '
                         'accessory_decoder:False}', str(obj2))


    def test_cv_builder_report_consist(self):
        obj1 = CVReport(19, 0x9b)
        obj2 = CVBuilder.construct_from_report(obj1)
        self.assertEqual('ConsistCV{cv_address:CONSIST_ADDRESS{19}, reverse:True, consist_address:27}', str(obj2))


    def test_cv_builder_report_railcom(self):
        obj1 = CVReport(28, 0x83)
        obj2 = CVBuilder.construct_from_report(obj1)
        self.assertEqual('RailcomCV{cv_address:RAILCOM{28}, ch1_broadcast:True, ch2_broadcast:True, '
                         'auto_ch1:False, enable_addr_3l:False, current_limit:False, railcom_login:True}', str(obj2))


    def test_cv_builder_report_numeric(self):
        obj1 = CVReport(3, 5)
        obj2 = CVBuilder.construct_from_report(obj1)
        self.assertEqual('NumericCV{cv_address:ACCELERATION{3}, value:5}', str(obj2))


    def test_cv_builder_report_fail(self):
        obj1 = CVReport(99, 5)
        with self.assertRaises(TypeError):
            CVBuilder.construct_from_report(obj1)


    def test_cv_builder_jdict_configuration(self):
        jstr = ('{"type": "ConfigurationCV", "addr": "CONFIGURATION", "reverse": false, "speed_128": true, '
                '"analog_enabled": false, "railcom_enabled": true, "speed_curve": false, "long_address": false, '
                '"accessory_decoder": false}')
        obj1 = CVBuilder.construct_from_jdict(json.loads(jstr))
        self.assertEqual('ConfigurationCV{cv_address:CONFIGURATION{29}, reverse:False, speed_128:True, '
                         'analog_enabled:False, railcom_enabled:True, speed_curve:False, long_address:False, '
                         'accessory_decoder:False}', str(obj1))


    def test_cv_builder_jdict_consist(self):
        jstr = '{"type": "ConsistCV", "addr": "CONSIST_ADDRESS", "reverse": true, "consist_address": 27}'
        obj1 = CVBuilder.construct_from_jdict(json.loads(jstr))
        self.assertEqual('ConsistCV{cv_address:CONSIST_ADDRESS{19}, reverse:True, consist_address:27}', str(obj1))


    def test_cv_builder_jdict_numeric(self):
        jstr = '{"type": "NumericCV", "addr": "ACCELERATION", "value": 5}'
        obj1 = CVBuilder.construct_from_jdict(json.loads(jstr))
        self.assertEqual('NumericCV{cv_address:ACCELERATION{3}, value:5}', str(obj1))


    def test_cv_builder_jdict_railcom(self):
        jstr = ('{"type": "RailcomCV", "addr": "RAILCOM", "ch1_broadcast": true, "ch2_broadcast": true, '
                '"auto_ch1": false, "enable_addr_3l": false, "current_limit": false, "railcom_login": true}')
        obj1 = CVBuilder.construct_from_jdict(json.loads(jstr))
        self.assertEqual('RailcomCV{cv_address:RAILCOM{28}, ch1_broadcast:True, ch2_broadcast:True, '
                         'auto_ch1:False, enable_addr_3l:False, current_limit:False, railcom_login:True}', str(obj1))


    def test_cv_builder_jdict_fail(self):
        jstr = '{"type": "UnknownCV", "addr": "ACCELERATION", "value": 5}'
        with self.assertRaises(TypeError):
            CVBuilder.construct_from_jdict(json.loads(jstr))
