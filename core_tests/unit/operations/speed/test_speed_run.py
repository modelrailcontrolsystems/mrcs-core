"""
Created on 25 Oct 2025

@author: Bruno Beloff (bbeloff@me.com)

python -m unittest -v unit/operations/speed/test_speed_run.py

https://realpython.com/python-testing/
https://www.jetbrains.com/help/pycharm/creating-tests.html
https://stackoverflow.com/questions/8047736/how-to-load-data-from-a-file-for-a-unit-test-in-python
"""

import json
import time
import unittest

from mrcs_core.data.iso_datetime import ISODatetime
from mrcs_core.data.json import JSONify
from mrcs_core.equipment.block.block_enums import BlockHeading
from mrcs_core.operations.speed.speed_log import SpeedLog
from mrcs_core.operations.speed.speed_run import SpeedRun


# --------------------------------------------------------------------------------------------------------------------

class TestSpeedRun(unittest.TestCase):

    @classmethod
    def __sample_run_1(cls):
        now = ISODatetime.construct_from_jdict('2026-10-25T08:55:38.234Z')
        return SpeedRun(500, BlockHeading.UP, 5, 12.125, 17.123, now)


    @classmethod
    def __sample_run_2(cls):
        now = ISODatetime.construct_from_jdict('2026-10-25T08:55:38.234Z')
        return SpeedRun(500, BlockHeading.UP, 4, 12.125, 17.123, now)


    @classmethod
    def __sample_run_3(cls):
        now = ISODatetime.construct_from_jdict('2026-10-25T08:55:38.235Z')
        return SpeedRun(500, BlockHeading.UP, 5, 12.125, 17.123, now)


    # ----------------------------------------------------------------------------------------------------------------

    def test_construct(self):
        obj1 = self.__sample_run_1()
        self.assertEqual('SpeedRun:{distance:500, direction:UP{1}, set_speed:5, average_reported_speed:12.1, '
                         'elapsed_time:17.123, test_time:ISODatetime:{2026-10-25T08:55:38.234+00:00}}', str(obj1))


    def test_eq(self):
        obj1 = self.__sample_run_1()
        obj2 = self.__sample_run_1()
        self.assertTrue(obj1 == obj2)


    def test_lt_1(self):
        obj1 = self.__sample_run_1()
        obj2 = self.__sample_run_2()
        self.assertFalse(obj1 < obj2)


    def test_lt_2(self):
        obj1 = self.__sample_run_1()
        obj2 = self.__sample_run_3()
        self.assertTrue(obj1 < obj2)


    def test_json(self):
        obj1 = self.__sample_run_1()
        self.assertEqual('{"distance": 500, "direction": "UP", "set": 5, "ars": 12.1, "elapsed": 17.123, '
                         '"test_time": "2026-10-25T08:55:38.234+00:00"}', JSONify.dumps(obj1))


    def test_json_eq(self):
        obj1 = self.__sample_run_1()
        jstr = JSONify.dumps(obj1)
        obj2 = SpeedRun.construct_from_jdict(json.loads(jstr))
        self.assertTrue(obj1 == obj2)


    def test_actual_speed(self):
        obj1 = self.__sample_run_1()
        self.assertEqual(0.029, obj1.actual_speed)


    def test_construct_from_log(self):
        obj1 = SpeedLog.start()
        time.sleep(1)
        obj1.mark(30)
        obj2 = SpeedRun.construct(500, BlockHeading.UP, 11, obj1)
        self.assertEqual(500, obj2.distance)
        self.assertEqual(11, obj2.set_speed)
        self.assertEqual(30.0, obj2.average_reported_speed)
        self.assertGreaterEqual(obj2.elapsed_time, 1.00)
        self.assertLess(obj2.elapsed_time, 1.10)


# --------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    unittest.main()
