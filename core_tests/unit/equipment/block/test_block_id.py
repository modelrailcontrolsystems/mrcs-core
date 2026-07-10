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
from mrcs_core.equipment.block.block_id import BlockID


# --------------------------------------------------------------------------------------------------------------------

class TestBlockID(unittest.TestCase):

    @staticmethod
    def __sample_block_id():
        detector_address = 5
        channel = 6
        reporter_id = 0x1234

        return BlockID(detector_address, channel, reporter_id)


    def test_block_construct(self):
        obj1 = self.__sample_block_id()
        self.assertEqual('BlockID:{detector_address:5, channel:6, reporter_id:0x1234}', str(obj1))


    def test_block_address(self):
        obj1 = self.__sample_block_id()
        self.assertEqual('5/6', obj1.block_address)


    def test_block_jstr(self):
        obj1 = self.__sample_block_id()
        jstr = JSONify.dumps(obj1)
        self.assertEqual('{"addr": 5, "channel": 6, "rid": 4660}', jstr)


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


# --------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    unittest.main()
