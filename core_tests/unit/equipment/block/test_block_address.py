"""
Created on 1 Oct 2026

@author: Bruno Beloff (bbeloff@me.com)

python -m unittest -v unit/equipment/block/test_block_address.py

https://realpython.com/python-testing/
https://www.jetbrains.com/help/pycharm/creating-tests.html
"""

import json
import unittest

from mrcs_core.data.json import JSONify
from mrcs_core.equipment.block.block_address import BlockAddress


# --------------------------------------------------------------------------------------------------------------------

class TestBlockAddress(unittest.TestCase):

    @staticmethod
    def __sample_block_address():
        return BlockAddress(5, 6)


    # construction ---------------------------------------------------------------------------------------------------

    def test_construct(self):
        obj1 = self.__sample_block_address()
        self.assertEqual(5, obj1.detector)
        self.assertEqual(6, obj1.channel)
        self.assertEqual('BlockAddress:{detector:5, channel:6}', str(obj1))


    def test_shortform(self):
        obj1 = self.__sample_block_address()
        self.assertEqual('5/6', obj1.shortform)


    def test_construct_from_shortform(self):
        obj1 = BlockAddress.construct_from_shortform('5/6')
        self.assertEqual(5, obj1.detector)
        self.assertEqual(6, obj1.channel)


    def test_construct_from_shortform_round_trip(self):
        obj1 = self.__sample_block_address()
        obj2 = BlockAddress.construct_from_shortform(obj1.shortform)
        self.assertEqual(obj1, obj2)


    def test_construct_from_shortform_invalid_structure(self):
        for shortform in ('', '5', '5/', '/6', '/', '5/6/7'):
            with self.subTest(shortform=shortform):
                with self.assertRaises(ValueError) as ctx:
                    BlockAddress.construct_from_shortform(shortform)

                self.assertEqual(shortform, str(ctx.exception))


    def test_construct_from_shortform_non_numeric(self):
        for shortform in ('a/6', '5/b', 'a/b'):
            with self.subTest(shortform=shortform):
                with self.assertRaises(ValueError):
                    BlockAddress.construct_from_shortform(shortform)


    # JSON -----------------------------------------------------------------------------------------------------------

    def test_as_json(self):
        obj1 = self.__sample_block_address()
        self.assertEqual('5/6', obj1.as_json())


    def test_jstr(self):
        obj1 = self.__sample_block_address()
        jstr = JSONify.dumps(obj1)
        self.assertEqual('"5/6"', jstr)


    def test_jstr_eq(self):
        obj1 = self.__sample_block_address()
        jstr = JSONify.dumps(obj1)
        obj2 = BlockAddress.construct_from_jdict(json.loads(jstr))
        self.assertEqual(obj1, obj2)


    # equality and hashing -------------------------------------------------------------------------------------------

    def test_eq(self):
        self.assertEqual(BlockAddress(5, 6), BlockAddress(5, 6))
        self.assertNotEqual(BlockAddress(5, 6), BlockAddress(5, 7))
        self.assertNotEqual(BlockAddress(5, 6), BlockAddress(4, 6))


    def test_eq_other_type(self):
        obj1 = self.__sample_block_address()
        self.assertNotEqual(obj1, None)
        self.assertNotEqual(obj1, '5/6')
        self.assertNotEqual(obj1, (5, 6))


    # ordering -------------------------------------------------------------------------------------------------------

    def test_lt_by_detector(self):
        self.assertTrue(BlockAddress(4, 9) < BlockAddress(5, 1))
        self.assertFalse(BlockAddress(5, 1) < BlockAddress(4, 9))


    def test_lt_by_channel(self):
        self.assertTrue(BlockAddress(5, 1) < BlockAddress(5, 2))
        self.assertFalse(BlockAddress(5, 2) < BlockAddress(5, 1))


    def test_lt_equal(self):
        obj1 = self.__sample_block_address()
        obj2 = self.__sample_block_address()
        self.assertFalse(obj1 < obj2)
        self.assertFalse(obj2 < obj1)


    def test_sorted(self):
        addresses = [BlockAddress(2, 1), BlockAddress(1, 3), BlockAddress(1, 2), BlockAddress(0, 9)]
        expected = [BlockAddress(0, 9), BlockAddress(1, 2), BlockAddress(1, 3), BlockAddress(2, 1)]
        self.assertEqual(expected, sorted(addresses))


# --------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    unittest.main()
