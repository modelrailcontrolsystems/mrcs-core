"""
Created on 6 Jul 2026

@author: Bruno Beloff (bbeloff@me.com)

python -m unittest -v unit/equipment/turnout/test_turnout_status.py

https://realpython.com/python-testing/
https://www.jetbrains.com/help/pycharm/creating-tests.html
"""

import json
import unittest

from mrcs_core.data.json import JSONify
from mrcs_core.equipment.turnout.turnout_enums import TurnoutPosition
from mrcs_core.equipment.turnout.turnout_status import TurnoutStatus


# --------------------------------------------------------------------------------------------------------------------

class TestTurnoutStatus(unittest.TestCase):

    def test_turnout_status_str(self):
        label = 'TE01'
        block_label = 'BN01'
        turnout_address = 3
        position = TurnoutPosition.UNKNOWN

        obj1 = TurnoutStatus(label, block_label, turnout_address, position)
        self.assertEqual('TurnoutStatus:{label:TE01, block_label:BN01, turnout_address:3, position:UNKNOWN}',
                         str(obj1))


    def test_turnout_status_is_known(self):
        label = 'TE01'
        block_label = 'BN01'
        turnout_address = 3
        position = TurnoutPosition.P1

        obj1 = TurnoutStatus(label, block_label, turnout_address, position)
        self.assertTrue(obj1.has_known_position)


    def test_turnout_status_is_not_known(self):
        label = 'TE01'
        block_label = 'BN01'
        turnout_address = 3
        position = TurnoutPosition.UNKNOWN

        obj1 = TurnoutStatus(label, block_label, turnout_address, position)
        self.assertFalse(obj1.has_known_position)


    def test_turnout_status_jstr(self):
        label = 'TE01'
        block_label = 'BN01'
        turnout_address = 3
        position = TurnoutPosition.P1

        obj1 = TurnoutStatus(label, block_label, turnout_address, position)
        jstr = JSONify.dumps(obj1)
        self.assertEqual('{"type": "TurnoutStatus", "label": "TE01", "block_label": "BN01", "addr": 3, '
                         '"position": "P1"}', jstr)


    def test_turnout_status_jstr_eq(self):
        label = 'TE01'
        block_label = 'BN01'
        turnout_address = 3
        position = TurnoutPosition.P1

        obj1 = TurnoutStatus(label, block_label, turnout_address, position)
        jstr = JSONify.dumps(obj1)
        obj2 = TurnoutStatus.construct_from_jdict(json.loads(jstr))
        self.assertEqual(obj1, obj2)


    def test_turnout_status_jstr_lt(self):
        label = 'TE01'
        block_label = 'BN01'
        turnout_address = 3
        position = TurnoutPosition.P0

        obj1 = TurnoutStatus(label, block_label, turnout_address, position)
        jstr = JSONify.dumps(obj1)
        obj2 = TurnoutStatus.construct_from_jdict(json.loads(jstr))
        self.assertFalse(obj1 < obj2)


# --------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    unittest.main()
