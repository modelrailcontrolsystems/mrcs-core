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
from mrcs_core.equipment.block.block_address import BlockAddress
from mrcs_core.equipment.block.block_enums import BlockHeading, BlockOccupantFace, BlockVoltage
from mrcs_core.equipment.block.block_occupant import BlockOccupant
from mrcs_core.equipment.block.block_status import BlockStatus


# --------------------------------------------------------------------------------------------------------------------

class TestBlockStatus(unittest.TestCase):

    @staticmethod
    def __sample_block_status():
        label = 'N01'
        address = BlockAddress(5, 6)
        heading = BlockHeading.UP
        voltage = BlockVoltage.OCCUPIED_WITH_VOLTAGE
        occupants = [BlockOccupant(0x1234, BlockOccupantFace.FACE_FORWARD),
                     BlockOccupant(0x4567, BlockOccupantFace.FACE_BACKWARD)]

        return BlockStatus(label, address, heading, voltage, *occupants)


    def test_block_status_str(self):
        obj1 = self.__sample_block_status()
        self.assertEqual('BlockStatus:{label:N01, address:BlockAddress:{detector:5, channel:6}, heading:UP, '
                         'voltage:OCCUPIED_WITH_VOLTAGE, occupants:[BlockOccupant:{mpu_address:4660, '
                         'face:FACE_FORWARD}, BlockOccupant:{mpu_address:17767, face:FACE_BACKWARD}]}', str(obj1))


    def test_block_status_address(self):
        obj1 = self.__sample_block_status()
        self.assertEqual(BlockAddress(5, 6), obj1.address)


    def test_block_status_as_json(self):
        obj1 = self.__sample_block_status()
        jdict = obj1.as_json()
        self.assertEqual(BlockAddress(5, 6), jdict['addr'])


    def test_block_occupation_report_jstr(self):
        obj1 = self.__sample_block_status()
        jstr = JSONify.dumps(obj1)
        self.assertEqual('{"type": "BlockStatus", "label": "N01", "addr": "5/6", "heading": "UP", '
                         '"voltage": "OCCUPIED_WITH_VOLTAGE", "occupants": [{"addr": 4660, "face": "FACE_FORWARD"}, '
                         '{"addr": 17767, "face": "FACE_BACKWARD"}]}', jstr)


    def test_block_occupation_report_jstr_eq(self):
        obj1 = self.__sample_block_status()
        jstr = JSONify.dumps(obj1)
        obj2 = BlockStatus.construct_from_jdict(json.loads(jstr))
        self.assertEqual(BlockAddress(5, 6), obj2.address)
        self.assertEqual(obj1, obj2)


    def test_block_status_eq(self):
        obj1 = self.__sample_block_status()
        self.assertEqual(obj1, self.__sample_block_status())

        occupants = obj1.occupants

        # Different label
        self.assertNotEqual(obj1, BlockStatus('N99', BlockAddress(5, 6), BlockHeading.UP,
                                              BlockVoltage.OCCUPIED_WITH_VOLTAGE, *occupants))

        # Different address
        self.assertNotEqual(obj1, BlockStatus('N01', BlockAddress(5, 7), BlockHeading.UP,
                                              BlockVoltage.OCCUPIED_WITH_VOLTAGE, *occupants))

        # Different heading
        self.assertNotEqual(obj1, BlockStatus('N01', BlockAddress(5, 6), BlockHeading.UNASSIGNED,
                                              BlockVoltage.OCCUPIED_WITH_VOLTAGE, *occupants))

        # Different voltage
        self.assertNotEqual(obj1, BlockStatus('N01', BlockAddress(5, 6), BlockHeading.UP,
                                              BlockVoltage.UNKNOWN, *occupants))

        # Different occupants
        self.assertNotEqual(obj1, BlockStatus('N01', BlockAddress(5, 6), BlockHeading.UP,
                                              BlockVoltage.OCCUPIED_WITH_VOLTAGE, occupants[0]))

        # Occupant order is not significant
        self.assertEqual(obj1, BlockStatus('N01', BlockAddress(5, 6), BlockHeading.UP,
                                           BlockVoltage.OCCUPIED_WITH_VOLTAGE, *reversed(occupants)))

        # Different type / None
        self.assertNotEqual(obj1, None)
        self.assertNotEqual(obj1, 'N01')


    def test_block_occupation_report_jstr_lt(self):
        obj1 = self.__sample_block_status()
        jstr = JSONify.dumps(obj1)
        obj2 = BlockStatus.construct_from_jdict(json.loads(jstr))
        self.assertFalse(obj1 < obj2)


# --------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    unittest.main()
