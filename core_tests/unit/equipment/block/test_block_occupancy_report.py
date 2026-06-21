"""
Created on 13 Jun 2026

@author: Bruno Beloff (bbeloff@me.com)

python -m unittest -v unit/equipment/block/test_block_occupancy_report.py

https://realpython.com/python-testing/
https://www.jetbrains.com/help/pycharm/creating-tests.html
"""

import json
import unittest

from mrcs_core.data.json import JSONify
from mrcs_core.equipment.block.block_occupant import BlockOccupant
from mrcs_core.equipment.block.block_occupant_face import BlockOccupantFace
from mrcs_core.equipment.block.block_report import BlockOccupancyReport


# --------------------------------------------------------------------------------------------------------------------

class TestBlockOccupancyReport(unittest.TestCase):

    def test_block_occupation_report(self):
        network_id = 1
        reporter_address = 2
        reporter_input = 3
        occupant_group = 1
        occupants = [BlockOccupant(0x1234, BlockOccupantFace.REV)]

        obj1 = BlockOccupancyReport(network_id, reporter_address, reporter_input, occupant_group, occupants)
        self.assertEqual(network_id, obj1.network_id)
        self.assertEqual(reporter_address, obj1.reporter_address)
        self.assertEqual(reporter_input, obj1.reporter_input)
        self.assertEqual(occupant_group, obj1.occupant_group)
        self.assertEqual(occupants, obj1.occupants)


    def test_block_occupation_report_str(self):
        network_id = 1
        reporter_address = 2
        reporter_input = 3
        occupant_group = 1
        occupants = [BlockOccupant(0x1234, BlockOccupantFace.REV)]

        obj1 = BlockOccupancyReport(network_id, reporter_address, reporter_input, occupant_group, occupants)
        self.assertEqual('BlockOccupancyReport:{network_id:0x0001, reporter_address:2, reporter_input:3, '
                         'occupant_group:1, occupants:[BlockOccupant:{address:4660, face:REV}]}', str(obj1))


    def test_block_occupation_report_jstr(self):
        network_id = 1
        reporter_address = 2
        reporter_input = 3
        occupant_group = 1
        occupants = [BlockOccupant(0x1234, BlockOccupantFace.REV)]

        obj1 = BlockOccupancyReport(network_id, reporter_address, reporter_input, occupant_group, occupants)
        jstr = JSONify.dumps(obj1)
        self.assertEqual('{"type": "BlockOccupancyReport", "nid": 1, "reporter": 2, "input": 3, "group": 1, '
                         '"occupants": [{"addr": 4660, "face": "REV"}]}', jstr)


    def test_block_occupation_report_jstr_eq(self):
        network_id = 1
        reporter_address = 2
        reporter_input = 3
        occupant_group = 1
        occupants = [BlockOccupant(0x1234, BlockOccupantFace.REV)]

        obj1 = BlockOccupancyReport(network_id, reporter_address, reporter_input, occupant_group, occupants)
        jstr = JSONify.dumps(obj1)
        obj2 = BlockOccupancyReport.construct_from_jdict(json.loads(jstr))
        self.assertEqual(obj1, obj2)
