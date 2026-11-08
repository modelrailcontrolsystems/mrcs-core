"""
Created on 7 Nov 2026

@author: Bruno Beloff (bbeloff@me.com)

python -m unittest -v unit/inventory/configuration_variable/test_manufacturer_cv.py

https://realpython.com/python-testing/
https://www.jetbrains.com/help/pycharm/creating-tests.html
"""

import json
import unittest

from mrcs_core.data.json import JSONify
from mrcs_core.equipment.conviguration_variable.cv_report import CVReport
from mrcs_core.inventory.configuration_variable.cv_address import CVAddress
from mrcs_core.inventory.configuration_variable.manufacturer_cv import ManufacturerCV
from mrcs_core.inventory.motive_power_unit.manufacturer import Manufacturer


# --------------------------------------------------------------------------------------------------------------------

class TestManufacturerCV(unittest.TestCase):

    def test_manufacturer_cv_construct(self):
        obj1 = ManufacturerCV(CVAddress.MANUFACTURER_ID, Manufacturer.ZIMO_ELEKTRONIK)
        self.assertEqual('ManufacturerCV{cv_address:MANUFACTURER_ID{8}, manufacturer:ZIMO_ELEKTRONIK{145}}',
                         str(obj1))


    def test_manufacturer_cv_value(self):
        obj1 = ManufacturerCV(CVAddress.MANUFACTURER_ID, Manufacturer.ZIMO_ELEKTRONIK)
        self.assertEqual(145, obj1.value)


    def test_manufacturer_cv_is_not_writeable(self):
        obj1 = ManufacturerCV(CVAddress.MANUFACTURER_ID, Manufacturer.ZIMO_ELEKTRONIK)
        self.assertFalse(obj1.is_writeable(None))


    # ----------------------------------------------------------------------------------------------------------------

    def test_manufacturer_cv_eq(self):
        obj1 = ManufacturerCV(CVAddress.MANUFACTURER_ID, Manufacturer.ZIMO_ELEKTRONIK)
        obj2 = ManufacturerCV(CVAddress.MANUFACTURER_ID, Manufacturer.ZIMO_ELEKTRONIK)
        self.assertEqual(obj1, obj2)


    def test_manufacturer_cv_not_eq_manufacturer(self):
        obj1 = ManufacturerCV(CVAddress.MANUFACTURER_ID, Manufacturer.ZIMO_ELEKTRONIK)
        obj2 = ManufacturerCV(CVAddress.MANUFACTURER_ID, Manufacturer.LENZ_ELEKTRONIK_GMBH)
        self.assertNotEqual(obj1, obj2)


    def test_manufacturer_cv_not_eq_other_type(self):
        obj1 = ManufacturerCV(CVAddress.MANUFACTURER_ID, Manufacturer.ZIMO_ELEKTRONIK)
        self.assertNotEqual(obj1, 145)


    # ----------------------------------------------------------------------------------------------------------------

    def test_manufacturer_cv_construct_from_report(self):
        obj1 = CVReport(8, 145)
        obj2 = ManufacturerCV.construct_from_report(obj1)
        self.assertEqual('ManufacturerCV{cv_address:MANUFACTURER_ID{8}, manufacturer:ZIMO_ELEKTRONIK{145}}',
                         str(obj2))


    def test_manufacturer_cv_construct_from_report_unknown_manufacturer(self):
        obj1 = CVReport(8, 250)
        with self.assertRaises(ValueError):
            ManufacturerCV.construct_from_report(obj1)


    def test_manufacturer_cv_construct_from_report_unknown_address(self):
        obj1 = CVReport(99, 145)
        with self.assertRaises(ValueError):
            ManufacturerCV.construct_from_report(obj1)


    def test_manufacturer_cv_report_roundtrip(self):
        obj1 = CVReport(8, 99)
        obj2 = ManufacturerCV.construct_from_report(obj1)
        obj3 = obj2.as_report()
        self.assertEqual(obj1, obj3)


    # ----------------------------------------------------------------------------------------------------------------

    def test_manufacturer_cv_json(self):
        obj1 = ManufacturerCV(CVAddress.MANUFACTURER_ID, Manufacturer.ZIMO_ELEKTRONIK)
        obj2 = JSONify.dumps(obj1)
        self.assertEqual('{"type": "ManufacturerCV", "addr": "MANUFACTURER_ID", "mfr": "ZIMO_ELEKTRONIK"}',
                         str(obj2))


    def test_manufacturer_cv_json_roundtrip(self):
        obj1 = ManufacturerCV(CVAddress.MANUFACTURER_ID, Manufacturer.ZIMO_ELEKTRONIK)
        obj2 = JSONify.dumps(obj1, indent=4)
        obj3 = ManufacturerCV.construct_from_jdict(json.loads(obj2))
        self.assertEqual(obj1, obj3)


    def test_manufacturer_cv_construct_from_jdict_unknown_manufacturer(self):
        jdict = {'type': 'ManufacturerCV', 'addr': 'MANUFACTURER_ID', 'mfr': 'UNKNOWN'}
        with self.assertRaises(KeyError):
            ManufacturerCV.construct_from_jdict(jdict)


    def test_manufacturer_cv_construct_from_jdict_missing_address(self):
        jdict = {'type': 'ManufacturerCV', 'mfr': 'ZIMO_ELEKTRONIK'}
        with self.assertRaises(KeyError):
            ManufacturerCV.construct_from_jdict(jdict)


# --------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    unittest.main()
