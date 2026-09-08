"""
Created on 6 Sep 2026

@author: Bruno Beloff (bbeloff@me.com)

python -m unittest -v unit/equipment/motive_power_unit/test_mpu_aspect.py

https://realpython.com/python-testing/
https://www.jetbrains.com/help/pycharm/creating-tests.html
"""

import json
import unittest

from mrcs_core.data.json import JSONify
from mrcs_core.equipment.block.block_enums import BlockDirection
from mrcs_core.equipment.motive_power_unit.mpu_aspect import MPUAspect


# --------------------------------------------------------------------------------------------------------------------

class TestMPUAspect(unittest.TestCase):

    @staticmethod
    def __sample_mpu_aspect():
        label = 'EMR Class 08'
        mpu_address = 3
        speed = 7
        direction = BlockDirection.UP
        location = 120

        return MPUAspect(label, mpu_address, speed, direction, location)


    def test_mpu_aspect_str(self):
        obj1 = self.__sample_mpu_aspect()
        self.assertEqual('MPUAspect:{label:EMR Class 08, mpu_address:3, '
                         'speed:7, direction:UP{1}, location:120}', str(obj1))


    def test_mpu_aspect_json(self):
        obj1 = self.__sample_mpu_aspect()
        jstr = JSONify.dumps(obj1)
        self.assertEqual('{"type": "MPUAspect", "label": "EMR Class 08", "addr": 3, '
                         '"speed": 7, "direction": "UP", "location": 120}', jstr)


    def test_mpu_aspect_json_eq(self):
        obj1 = self.__sample_mpu_aspect()
        jstr = JSONify.dumps(obj1)
        obj2 = MPUAspect.construct_from_jdict(json.loads(jstr))
        self.assertEqual(obj1, obj2)


    def test_mpu_aspect_json_lt(self):
        obj1 = self.__sample_mpu_aspect()
        jstr = JSONify.dumps(obj1)
        obj2 = MPUAspect.construct_from_jdict(json.loads(jstr))
        self.assertFalse(obj1 < obj2)


# --------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    unittest.main()
