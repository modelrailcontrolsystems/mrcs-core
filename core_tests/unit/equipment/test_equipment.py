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
        jstr = ('{"type": "BlockOccupancyReport", "id": {"addr": 5, "channel": 6, "rid": 4660}, '
                '"group": 1, "occupants": [{"addr": 22136, "face": "FACE_BACKWARD"}]}')
        obj1 = EquipmentReport.construct_from_jdict(json.loads(jstr))
        self.assertEqual('BlockOccupancyReport:{block_id:BlockID:{detector_address:5, channel:6, reporter_id:0x1234}, '
                         'occupant_group:1, occupants:[BlockOccupant:{mpu_address:22136, face:FACE_BACKWARD}]}',
                         str(obj1))


    def test_block_status_report(self):
        jstr = ('{"type": "BlockVoltageReport", "id": {"addr": 5, "channel": 6, "rid": 4660}, '
                '"voltage": "OCCUPIED_OVERLOAD_1"}')
        obj1 = EquipmentReport.construct_from_jdict(json.loads(jstr))
        self.assertEqual('BlockVoltageReport:{block_id:BlockID:{detector_address:5, channel:6, reporter_id:0x1234}, '
                         'voltage:OCCUPIED_OVERLOAD_1}', str(obj1))


    def test_control_router(self):
        jstr = ('{"type": "ControlRouterReport", "main_current": 1, "prog_current": 2, "filtered_main_current": 3, '
                '"supply_voltage": 4, "track_voltage": 5, "temperature": 6, "central_state": 255, '
                '"central_state_ext": 0, "capabilities": 170, "reserved": 85}')
        obj1 = EquipmentReport.construct_from_jdict(json.loads(jstr))
        self.assertEqual('ControlRouterReport:{main_current:1, prog_current:2, filtered_main_current:3, '
                         'supply_voltage:4, track_voltage:5, temperature:6, central_state:0xff, '
                         'central_state_ext:0x00, capabilities:0xaa, reserved:0x55}', str(obj1))


    def test_motive_power_unit(self):
        jstr = ('{"type": "MPUConfigurationReport", "addr": 3, "functions": "+-+", "busy": false, '
                '"stepping": "STEPS_28", "speed": 12, "reverse": true, "consist": false, "smart_search": true}')
        obj1 = EquipmentReport.construct_from_jdict(json.loads(jstr))
        self.assertEqual('MPUConfigurationReport:{mpu_address:3, functions:+-+, is_busy:False, stepping:STEPS_28, '
                         'speed_setting:12, reverse:True, double_traction:False, smart_search:True}', str(obj1))


    def test_track(self):
        jstr = '{"type": "TrackReport", "mode": "SHORT_CIRCUIT"}'
        obj1 = EquipmentReport.construct_from_jdict(json.loads(jstr))
        self.assertEqual('TrackReport:{mode:SHORT_CIRCUIT}', str(obj1))


    def test_turnout(self):
        jstr = '{"type": "TurnoutReport", "addr": 3, "position": "P1"}'
        obj1 = EquipmentReport.construct_from_jdict(json.loads(jstr))
        self.assertEqual('TurnoutReport:{turnout_address:3, position:P1}', str(obj1))


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
