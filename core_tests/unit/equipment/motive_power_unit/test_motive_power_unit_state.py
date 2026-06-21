"""
Created on 6 Jun 2026

@author: Bruno Beloff (bbeloff@me.com)

python -m unittest -v unit/equipment/motive_power_unit/test_motive_power_unit_state.py

https://realpython.com/python-testing/
https://www.jetbrains.com/help/pycharm/creating-tests.html
"""

import json
import unittest

from mrcs_core.data.json import JSONify
from mrcs_core.equipment.motive_power_unit.motive_power_unit_state import MotivePowerUnitState
from mrcs_core.equipment.motive_power_unit.throttle import DCCThrottleSteps


# --------------------------------------------------------------------------------------------------------------------

class TestMotivePowerUnitState(unittest.TestCase):

    def test_construct_motive_power_unit(self):
        address = 3
        functions = [True, False, True]
        is_busy = False
        stepping = DCCThrottleSteps.STEPS_28
        speed_value = 12
        reverse = True
        double_traction = False
        smart_search = True

        obj1 = MotivePowerUnitState(address, functions, is_busy=is_busy, stepping=stepping, speed_value=speed_value,
                                    reverse=reverse, double_traction=double_traction, smart_search=smart_search)
        self.assertEqual(address, obj1.address)
        self.assertEqual(functions, obj1.functions)
        self.assertEqual(is_busy, obj1.is_busy)
        self.assertEqual(stepping, obj1.stepping)
        self.assertEqual(speed_value, obj1.speed_value)
        self.assertEqual(reverse, obj1.reverse)
        self.assertEqual(double_traction, obj1.double_traction)
        self.assertEqual(smart_search, obj1.smart_search)


    def test_motive_power_unit_percentage(self):
        address = 3
        functions = [True, False, True]
        is_busy = False
        stepping = DCCThrottleSteps.STEPS_28
        speed_value = 12
        reverse = True
        double_traction = False
        smart_search = True

        obj1 = MotivePowerUnitState(address, functions, is_busy=is_busy, stepping=stepping, speed_value=speed_value,
                                    reverse=reverse, double_traction=double_traction, smart_search=smart_search)
        self.assertEqual(43, obj1.speed_percentage)


    def test_motive_power_unit_str(self):
        address = 3
        functions = [True, False, True]
        is_busy = False
        stepping = DCCThrottleSteps.STEPS_28
        speed_value = 12
        reverse = True
        double_traction = False
        smart_search = True

        obj1 = MotivePowerUnitState(address, functions, is_busy=is_busy, stepping=stepping, speed_value=speed_value,
                                    reverse=reverse, double_traction=double_traction, smart_search=smart_search)
        self.assertEqual('MotivePowerUnitState:{address:3, functions:+-+, is_busy:False, stepping:STEPS_28, '
                         'speed_value:12, reverse:True, double_traction:False, smart_search:True}', str(obj1))


    def test_motive_power_unit_json(self):
        address = 3
        functions = [True, False, True]
        is_busy = False
        stepping = DCCThrottleSteps.STEPS_28
        speed_value = 12
        reverse = True
        double_traction = False
        smart_search = True

        obj1 = MotivePowerUnitState(address, functions, is_busy=is_busy, stepping=stepping, speed_value=speed_value,
                                    reverse=reverse, double_traction=double_traction, smart_search=smart_search)
        jstr = JSONify.dumps(obj1)
        self.assertEqual('{"type": "MotivePowerUnitState", "addr": 3, "functions": "+-+", "busy": false, '
                         '"stepping": "STEPS_28", "speed": 12, "reverse": true, "consist": false, '
                         '"smart_search": true}', jstr)
        obj2 = MotivePowerUnitState.construct_from_jdict(json.loads(jstr))
        self.assertEqual(obj1, obj2)
