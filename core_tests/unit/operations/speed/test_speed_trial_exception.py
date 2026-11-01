"""
Created on 25 Oct 2025

@author: Bruno Beloff (bbeloff@me.com)

python -m unittest -v unit/operations/speed/test_speed_trial_exception.py

https://realpython.com/python-testing/
https://www.jetbrains.com/help/pycharm/creating-tests.html
https://stackoverflow.com/questions/8047736/how-to-load-data-from-a-file-for-a-unit-test-in-python
"""

import unittest

from mrcs_core.operations.speed.speed_trial_exception import SpeedTrialException


# --------------------------------------------------------------------------------------------------------------------

class TestSpeedTrialException(unittest.TestCase):

    def test_construct(self):
        obj1 = SpeedTrialException('something went wrong')
        self.assertEqual('something went wrong', str(obj1))


# --------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    unittest.main()
