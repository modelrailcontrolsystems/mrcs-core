"""
Created on 20 Jun 2026

@author: Bruno Beloff (bbeloff@me.com)

python -m unittest -v unit/equipment/test_equipment.py

https://realpython.com/python-testing/
https://www.jetbrains.com/help/pycharm/creating-tests.html
"""

import json
import unittest

from mrcs_core.equipment.equipment_report import EquipmentReport


# --------------------------------------------------------------------------------------------------------------------

class TestEquipment(unittest.TestCase):

    def test_block_occupancy_report(self):
        jstr = ('{"type": "BlockOccupancyReport", "nid": 1, "reporter": 2, "input": 3, "group": 1, '
                '"occupants": [{"addr": 4660, "face": "REV"}]}')
        obj1 = EquipmentReport.construct_from_jdict(json.loads(jstr))
        self.assertEqual('BlockOccupancyReport:{network_id:0x0001, reporter_address:2, reporter_input:3, '
                         'occupant_group:1, occupants:[BlockOccupant:{address:4660, face:REV}]}', str(obj1))


    def test_block_status_report(self):
        jstr = '{"type": "BlockStatusReport", "nid": 1, "reporter": 2, "input": 3, "status": "OCCUPIED_OVERLOAD_1"}'
        obj1 = EquipmentReport.construct_from_jdict(json.loads(jstr))
        self.assertEqual('BlockStatusReport:{network_id:0x0001, reporter_address:2, reporter_input:3, '
                         'status:OCCUPIED_OVERLOAD_1}', str(obj1))


    def test_control_router(self):
        jstr = ('{"type": "ControlRouterState", "main_current": 1, "prog_current": 2, "filtered_main_current": 3, '
                '"supply_voltage": 4, "track_voltage": 5, "temperature": 6, "central_state": 255, '
                '"central_state_ext": 0, "capabilities": 170, "reserved": 85}')
        obj1 = EquipmentReport.construct_from_jdict(json.loads(jstr))
        self.assertEqual('ControlRouterState:{main_current:1, prog_current:2, filtered_main_current:3, '
                         'supply_voltage:4, track_voltage:5, temperature:6, central_state:0xff, '
                         'central_state_ext:0x00, capabilities:0xaa, reserved:0x55}', str(obj1))


    def test_motive_power_unit(self):
        jstr = ('{"type": "MotivePowerUnitState", "addr": 3, "functions": "+-+", "busy": false, '
                '"stepping": "STEPS_28", "speed": 12, "reverse": true, "consist": false, "smart_search": true}')
        obj1 = EquipmentReport.construct_from_jdict(json.loads(jstr))
        self.assertEqual('MotivePowerUnitState:{address:3, functions:+-+, is_busy:False, stepping:STEPS_28, '
                         'speed_value:12, reverse:True, double_traction:False, smart_search:True}', str(obj1))


    def test_track(self):
        jstr = '{"type": "TrackState", "mode": "SHORT_CIRCUIT"}'
        obj1 = EquipmentReport.construct_from_jdict(json.loads(jstr))
        self.assertEqual('TrackState:{mode:SHORT_CIRCUIT}', str(obj1))


    def test_turnout(self):
        jstr = '{"type": "TurnoutState", "addr": 3, "position": "P1"}'
        obj1 = EquipmentReport.construct_from_jdict(json.loads(jstr))
        self.assertEqual('TurnoutState:{address:3, position:P1}', str(obj1))


    def test_unknown(self):
        jstr = '{"type": "Unknown", "addr": 3, "position": "P1"}'
        with self.assertRaises(TypeError):
            EquipmentReport.construct_from_jdict(json.loads(jstr))


    def test_none(self):
        jstr = '{"addr": 3, "position": "P1"}'
        with self.assertRaises(TypeError):
            EquipmentReport.construct_from_jdict(json.loads(jstr))


# --------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    unittest.main()
