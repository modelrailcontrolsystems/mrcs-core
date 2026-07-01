"""
Created on 11 Jun 2026

@author: Bruno Beloff (bbeloff@me.com)

python -m unittest -v unit/equipment/control_router/test_control_router_report.py

https://realpython.com/python-testing/
https://www.jetbrains.com/help/pycharm/creating-tests.html
"""

import json
import unittest

from mrcs_core.data.json import JSONify
from mrcs_core.equipment.control_router.control_router_report import ControlRouterReport


# --------------------------------------------------------------------------------------------------------------------

class TestControlRouterReport(unittest.TestCase):

    def test_control_router(self):
        main_current = 1
        prog_current = 2
        filtered_main_current = 3
        supply_voltage = 4
        track_voltage = 5
        temperature = 6
        central_state = 0xff
        central_state_ext = 0x00
        capabilities = 0xaa
        reserved = 0x55

        obj1 = ControlRouterReport(main_current, prog_current, filtered_main_current, supply_voltage, track_voltage,
                                   temperature, central_state, central_state_ext, capabilities, reserved=reserved)
        self.assertEqual(main_current, obj1.main_current)
        self.assertEqual(prog_current, obj1.prog_current)
        self.assertEqual(filtered_main_current, obj1.filtered_main_current)
        self.assertEqual(supply_voltage, obj1.supply_voltage)
        self.assertEqual(track_voltage, obj1.track_voltage)
        self.assertEqual(temperature, obj1.temperature)
        self.assertEqual(central_state, obj1.central_state)
        self.assertEqual(central_state_ext, obj1.central_state_ext)
        self.assertEqual(capabilities, obj1.capabilities)
        self.assertEqual(reserved, obj1.reserved)


    def test_control_router_str(self):
        main_current = 1
        prog_current = 2
        filtered_main_current = 3
        supply_voltage = 4
        track_voltage = 5
        temperature = 6
        central_state = 0xff
        central_state_ext = 0x00
        capabilities = 0xaa
        reserved = 0x55

        obj1 = ControlRouterReport(main_current, prog_current, filtered_main_current, supply_voltage, track_voltage,
                                   temperature, central_state, central_state_ext, capabilities, reserved=reserved)
        self.assertEqual(
            'ControlRouterReport:{main_current:1, prog_current:2, filtered_main_current:3, supply_voltage:4, '
            'track_voltage:5, temperature:6, central_state:0xff, central_state_ext:0x00, capabilities:0xaa, '
            'reserved:0x55}', str(obj1))


    def test_control_router_jstr(self):
        main_current = 1
        prog_current = 2
        filtered_main_current = 3
        supply_voltage = 4
        track_voltage = 5
        temperature = 6
        central_state = 0xff
        central_state_ext = 0x00
        capabilities = 0xaa
        reserved = 0x55

        obj1 = ControlRouterReport(main_current, prog_current, filtered_main_current, supply_voltage, track_voltage,
                                   temperature, central_state, central_state_ext, capabilities, reserved=reserved)
        jstr = JSONify.dumps(obj1)
        self.assertEqual('{"type": "ControlRouterReport", "main_current": 1, "prog_current": 2, '
                         '"filtered_main_current": 3, "supply_voltage": 4, "track_voltage": 5, "temperature": 6, '
                         '"central_state": 255, "central_state_ext": 0, "capabilities": 170, "reserved": 85}', jstr)


    def test_control_router_jstr_eq(self):
        main_current = 1
        prog_current = 2
        filtered_main_current = 3
        supply_voltage = 4
        track_voltage = 5
        temperature = 6
        central_state = 0xff
        central_state_ext = 0x00
        capabilities = 0xaa
        reserved = 0x55

        obj1 = ControlRouterReport(main_current, prog_current, filtered_main_current, supply_voltage, track_voltage,
                                   temperature, central_state, central_state_ext, capabilities, reserved=reserved)
        jstr = JSONify.dumps(obj1)
        obj2 = ControlRouterReport.construct_from_jdict(json.loads(jstr))
        self.assertEqual(obj1, obj2)


# --------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    unittest.main()
