"""
Created on 10 Oct 2026

@author: Bruno Beloff (bbeloff@me.com)

python -m unittest -v unit/inventory/configuration_variable/test_cv_address.py

https://realpython.com/python-testing/
https://www.jetbrains.com/help/pycharm/creating-tests.html
"""

import unittest

from mrcs_core.inventory.configuration_variable.cv_address import CVAddress


# --------------------------------------------------------------------------------------------------------------------

class TestCVAddress(unittest.TestCase):

    def test_cv_address_list(self):
        obj1 = CVAddress.keys()
        self.assertEqual(['SHORT_ADDRESS', 'START_VOLTAGE', 'ACCELERATION', 'DECELERATION', 'MAX_SPEED',
                          'MID_SPEED', 'MANUFACTURER_VERSION', 'MANUFACTURER_ID', 'MOTOR_PWM_FREQUENCY',
                          'CONSIST_ADDRESS', 'RAILCOM', 'CONFIGURATION', 'SOUND_VOLUME'], list(obj1))


    def test_cv_address_find(self):
        obj1 = CVAddress['SHORT_ADDRESS']
        self.assertEqual('SHORT_ADDRESS{1}', str(obj1))
