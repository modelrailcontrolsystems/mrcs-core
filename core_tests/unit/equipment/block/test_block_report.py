"""
Created on 17 Jun 2026

@author: Bruno Beloff (bbeloff@me.com)

python -m unittest -v unit/equipment/block/test_block_report.py

https://realpython.com/python-testing/
https://www.jetbrains.com/help/pycharm/creating-tests.html
"""

import json
import unittest

from mrcs_core.equipment.block.block_report import BlockReport


# --------------------------------------------------------------------------------------------------------------------

class TestBlockReport(unittest.TestCase):

    def test_block_report_status(self):
        jstr = ('{"type": "BlockVoltageReport", "id": {"addr": 5, "channel": 6, "rid": 4660}, '
                '"voltage": "OCCUPIED_OVERLOAD_1"}')

        obj1 = BlockReport.construct_from_jdict(json.loads(jstr))
        self.assertEqual('BlockVoltageReport:{block_id:BlockID:{address:5, channel:6, reporter_id:0x1234}, '
                         'voltage:OCCUPIED_OVERLOAD_1}', str(obj1))


    def test_block_address(self):
        jstr = ('{"type": "BlockVoltageReport", "id": {"addr": 5, "channel": 6, "rid": 4660}, '
                '"voltage": "OCCUPIED_OVERLOAD_1"}')

        obj1 = BlockReport.construct_from_jdict(json.loads(jstr))
        self.assertEqual('5/6', obj1.block_address)


    def test_block_report_occupancy(self):
        jstr = ('{"type": "BlockOccupancyReport", "id": {"addr": 5, "channel": 6, "rid": 4660}, '
                '"group": 1, "occupants": [{"addr": 22136, "face": "REV"}]}')

        obj1 = BlockReport.construct_from_jdict(json.loads(jstr))
        self.assertEqual('BlockOccupancyReport:{block_id:BlockID:{address:5, channel:6, reporter_id:0x1234}, '
                         'occupant_group:1, occupants:[BlockOccupant:{address:22136, face:REV}]}', str(obj1))


    def test_bad_type(self):
        jstr = ('{"type": "JUNK", "id": {"addr": 5, "channel": 6, "rid": 4660}, '
                '"group": 1, "occupants": [{"addr": 22136, "face": "REV"}]}')

        with self.assertRaises(TypeError):
            BlockReport.construct_from_jdict(json.loads(jstr))


# --------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    unittest.main()
