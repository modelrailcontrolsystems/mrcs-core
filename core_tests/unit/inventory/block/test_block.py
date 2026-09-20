"""
Created on 10 Jul 2026

@author: Bruno Beloff (bbeloff@me.com)

python -m unittest -v unit/inventory/block/test_block.py

https://realpython.com/python-testing/
https://www.jetbrains.com/help/pycharm/creating-tests.html
"""

import json
import unittest
from collections import OrderedDict

from mrcs_core.data.json import JSONify
from mrcs_core.inventory.block.block import Block
from mrcs_core.inventory.block.block_operation import BlockOperation
from mrcs_core.inventory.layout.location import Location
from mrcs_core.inventory.segment.segment import TrackSegment
from mrcs_core.inventory.segment.segment_link import FixedSegmentLink


# --------------------------------------------------------------------------------------------------------------------

class TestBlock(unittest.TestCase):

    @classmethod
    def __sample_simple_segment_link_1(cls):
        return FixedSegmentLink(Location('BN01', 'S02'))


    @classmethod
    def __sample_simple_segment_link_2(cls):
        return FixedSegmentLink(Location('BN01', 'S03'))


    @classmethod
    def __sample_track_segment_1(cls):
        label = 'S01'
        up_link = cls.__sample_simple_segment_link_1()
        down_link = None
        length = 60
        return TrackSegment(label, up_link, down_link, length)


    @classmethod
    def __sample_track_segment_2(cls):
        label = 'S02'
        up_link = cls.__sample_simple_segment_link_1()
        down_link = cls.__sample_simple_segment_link_2()
        length = 80
        return TrackSegment(label, up_link, down_link, length)


    @classmethod
    def __sample_block_1(cls):
        label = 'BN01'
        address = '1/1'
        operation = BlockOperation.REVERSIBLE
        segment1 = cls.__sample_track_segment_1()
        segments = OrderedDict({segment1.label: segment1})
        return Block(label, address, operation, segments)


    @classmethod
    def __sample_block_2(cls):
        label = 'BN02'
        address = '1/2'
        operation = BlockOperation.UP_ONLY
        segment1 = cls.__sample_track_segment_1()
        segment2 = cls.__sample_track_segment_2()
        segments = OrderedDict({segment1.label: segment1, segment2.label: segment2})
        return Block(label, address, operation, segments)


    def test_block_construct(self):
        obj1 = self.__sample_block_1()
        self.assertEqual('BN01', obj1.label)
        self.assertEqual('1/1', obj1.address)
        self.assertEqual(BlockOperation.REVERSIBLE, obj1.operation)
        self.assertEqual((self.__sample_track_segment_1(),), obj1.segments)

        obj2 = self.__sample_block_2()
        self.assertEqual('BN02', obj2.label)
        self.assertEqual('1/2', obj2.address)
        self.assertEqual(BlockOperation.UP_ONLY, obj2.operation)
        self.assertEqual((self.__sample_track_segment_1(), self.__sample_track_segment_2()), obj2.segments)


    def test_block_str(self):
        self.maxDiff = None
        obj1 = self.__sample_block_1()
        self.assertEqual('Block:{label:BN01, address:1/1, operation:REVERSIBLE, '
                         'segments:[TrackSegment:{label:S01, up_link:FixedSegmentLink:{next_location:'
                         'Location:{block_label:BN01, segment_label:S02}}, down_link:None, length:60}]}', str(obj1))

        obj2 = self.__sample_block_2()
        self.assertEqual('Block:{label:BN02, address:1/2, operation:UP_ONLY, '
                         'segments:[TrackSegment:{label:S01, up_link:FixedSegmentLink:{next_location:'
                         'Location:{block_label:BN01, segment_label:S02}}, down_link:None, length:60}, '
                         'TrackSegment:{label:S02, up_link:FixedSegmentLink:{next_location:'
                         'Location:{block_label:BN01, segment_label:S02}}, down_link:FixedSegmentLink:{next_location:'
                         'Location:{block_label:BN01, segment_label:S03}}, length:80}]}', str(obj2))


    def test_block_as_json(self):
        obj1 = self.__sample_block_1()
        jdict = obj1.as_json()
        self.assertEqual('BN01', jdict['label'])
        self.assertEqual('1/1', jdict['addr'])
        self.assertEqual('REVERSIBLE', jdict['operation'])
        self.assertEqual((self.__sample_track_segment_1(),), jdict['segments'])

        obj2 = self.__sample_block_2()
        jdict2 = obj2.as_json()
        self.assertEqual('BN02', jdict2['label'])
        self.assertEqual('1/2', jdict2['addr'])
        self.assertEqual('UP_ONLY', jdict2['operation'])
        self.assertEqual((self.__sample_track_segment_1(), self.__sample_track_segment_2()), jdict2['segments'])


    def test_block_jstr(self):
        self.maxDiff = None
        obj1 = self.__sample_block_1()
        jstr = JSONify.dumps(obj1)
        self.assertEqual('{"label": "BN01", "addr": "1/1", "operation": "REVERSIBLE", '
                         '"segments": [{"type": "TrackSegment", "label": "S01", "length": 60, '
                         '"up-link": {"type": "Fixed", "next": "BN01/S02"}, "down-link": null}]}', jstr)

        obj2 = self.__sample_block_2()
        jstr2 = JSONify.dumps(obj2)
        self.assertEqual('{"label": "BN02", "addr": "1/2", "operation": "UP_ONLY", '
                         '"segments": [{"type": "TrackSegment", "label": "S01", "length": 60, '
                         '"up-link": {"type": "Fixed", "next": "BN01/S02"}, "down-link": null}, '
                         '{"type": "TrackSegment", "label": "S02", "length": 80, '
                         '"up-link": {"type": "Fixed", "next": "BN01/S02"}, '
                         '"down-link": {"type": "Fixed", "next": "BN01/S03"}}]}', jstr2)


    def test_block_jstr_eq(self):
        obj1 = self.__sample_block_1()
        jstr = JSONify.dumps(obj1)
        obj2 = Block.construct_from_jdict(json.loads(jstr))
        self.assertEqual(obj2, obj1)

        obj2 = self.__sample_block_2()
        jstr2 = JSONify.dumps(obj2)
        obj2_deserialized = Block.construct_from_jdict(json.loads(jstr2))
        self.assertEqual(obj2_deserialized, obj2)


    def test_block_eq(self):
        obj1 = self.__sample_block_1()
        obj2 = self.__sample_block_1()
        self.assertEqual(obj1, obj2)

        # Different label
        segment1 = self.__sample_track_segment_1()
        segments = OrderedDict({segment1.label: segment1})
        self.assertNotEqual(obj1, Block('BN99', '1/1', BlockOperation.REVERSIBLE, segments))

        # Different address
        segment1 = self.__sample_track_segment_1()
        segments = OrderedDict({segment1.label: segment1})
        self.assertNotEqual(obj1, Block('BN01', '9/9', BlockOperation.REVERSIBLE, segments))

        # Different segments
        segment2 = self.__sample_track_segment_2()
        segments = OrderedDict({segment2.label: segment2})
        self.assertNotEqual(obj1, Block('BN01', '1/1', BlockOperation.REVERSIBLE, segments))

        # Empty segments
        segments = OrderedDict({})
        self.assertNotEqual(obj1, Block('BN01', '1/1', BlockOperation.REVERSIBLE, segments))

        # Different type / None
        self.assertNotEqual(obj1, None)
        self.assertNotEqual(obj1, 'BN01')


    def test_block_lt(self):
        obj1 = self.__sample_block_1()
        obj2 = self.__sample_block_2()

        self.assertTrue(obj1 < obj2)
        self.assertFalse(obj2 < obj1)


    def test_block_segment(self):
        obj1 = self.__sample_block_1()
        self.assertEqual(self.__sample_track_segment_1(), obj1.segment('S01'))
        self.assertIsNone(obj1.segment('S99'))

        obj2 = self.__sample_block_2()
        self.assertEqual(self.__sample_track_segment_1(), obj2.segment('S01'))
        self.assertEqual(self.__sample_track_segment_2(), obj2.segment('S02'))
        self.assertIsNone(obj2.segment('S99'))


# --------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    unittest.main()
