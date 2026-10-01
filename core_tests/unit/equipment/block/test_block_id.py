"""
Created on 2 Jul 2026

@author: Bruno Beloff (bbeloff@me.com)

python -m unittest -v unit/equipment/block/test_block_id.py

https://realpython.com/python-testing/
https://www.jetbrains.com/help/pycharm/creating-tests.html
"""

import json
import unittest

from mrcs_core.data.json import JSONify
from mrcs_core.equipment.block.block_address import BlockAddress
from mrcs_core.equipment.block.block_id import BlockID


# --------------------------------------------------------------------------------------------------------------------

class TestBlockID(unittest.TestCase):

    @staticmethod
    def __sample_block_id():
        address = BlockAddress(5, 6)
        reporter_id = 0x1234

        return BlockID(address, reporter_id)


    def test_block_construct(self):
        obj1 = self.__sample_block_id()
        self.assertEqual(BlockAddress(5, 6), obj1.address)
        self.assertEqual(0x1234, obj1.reporter_id)
        self.assertEqual('BlockID:{address:BlockAddress:{detector:5, channel:6}, reporter_id:0x1234}', str(obj1))


    def test_block_as_json(self):
        obj1 = self.__sample_block_id()
        jdict = obj1.as_json()
        self.assertEqual(['addr', 'rid'], list(jdict.keys()))
        self.assertEqual(BlockAddress(5, 6), jdict['addr'])
        self.assertEqual(0x1234, jdict['rid'])


    def test_block_jstr(self):
        obj1 = self.__sample_block_id()
        jstr = JSONify.dumps(obj1)
        self.assertEqual('{"addr": "5/6", "rid": 4660}', jstr)


    def test_block_construct_from_jdict(self):
        obj1 = BlockID.construct_from_jdict({'addr': '5/6', 'rid': 4660})
        self.assertEqual(BlockAddress(5, 6), obj1.address)
        self.assertEqual(0x1234, obj1.reporter_id)


    def test_block_jstr_eq(self):
        obj1 = self.__sample_block_id()
        jstr = JSONify.dumps(obj1)
        obj2 = BlockID.construct_from_jdict(json.loads(jstr))
        self.assertEqual(obj1, obj2)


    def test_block_jstr_lt(self):
        obj1 = self.__sample_block_id()
        jstr = JSONify.dumps(obj1)
        obj2 = BlockID.construct_from_jdict(json.loads(jstr))
        self.assertFalse(obj1 < obj2)


    def test_block_eq(self):
        obj1 = self.__sample_block_id()
        self.assertEqual(obj1, BlockID(BlockAddress(5, 6), 0x1234))
        self.assertNotEqual(obj1, BlockID(BlockAddress(5, 7), 0x1234))
        self.assertNotEqual(obj1, BlockID(BlockAddress(4, 6), 0x1234))
        self.assertNotEqual(obj1, BlockID(BlockAddress(5, 6), 0x4321))


    def test_block_eq_other_type(self):
        obj1 = self.__sample_block_id()
        self.assertNotEqual(obj1, None)
        self.assertNotEqual(obj1, BlockAddress(5, 6))


    def test_block_lt_by_address(self):
        obj1 = BlockID(BlockAddress(5, 1), 0x4321)
        obj2 = BlockID(BlockAddress(5, 2), 0x1234)
        self.assertTrue(obj1 < obj2)
        self.assertFalse(obj2 < obj1)


    def test_block_lt_by_reporter_id(self):
        obj1 = BlockID(BlockAddress(5, 6), 0x1234)
        obj2 = BlockID(BlockAddress(5, 6), 0x4321)
        self.assertTrue(obj1 < obj2)
        self.assertFalse(obj2 < obj1)


    def test_block_sorted(self):
        ids = [BlockID(BlockAddress(2, 1), 1), BlockID(BlockAddress(1, 2), 2), BlockID(BlockAddress(1, 2), 1)]
        expected = [BlockID(BlockAddress(1, 2), 1), BlockID(BlockAddress(1, 2), 2), BlockID(BlockAddress(2, 1), 1)]
        self.assertEqual(expected, sorted(ids))


# --------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    unittest.main()
