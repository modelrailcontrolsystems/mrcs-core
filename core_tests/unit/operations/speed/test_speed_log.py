"""
Created on 25 Oct 2025

@author: Bruno Beloff (bbeloff@me.com)

python -m unittest -v unit/operations/speed/test_speed_log.py

https://realpython.com/python-testing/
https://www.jetbrains.com/help/pycharm/creating-tests.html
https://stackoverflow.com/questions/8047736/how-to-load-data-from-a-file-for-a-unit-test-in-python
"""

import time
import unittest

from mrcs_core.operations.speed.speed_log import SpeedLog


# --------------------------------------------------------------------------------------------------------------------

class TestSpeedLog(unittest.TestCase):

    def test_construct(self):
        obj1 = SpeedLog.start()
        self.assertEqual(1, len(obj1))


    def test_run_1(self):
        obj1 = SpeedLog.start()
        time.sleep(1)
        obj1.mark(30)
        self.assertEqual(30, obj1.average_reported_speed)


    def test_run_2(self):
        obj1 = SpeedLog.start()
        time.sleep(1)
        obj1.mark(30)
        time.sleep(1)
        obj1.mark(40)
        self.assertEqual(35, obj1.average_reported_speed)


    def test_run_3(self):
        obj1 = SpeedLog.start()
        time.sleep(1)
        obj1.mark(30)
        time.sleep(1)
        obj1.mark(40)
        time.sleep(1)
        obj1.mark(50)
        self.assertEqual(40, obj1.average_reported_speed)


# --------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    unittest.main()
