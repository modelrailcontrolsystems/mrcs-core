"""
Created on 15 Nov 2025

@author: Bruno Beloff (bbeloff@me.com)

python -m unittest -v data/test_equipment_filter.py

https://realpython.com/python-testing/
https://www.jetbrains.com/help/pycharm/creating-tests.html
"""

import json
import unittest

from mrcs_core.data.equipment_identity import EquipmentFilter


# --------------------------------------------------------------------------------------------------------------------

class TestEquipmentFilter(unittest.TestCase):
    def test_construct_from_none_jdict(self):
        obj1 = EquipmentFilter.construct_from_jdict({})
        self.assertEqual(None, obj1)

    def test_construct_from_jdict(self):
        obj1 = EquipmentFilter.construct_from_jdict(json.loads('"SBO.01.*"'))
        self.assertEqual('EquipmentFilter:{equipment_type:SBO, sector_number:1, serial_number:None}', str(obj1))

    def test_eq(self):
        obj1 = EquipmentFilter.construct_from_jdict(json.loads('"SBO.01.*"'))
        obj2 = EquipmentFilter.construct_from_jdict(json.loads('"SBO.01.*"'))
        self.assertEqual(True, obj1 == obj2)

    def test_neq(self):
        obj1 = EquipmentFilter.construct_from_jdict(json.loads('"SBO.01.*"'))
        obj2 = EquipmentFilter.construct_from_jdict(json.loads('"SBO.02.*"'))
        self.assertEqual(False, obj1 == obj2)

    def test_lt(self):
        obj1 = EquipmentFilter.construct_from_jdict(json.loads('"SBO.01.*"'))
        obj2 = EquipmentFilter.construct_from_jdict(json.loads('"SBO.01.01"'))
        self.assertEqual(True, obj1 < obj2)

    def test_nlt(self):
        obj1 = EquipmentFilter.construct_from_jdict(json.loads('"SBO.02.*"'))
        obj2 = EquipmentFilter.construct_from_jdict(json.loads('"SBO.01.*"'))
        self.assertEqual(False, obj1 < obj2)

    def test_as_json(self):
        obj1 = EquipmentFilter.construct_from_jdict(json.loads('"SBO.01.*"'))
        self.assertEqual('SBO.001.*', obj1.as_json())


if __name__ == "__main_":
    unittest.main()
