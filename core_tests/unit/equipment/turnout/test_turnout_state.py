"""
Created on 11 Jun 2026

@author: Bruno Beloff (bbeloff@me.com)

python -m unittest -v dcc/z21/entities/test_control_router.py

https://realpython.com/python-testing/
https://www.jetbrains.com/help/pycharm/creating-tests.html
"""
import json
import unittest

from mrcs_core.data.json import JSONify
from mrcs_core.equipment.turnout.turnout_position import TurnoutPosition
from mrcs_core.equipment.turnout.turnout_state import TurnoutState


# --------------------------------------------------------------------------------------------------------------------

class TestTurnoutState(unittest.TestCase):

    def test_turnout(self):
        address = 3
        position = TurnoutPosition.P1

        obj1 = TurnoutState(address, position)
        self.assertEqual(address, obj1.address)
        self.assertEqual(position, obj1.position)


    def test_turnout_str(self):
        address = 3
        position = TurnoutPosition.P1

        obj1 = TurnoutState(address, position)
        self.assertEqual('TurnoutState:{address:3, position:P1}', str(obj1))


    def test_turnout_is_valid(self):
        address = 3
        position = TurnoutPosition.P1

        obj1 = TurnoutState(address, position)
        self.assertEqual(True, obj1.is_valid)


    def test_turnout_is_known(self):
        address = 3
        position = TurnoutPosition.P1

        obj1 = TurnoutState(address, position)
        self.assertEqual(True, obj1.is_known)


    def test_turnout_jstr(self):
        address = 3
        position = TurnoutPosition.P1

        obj1 = TurnoutState(address, position)
        jstr = JSONify.dumps(obj1)
        self.assertEqual('{"type": "TurnoutState", "addr": 3, "position": "P1"}', jstr)


    def test_turnout_jstr_eq(self):
        address = 3
        position = TurnoutPosition.P1

        obj1 = TurnoutState(address, position)
        jstr = JSONify.dumps(obj1)
        obj2 = TurnoutState.construct_from_jdict(json.loads(jstr))
        self.assertEqual(obj1, obj2)
