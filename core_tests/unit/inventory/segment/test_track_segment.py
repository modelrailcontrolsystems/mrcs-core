"""
Created on 10 Jul 2026

@author: Bruno Beloff (bbeloff@me.com)

python -m unittest -v unit/inventory/segment/test_track_segment.py

https://realpython.com/python-testing/
https://www.jetbrains.com/help/pycharm/creating-tests.html
"""

import json
import unittest

from mrcs_core.data.json import JSONify
from mrcs_core.equipment.block.block_enums import BlockHeading
from mrcs_core.equipment.turnout.turnout_configuration import TurnoutConfiguration
from mrcs_core.inventory.layout.location import Location
from mrcs_core.inventory.segment.segment import Segment, TrackSegment
from mrcs_core.inventory.segment.segment_link import FixedSegmentLink


# --------------------------------------------------------------------------------------------------------------------

class TestTrackSegment(unittest.TestCase):

    @classmethod
    def __sample_simple_segment_link_1(cls):
        return FixedSegmentLink(Location('BN01', 'S02'))


    @classmethod
    def __sample_simple_segment_link_2(cls):
        return FixedSegmentLink(Location('BN01', 'S03'))


    @classmethod
    def __sample_track_segment_1(cls):
        label = 'S01'
        length = 60
        up_link = cls.__sample_simple_segment_link_1()
        down_link = None
        return TrackSegment(label, length, up_link, down_link)


    @classmethod
    def __sample_track_segment_2(cls):
        label = 'S02'
        length = 80
        up_link = cls.__sample_simple_segment_link_1()
        down_link = cls.__sample_simple_segment_link_2()
        return TrackSegment(label, length, up_link, down_link)


    @classmethod
    def __sample_turnout_configuration(cls):
        return TurnoutConfiguration({})


    def test_track_segment_construct(self):
        obj1 = self.__sample_track_segment_1()
        self.assertEqual('S01', obj1.label)
        self.assertEqual(60, obj1.length)
        self.assertEqual(self.__sample_simple_segment_link_1(), obj1.up_link)
        self.assertIsNone(obj1.down_link)


    def test_track_segment_str(self):
        obj1 = self.__sample_track_segment_1()
        self.assertEqual('TrackSegment:{label:S01, length:60, up_link:FixedSegmentLink:{next_location:Location:'
                         '{block_label:BN01, segment_label:S02}}, down_link:None}', str(obj1))


    def test_track_segment_as_json(self):
        obj1 = self.__sample_track_segment_1()
        jdict = obj1.as_json()
        self.assertEqual('TrackSegment', jdict['type'])
        self.assertEqual('S01', jdict['label'])
        self.assertEqual(60, jdict['length'])
        self.assertEqual(self.__sample_simple_segment_link_1(), jdict['up-link'])
        self.assertIsNone(jdict['down-link'])


    def test_track_segment_jstr(self):
        obj1 = self.__sample_track_segment_1()
        jstr = JSONify.dumps(obj1)
        self.assertEqual('{"type": "TrackSegment", "label": "S01", "length": 60, '
                         '"up-link": {"type": "Fixed", "next": ["BN01", "S02"]}, "down-link": null}', jstr)


    def test_track_segment_jstr_eq(self):
        obj1 = self.__sample_track_segment_1()
        jstr = JSONify.dumps(obj1)
        obj2 = TrackSegment.construct_from_jdict(json.loads(jstr))
        self.assertEqual(obj2, obj1)


    def test_track_segment_construct_from_jdict_invalid_type(self):
        with self.assertRaises(TypeError):
            TrackSegment.construct_from_jdict({'type': 'InvalidType'})


    def test_segment_construct_from_jdict(self):
        obj1 = self.__sample_track_segment_1()
        jstr = JSONify.dumps(obj1)
        obj2 = Segment.construct_from_jdict(json.loads(jstr))
        self.assertEqual(obj2, obj1)

        with self.assertRaises(TypeError):
            Segment.construct_from_jdict({'type': 'InvalidType'})


    def test_track_segment_eq(self):
        obj1 = self.__sample_track_segment_1()
        obj2 = self.__sample_track_segment_1()
        self.assertEqual(obj1, obj2)

        # Different label
        self.assertNotEqual(obj1, TrackSegment('S99', 60, self.__sample_simple_segment_link_1(), None))
        # Different length
        self.assertNotEqual(obj1, TrackSegment('S01', 100, self.__sample_simple_segment_link_1(), None))
        # Different up_link
        self.assertNotEqual(obj1, TrackSegment('S01', 60, None, None))
        # Different down_link
        self.assertNotEqual(obj1, TrackSegment('S01', 60, self.__sample_simple_segment_link_1(),
                                               self.__sample_simple_segment_link_2()))
        # Different type / None
        self.assertNotEqual(obj1, None)
        self.assertNotEqual(obj1, 'S01')


    def test_track_segment_lt(self):
        obj1 = self.__sample_track_segment_1()
        obj2 = self.__sample_track_segment_2()

        self.assertTrue(obj1 < obj2)
        self.assertFalse(obj2 < obj1)


    def test_track_segment_next_location(self):
        obj1 = self.__sample_track_segment_1()
        conf = self.__sample_turnout_configuration()

        self.assertEqual(Location('BN01', 'S02'), obj1.next_location(conf, BlockHeading.UP))
        self.assertIsNone(obj1.next_location(conf, BlockHeading.DOWN))

        with self.assertRaises(ValueError):
            obj1.next_location(conf, BlockHeading.UNASSIGNED)


    def test_track_segment_next_up_location(self):
        obj1 = self.__sample_track_segment_1()
        conf = self.__sample_turnout_configuration()
        self.assertEqual(Location('BN01', 'S02'), obj1.next_up_location(conf))

        obj_no_link = TrackSegment('S01', 60, None, None)
        self.assertIsNone(obj_no_link.next_up_location(conf))


    def test_track_segment_next_down_location(self):
        obj1 = self.__sample_track_segment_1()
        conf = self.__sample_turnout_configuration()
        self.assertIsNone(obj1.next_down_location(conf))

        obj2 = self.__sample_track_segment_2()
        self.assertEqual(Location('BN01', 'S03'), obj2.next_down_location(conf))


    def test_track_segment_next_locations(self):
        obj1 = self.__sample_track_segment_1()
        self.assertEqual([Location('BN01', 'S02')], obj1.next_up_locations())
        self.assertEqual([], obj1.next_down_locations())
        self.assertEqual([Location('BN01', 'S02')], obj1.next_locations())

        obj2 = self.__sample_track_segment_2()
        self.assertEqual([Location('BN01', 'S02')], obj2.next_up_locations())
        self.assertEqual([Location('BN01', 'S03')], obj2.next_down_locations())
        self.assertEqual([Location('BN01', 'S02'), Location('BN01', 'S03')], obj2.next_locations())

        obj_no_links = TrackSegment('S01', 60, None, None)
        self.assertEqual([], obj_no_links.next_up_locations())
        self.assertEqual([], obj_no_links.next_down_locations())
        self.assertEqual([], obj_no_links.next_locations())


# --------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    unittest.main()
