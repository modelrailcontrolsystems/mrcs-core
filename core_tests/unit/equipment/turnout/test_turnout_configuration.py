"""
Created on 9 Jul 2026

@author: Bruno Beloff (bbeloff@me.com)

python -m unittest -v unit/equipment/turnout/test_turnout_configuration.py

https://realpython.com/python-testing/
https://www.jetbrains.com/help/pycharm/creating-tests.html
"""

import unittest

from mrcs_core.equipment.turnout.turnout_configuration import TurnoutConfiguration
from mrcs_core.equipment.turnout.turnout_enums import TurnoutPosition
from mrcs_core.equipment.turnout.turnout_status import TurnoutStatus


# --------------------------------------------------------------------------------------------------------------------

class TestTurnoutConfiguration(unittest.TestCase):

    @staticmethod
    def __sample_turnout_status_group_valid():
        label = 'TE01'
        block_label = 'BN01'
        turnout_address = 3
        position = TurnoutPosition.P1
        obj1 = TurnoutStatus(label, block_label, turnout_address, position)

        label = 'TE02'
        block_label = 'BN01'
        turnout_address = 4
        position = TurnoutPosition.P0
        obj2 = TurnoutStatus(label, block_label, turnout_address, position)

        return TurnoutConfiguration.construct_from_turnouts(obj1, obj2)


    @staticmethod
    def __sample_turnout_status_group_invalid():
        label = 'TE01'
        block_label = 'BN01'
        turnout_address = 3
        position = TurnoutPosition.P1
        obj1 = TurnoutStatus(label, block_label, turnout_address, position)

        label = 'TE02'
        block_label = 'BN01'
        turnout_address = 4
        position = TurnoutPosition.UNKNOWN
        obj2 = TurnoutStatus(label, block_label, turnout_address, position)

        return TurnoutConfiguration.construct_from_turnouts(obj1, obj2)


    def test_turnout_configuration_str(self):
        config = self.__sample_turnout_status_group_valid()
        self.assertEqual('TurnoutConfiguration:{positions:{TE01:P1, TE02:P0}}', str(config))


    def test_turnout_configuration_valid(self):
        config = self.__sample_turnout_status_group_valid()
        self.assertTrue(config.is_valid())


    def test_turnout_configuration_TE02(self):
        config = self.__sample_turnout_status_group_valid()
        position = config.position('TE02')
        assert position is not None
        self.assertEqual('P0', position.name)


    def test_turnout_configuration_invalid(self):
        config = self.__sample_turnout_status_group_invalid()
        self.assertFalse(config.is_valid())


# --------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    unittest.main()
