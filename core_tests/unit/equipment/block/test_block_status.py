"""
Created on 3 Jul 2026

@author: Bruno Beloff (bbeloff@me.com)

python -m unittest -v unit/equipment/block/test_block_status.py

https://realpython.com/python-testing/
https://www.jetbrains.com/help/pycharm/creating-tests.html
"""

import json
import unittest

from mrcs_core.data.json import JSONify
from mrcs_core.equipment.block.block_enums import BlockDirection, BlockOccupantFace, BlockVoltage
from mrcs_core.equipment.block.block_occupant import BlockOccupant
from mrcs_core.equipment.block.block_status import BlockStatus


# --------------------------------------------------------------------------------------------------------------------

class TestBlockStatus(unittest.TestCase):

    @staticmethod
    def __sample_block_status():
        label = 'N01'
        address = '5/6'
        direction = BlockDirection.UP
        voltage = BlockVoltage.OCCUPIED_WITH_VOLTAGE
        occupants = [BlockOccupant(0x1234, BlockOccupantFace.FWD),
                     BlockOccupant(0x4567, BlockOccupantFace.REV)]

        return BlockStatus(label, address, direction, voltage, *occupants)


    def test_block_status_str(self):
        obj1 = self.__sample_block_status()
        self.assertEqual('BlockStatus:{label:N01, address:5/6, direction:UP, voltage:OCCUPIED_WITH_VOLTAGE, '
                         'occupants:[BlockOccupant:{address:4660, face:FWD}, '
                         'BlockOccupant:{address:17767, face:REV}]}', str(obj1))


    def test_block_occupation_report_jstr(self):
        obj1 = self.__sample_block_status()
        jstr = JSONify.dumps(obj1)
        self.assertEqual('{"type": "BlockStatus", "label": "N01", "addr": "5/6", "direction": "UP", '
                         '"voltage": "OCCUPIED_WITH_VOLTAGE", "occupants": [{"addr": 4660, "face": "FWD"}, '
                         '{"addr": 17767, "face": "REV"}]}', jstr)


    def test_block_occupation_report_jstr_eq(self):
        obj1 = self.__sample_block_status()
        jstr = JSONify.dumps(obj1)
        obj2 = BlockStatus.construct_from_jdict(json.loads(jstr))
        self.assertEqual(obj1, obj2)


    def test_block_occupation_report_jstr_lt(self):
        obj1 = self.__sample_block_status()
        jstr = JSONify.dumps(obj1)
        obj2 = BlockStatus.construct_from_jdict(json.loads(jstr))
        self.assertFalse(obj1 < obj2)


# --------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    unittest.main()
