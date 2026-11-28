"""
Created on 4 Oct 2026

@author: Bruno Beloff (bbeloff@me.com)

python -m unittest -v unit/inventory/motive_power_unit/test_speed_normalisation.py

https://realpython.com/python-testing/
https://www.jetbrains.com/help/pycharm/creating-tests.html
"""

import json
import unittest

from mrcs_core.data.json import JSONify
from mrcs_core.inventory.motive_power_unit.speed_normalisation import SpeedNormalisation


# --------------------------------------------------------------------------------------------------------------------

class TestSpeedNormalisation(unittest.TestCase):

    def test_normalisation_construct(self):
        obj1 = SpeedNormalisation(0.492, 1.418)
        self.assertEqual('SpeedNormalisation:{slope:0.492, offset:1.418}', str(obj1))


    def test_normalisation_jstr(self):
        obj1 = SpeedNormalisation(0.492, 1.418)
        jstr = JSONify.dumps(obj1)
        self.assertEqual('{"slope": 0.492, "offset": 1.418}', jstr)


    def test_normalisation_jstr_eq(self):
        obj1 = SpeedNormalisation(0.492, 1.418)
        jstr = JSONify.dumps(obj1)
        obj2 = SpeedNormalisation.construct_from_jdict(json.loads(jstr))
        self.assertTrue(obj1 == obj2)


    def test_normalisation_zero(self):
        obj1 = SpeedNormalisation(0.492, 1.418)
        actual = obj1.actual_speed(0)
        self.assertEqual(0, actual)


    def test_normalisation_low(self):
        obj1 = SpeedNormalisation(0.492, 1.418)
        actual = obj1.actual_speed(1)
        self.assertEqual(1.9, actual)


    def test_normalisation_high(self):
        obj1 = SpeedNormalisation(0.492, 1.418)
        actual = obj1.actual_speed(180)
        self.assertEqual(90.0, actual)


# --------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    unittest.main()
