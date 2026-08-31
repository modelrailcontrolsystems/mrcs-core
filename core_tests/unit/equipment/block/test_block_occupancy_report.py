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
from mrcs_core.equipment.block.block_enums import BlockOccupantFace
from mrcs_core.equipment.block.block_id import BlockID
from mrcs_core.equipment.block.block_occupant import BlockOccupant
from mrcs_core.equipment.block.block_report import BlockOccupancyReport


# --------------------------------------------------------------------------------------------------------------------

class TestBlockOccupancyReport(unittest.TestCase):

    @staticmethod
    def __sample_block_occupancy_report():
        detector_address = 5
        channel = 6
        reporter_id = 0x1234
        block_id = BlockID(detector_address, channel, reporter_id)

        occupant_group = 1
        occupants = [BlockOccupant(0x5678, BlockOccupantFace.FACE_BACKWARD)]

        return BlockOccupancyReport(block_id, occupant_group, occupants)


    def test_block_occupation_report_str(self):
        obj1 = self.__sample_block_occupancy_report()
        self.assertEqual('BlockOccupancyReport:{block_id:BlockID:{detector_address:5, channel:6, reporter_id:0x1234}, '
                         'occupant_group:1, occupants:[BlockOccupant:{mpu_address:22136, face:FACE_BACKWARD}]}',
                         str(obj1))


    def test_block_status_report_occupancy(self):
        obj1 = self.__sample_block_occupancy_report()
        self.assertTrue(obj1.has_occupants)


    def test_block_occupation_report_jstr(self):
        obj1 = self.__sample_block_occupancy_report()
        jstr = JSONify.dumps(obj1)
        self.assertEqual('{"type": "BlockOccupancyReport", "id": {"addr": 5, "channel": 6, "rid": 4660}, '
                         '"group": 1, "occupants": [{"addr": 22136, "face": "FACE_BACKWARD"}]}', jstr)


    def test_block_occupation_report_jstr_eq(self):
        obj1 = self.__sample_block_occupancy_report()
        jstr = JSONify.dumps(obj1)
        obj2 = BlockOccupancyReport.construct_from_jdict(json.loads(jstr))
        self.assertEqual(obj1, obj2)


# --------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    unittest.main()
