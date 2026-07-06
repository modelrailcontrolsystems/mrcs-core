"""
Created on 6 Jun 2026

@author: Bruno Beloff (bbeloff@me.com)

python -m unittest -v unit/equipment/motive_power_unit/test_mpu_configuration_report.py

https://realpython.com/python-testing/
https://www.jetbrains.com/help/pycharm/creating-tests.html
"""

import json
import unittest

from mrcs_core.data.json import JSONify
from mrcs_core.equipment.motive_power_unit.mpu_functions import MPUFunctions
from mrcs_core.equipment.motive_power_unit.mpu_status import MPUStatus


# --------------------------------------------------------------------------------------------------------------------

class TestMPUStatus(unittest.TestCase):

    @staticmethod
    def __sample_mpu_status():
        label = 'EMR Class 08'
        address = 3
        functions = MPUFunctions([True, False, True])
        speed_setting = 12
        speed = 7
        reverse = True

        return MPUStatus(label, address, functions, speed_setting, speed, reverse)


    def test_mpu_status_str(self):
        obj1 = self.__sample_mpu_status()
        self.assertEqual('MPUStatus:{label:EMR Class 08, address:3, functions:+-+, '
                         'speed_setting:12, speed:7, reverse:True}', str(obj1))


    def test_mpu_status_json(self):
        obj1 = self.__sample_mpu_status()
        jstr = JSONify.dumps(obj1)
        self.assertEqual('{"type": "MPUStatus", "label": "EMR Class 08", "addr": 3, "functions": "+-+", '
                         '"speed_setting": 12, "speed": 7, "reverse": true}', jstr)


    def test_mpu_status_json_eq(self):
        obj1 = self.__sample_mpu_status()
        jstr = JSONify.dumps(obj1)
        obj2 = MPUStatus.construct_from_jdict(json.loads(jstr))
        self.assertEqual(obj1, obj2)


    def test_mpu_status_json_lt(self):
        obj1 = self.__sample_mpu_status()
        jstr = JSONify.dumps(obj1)
        obj2 = MPUStatus.construct_from_jdict(json.loads(jstr))
        self.assertFalse(obj1 < obj2)


# --------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    unittest.main()
