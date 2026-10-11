"""
Created on 4 Oct 2026

@author: Bruno Beloff (bbeloff@me.com)

python -m unittest -v unit/inventory/motive_power_unit/test_mpu.py

https://realpython.com/python-testing/
https://www.jetbrains.com/help/pycharm/creating-tests.html
"""

import json
import unittest
from typing import OrderedDict

from mrcs_core.data.json import JSONify
from mrcs_core.inventory.configuration_variable.cv_address import CVAddress
from mrcs_core.inventory.configuration_variable.numeric_cv import NumericCV
from mrcs_core.inventory.motive_power_unit.mpu import MPU


# --------------------------------------------------------------------------------------------------------------------

class TestMPU(unittest.TestCase):

    @staticmethod
    def __sample_mpu(address: int):
        cv1 = NumericCV(CVAddress.ACCELERATION, 5)
        cv2 = NumericCV(CVAddress.DECELERATION, 9)
        cvs = OrderedDict({cv1.cv_address: cv1, cv2.cv_address: cv2})
        return MPU('DB59', address, 'DB Schenker', '59', '59201',
                   'Revolution Trains', 145, cvs)


    def test_mpu_construct(self):
        obj1 = self.__sample_mpu(5)
        self.assertEqual('MPU:{label:DB59, address:5, operator:DB Schenker, mpu_class:59, number:59201, '
                         'vendor:Revolution Trains, length:145, cvs:[NumericCV{cv_address:ACCELERATION{3}, value:5}, '
                         'NumericCV{cv_address:DECELERATION{4}, value:9}]}', str(obj1))


    def test_mpu_eq(self):
        obj1 = self.__sample_mpu(5)
        obj2 = self.__sample_mpu(5)
        self.assertTrue(obj1 == obj2)


    def test_mpu_lt(self):
        obj1 = self.__sample_mpu(5)
        obj2 = self.__sample_mpu(6)
        self.assertTrue(obj1 < obj2)


    def test_mpu_cv(self):
        obj1 = self.__sample_mpu(5)
        obj2 = obj1.cv(CVAddress.DECELERATION)
        self.assertEqual('NumericCV{cv_address:DECELERATION{4}, value:9}', str(obj2))


    def test_mpu_json(self):
        obj1 = self.__sample_mpu(5)
        jstr = JSONify.dumps(obj1)
        self.assertEqual('{"label": "DB59", "addr": 5, "operator": "DB Schenker", "class": "59", '
                         '"number": "59201", "vendor": "Revolution Trains", "length": 145, '
                         '"cvs": [{"type": "NumericCV", "addr": "ACCELERATION", "value": 5}, '
                         '{"type": "NumericCV", "addr": "DECELERATION", "value": 9}]}', jstr)


    def test_mpu_json_roundtrip(self):
        obj1 = self.__sample_mpu(5)
        jstr = JSONify.dumps(obj1)
        obj2 = MPU.construct_from_jdict(json.loads(jstr))
        self.assertEqual(obj1, obj2)


    def test_mpu_status(self):
        obj1 = self.__sample_mpu(5)
        obj2 = obj1.mpu_status()
        self.assertEqual('MPUStatus:{label:DB59, mpu_address:5, functions:, speed_setting:None, speed:None, '
                         'direction:UNKNOWN{2}}', str(obj2))
