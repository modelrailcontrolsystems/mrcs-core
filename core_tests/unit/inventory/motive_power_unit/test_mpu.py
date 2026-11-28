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
from mrcs_core.data.scale import Scale
from mrcs_core.inventory.configuration_variable.cv_address import CVAddress
from mrcs_core.inventory.configuration_variable.types.cv import CV
from mrcs_core.inventory.configuration_variable.types.manufacturer_cv import ManufacturerCV
from mrcs_core.inventory.configuration_variable.types.numeric_cv import NumericCV
from mrcs_core.inventory.manufacturer.manufacturer import Manufacturer
from mrcs_core.inventory.motive_power_unit.mpu import MPU
from mrcs_core.inventory.motive_power_unit.speed_normalisation import SpeedNormalisation


# --------------------------------------------------------------------------------------------------------------------

class TestMPU(unittest.TestCase):

    @staticmethod
    def __sample_mpu(address: int):
        normalisation = SpeedNormalisation(0.492, 1.418)
        cv1 = NumericCV(CVAddress.ACCELERATION, 5)
        cv2 = NumericCV(CVAddress.DECELERATION, 9)
        cv3 = ManufacturerCV(CVAddress.MANUFACTURER_ID, Manufacturer.ZIMO_ELEKTRONIK)
        cvs: OrderedDict[CVAddress, CV] = OrderedDict({cv1.address: cv1,
                                                       cv2.address: cv2, cv3.address: cv3})
        return MPU('DB59', address, 'DB Schenker', '59', '59201',
                   'Revolution Trains', Scale.N, 145, normalisation, cvs)


    def test_mpu_construct(self):
        self.maxDiff = None
        obj1 = self.__sample_mpu(5)
        self.assertEqual('MPU:{label:DB59, address:5, operator:DB Schenker, mpu_class:59, number:59201, '
                         'manufacturer:Revolution Trains, scale:N{148}, length:145, normalisation:SpeedNormalisation:'
                         '{slope:0.492, offset:1.418}, cvs:[NumericCV{address:ACCELERATION{3}, value:5}, '
                         'NumericCV{address:DECELERATION{4}, value:9}, ManufacturerCV{address:MANUFACTURER_ID{8}, '
                         'manufacturer:ZIMO_ELEKTRONIK{145}}]}', str(obj1))


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
        self.assertEqual('NumericCV{address:DECELERATION{4}, value:9}', str(obj2))


    def test_mpu_json(self):
        self.maxDiff = None
        obj1 = self.__sample_mpu(5)
        jstr = JSONify.dumps(obj1)
        self.assertEqual('{"label": "DB59", "addr": 5, "operator": "DB Schenker", "class": "59", '
                         '"number": "59201", "manufacturer": "Revolution Trains", "scale": "N", "length": 145, '
                         '"normalisation": {"slope": 0.492, "offset": 1.418}, "cvs": [{"type": "NumericCV", '
                         '"addr": "ACCELERATION", "value": 5}, {"type": "NumericCV", "addr": "DECELERATION", '
                         '"value": 9}, {"type": "ManufacturerCV", "addr": "MANUFACTURER_ID", '
                         '"mfr": "ZIMO_ELEKTRONIK"}]}', jstr)


    def test_mpu_json_roundtrip(self):
        obj1 = self.__sample_mpu(5)
        jstr = JSONify.dumps(obj1)
        obj2 = MPU.construct_from_jdict(json.loads(jstr))
        self.assertEqual(obj1, obj2)


    def test_mpu_status(self):
        obj1 = self.__sample_mpu(5)
        obj2 = obj1.mpu_status()
        self.assertEqual('MPUStatus:{label:DB59, mpu_address:5, functions:, speed_setting:None, '
                         'reported_speed:None, actual_speed:None, direction:UNKNOWN{2}}', str(obj2))


    def test_mpu_decoder(self):
        obj1 = self.__sample_mpu(5)
        decoder = obj1.decoder()
        self.assertEqual('ZIMO_ELEKTRONIK{145}', str(decoder))


    def test_actual_speed(self):
        obj1 = self.__sample_mpu(5)
        actual_speed = obj1.actual_speed(50)
        self.assertEqual(26.0, actual_speed)


# --------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    unittest.main()
