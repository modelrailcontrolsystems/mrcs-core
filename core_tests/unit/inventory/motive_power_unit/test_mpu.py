"""
Created on 4 Oct 2026

@author: Bruno Beloff (bbeloff@me.com)

python -m unittest -v unit/inventory/motive_power_unit/test_mpu.py

https://realpython.com/python-testing/
https://www.jetbrains.com/help/pycharm/creating-tests.html
"""

import json
import unittest

from mrcs_core.data.json import JSONify
from mrcs_core.inventory.motive_power_unit.mpu import MPU


# --------------------------------------------------------------------------------------------------------------------

class TestMPU(unittest.TestCase):

    def test_mpu_construct(self):
        obj1 = MPU('lab1', 1, 'DB', '59', '593456', 'Revolution', 15)
        self.assertEqual('MPU:{label:lab1, address:1, operator:DB, mpu_class:59, number:593456, '
                         'vendor:Revolution, length:15}', str(obj1))


    def test_mpu_eq(self):
        obj1 = MPU('lab1', 1, 'DB', '59', '593456', 'Revolution', 15)
        obj2 = MPU('lab1', 1, 'DB', '59', '593456', 'Revolution', 15)
        self.assertTrue(obj1 == obj2)


    def test_mpu_lt(self):
        obj1 = MPU('lab1', 1, 'DB', '59', '593456', 'Revolution', 15)
        obj2 = MPU('lab1', 2, 'DB', '59', '593456', 'Revolution', 15)
        self.assertTrue(obj1 < obj2)


    def test_mpu_json(self):
        obj1 = MPU('lab1', 1, 'DB', '59', '593456', 'Revolution', 15)
        jstr = JSONify.dumps(obj1)
        self.assertEqual('{"label": "lab1", "addr": 1, "operator": "DB", "class": "59", "number": "593456", '
                         '"vendor": "Revolution", "length": 15}', jstr)


    def test_mpu_json_roundtrip(self):
        obj1 = MPU('lab1', 1, 'DB', '59', '593456', 'Revolution', 15)
        jstr = JSONify.dumps(obj1)
        obj2 = MPU.construct_from_jdict(json.loads(jstr))
        self.assertEqual(obj1, obj2)


    def test_mpu_status(self):
        obj1 = MPU('lab1', 1, 'DB', '59', '593456', 'Revolution', 15)
        obj2 = obj1.mpu_status()
        self.assertEqual('MPUStatus:{label:lab1, mpu_address:1, functions:, speed_setting:None, speed:None, '
                         'direction:UNKNOWN{2}}', str(obj2))
