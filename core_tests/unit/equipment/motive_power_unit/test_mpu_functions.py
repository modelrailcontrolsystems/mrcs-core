"""
Created on 5 Jul 2026

@author: Bruno Beloff (bbeloff@me.com)

python -m unittest -v unit/equipment/motive_power_unit/test_mpu_functions.py

https://realpython.com/python-testing/
https://www.jetbrains.com/help/pycharm/creating-tests.html
"""

import json
import unittest

from mrcs_core.data.json import JSONify
from mrcs_core.equipment.motive_power_unit.mpu_functions import MPUFunctions


# --------------------------------------------------------------------------------------------------------------------

class TestMPUFunctions(unittest.TestCase):

    def test_mpu_status_str(self):
        obj1 = MPUFunctions([True, False, True, False, False, False, False, False])
        self.assertEqual('MPUFunctions:{+-+-----}', str(obj1))


    def test_mpu_status_json(self):
        obj1 = MPUFunctions([True, False, True, False, False, False, False, False])
        jstr = JSONify.dumps(obj1)
        self.assertEqual('"+-+-----"', jstr)


    def test_mpu_status_json_eq(self):
        obj1 = MPUFunctions([True, False, True, False, False, False, False, False])
        jstr = JSONify.dumps(obj1)
        obj2 = MPUFunctions.construct_from_jdict(json.loads(jstr))
        self.assertEqual(obj1, obj2)


# --------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    unittest.main()
