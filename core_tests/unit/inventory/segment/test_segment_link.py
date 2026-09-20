"""
Created on 10 Jul 2026

@author: Bruno Beloff (bbeloff@me.com)

python -m unittest -v unit/inventory/segment/test_segment_link.py

https://realpython.com/python-testing/
https://www.jetbrains.com/help/pycharm/creating-tests.html
"""

import json
import unittest

from mrcs_core.data.json import JSONify
from mrcs_core.equipment.turnout.turnout_enums import TurnoutPosition
from mrcs_core.inventory.layout.location import Location
from mrcs_core.inventory.segment.segment_link import FixedSegmentLink, SegmentLink, SwitchedSegmentLink


# --------------------------------------------------------------------------------------------------------------------

class TestSegmentLink(unittest.TestCase):

    @classmethod
    def __sample_simple_segment_link_1(cls):
        return FixedSegmentLink(Location('BN01', 'S02'))


    @classmethod
    def __sample_simple_segment_link_2(cls):
        return FixedSegmentLink(Location('BN02', 'S01'))


    @classmethod
    def __sample_switched_segment_link(cls):
        return SwitchedSegmentLink(Location('BN01', 'S02'), Location('BN02', 'S01'))


    @classmethod
    def __sample_switched_segment_link_half_null(cls):
        return SwitchedSegmentLink(Location('BN01', 'S02'), None)


    def test_track_segment_link_str(self):
        obj1 = self.__sample_simple_segment_link_1()
        self.assertEqual('FixedSegmentLink:{next_location:Location:{block_label:BN01, segment_label:S02}}', str(obj1))


    def test_track_segment_link_jstr(self):
        obj1 = self.__sample_simple_segment_link_1()
        jstr = JSONify.dumps(obj1)
        self.assertEqual('{"type": "Fixed", "next": "BN01/S02"}', jstr)


    def test_track_segment_jstr_eq(self):
        obj1 = self.__sample_simple_segment_link_1()
        jstr = JSONify.dumps(obj1)
        obj2 = SegmentLink.construct_from_jdict(json.loads(jstr))
        self.assertEqual(obj2, obj1)


    def test_track_segment_link(self):
        obj1 = self.__sample_simple_segment_link_1()
        link = obj1.selected_next_location(TurnoutPosition.P0)
        self.assertEqual('Location:{block_label:BN01, segment_label:S02}', str(link))


    def test_track_segment_link_next_locations(self):
        obj1 = self.__sample_simple_segment_link_1()
        self.assertEqual([Location('BN01', 'S02')], obj1.next_locations())


    def test_turnout_segment_link_str(self):
        obj1 = self.__sample_switched_segment_link()
        self.assertEqual('SwitchedSegmentLink:{p0_next_location:Location:{block_label:BN01, segment_label:S02}, '
                         'p1_next_location:Location:{block_label:BN02, segment_label:S01}}', str(obj1))


    def test_turnout_segment_link_jstr(self):
        obj1 = self.__sample_switched_segment_link()
        jstr = JSONify.dumps(obj1)
        self.assertEqual('{"type": "Switched", "p0-next": "BN01/S02", "p1-next": "BN02/S01"}', jstr)


    def test_turnout_segment_link_jstr_eq(self):
        obj1 = self.__sample_switched_segment_link()
        jstr = JSONify.dumps(obj1)
        obj2 = SegmentLink.construct_from_jdict(json.loads(jstr))
        self.assertEqual(obj2, obj1)


    def test_turnout_segment_link_half_null_jstr(self):
        obj1 = self.__sample_switched_segment_link_half_null()
        jstr = JSONify.dumps(obj1)
        self.assertEqual('{"type": "Switched", "p0-next": "BN01/S02", "p1-next": null}', jstr)


    def test_turnout_segment_link_half_null_jstr_eq(self):
        obj1 = self.__sample_switched_segment_link_half_null()
        jstr = JSONify.dumps(obj1)
        obj2 = SwitchedSegmentLink.construct_from_jdict(json.loads(jstr))
        self.assertEqual(obj2, obj1)


    def test_turnout_segment_link_p0(self):
        obj1 = self.__sample_switched_segment_link()
        link = obj1.selected_next_location(TurnoutPosition.P0)
        self.assertEqual('Location:{block_label:BN01, segment_label:S02}', str(link))


    def test_turnout_segment_link_p1(self):
        obj1 = self.__sample_switched_segment_link()
        link = obj1.selected_next_location(TurnoutPosition.P1)
        self.assertEqual('Location:{block_label:BN02, segment_label:S01}', str(link))


    def test_turnout_segment_link_next_locations(self):
        obj1 = self.__sample_switched_segment_link()
        self.assertEqual([Location('BN01', 'S02'), Location('BN02', 'S01')], obj1.next_locations())

        obj_half_null = self.__sample_switched_segment_link_half_null()
        self.assertEqual([Location('BN01', 'S02')], obj_half_null.next_locations())

        obj_null = SwitchedSegmentLink(None, None)
        self.assertEqual([], obj_null.next_locations())


    def test_turnout_segment_link_invalid_turnout_position(self):
        obj1 = self.__sample_switched_segment_link()
        with self.assertRaises(ValueError):
            obj1.selected_next_location(None)


    def test_segment_link_construct_from_none(self):
        self.assertIsNone(SegmentLink.construct_from_jdict(None))
        self.assertIsNone(FixedSegmentLink.construct_from_jdict(None))
        self.assertIsNone(SwitchedSegmentLink.construct_from_jdict(None))


    def test_segment_link_construct_from_jdict_invalid_type(self):
        with self.assertRaises(TypeError):
            SegmentLink.construct_from_jdict({'type': 'InvalidType'})

        with self.assertRaises(TypeError):
            FixedSegmentLink.construct_from_jdict({'type': 'Switched'})


    def test_fixed_segment_link_eq(self):
        obj1 = self.__sample_simple_segment_link_1()
        obj2 = self.__sample_simple_segment_link_1()
        obj3 = self.__sample_simple_segment_link_2()

        self.assertEqual(obj1, obj2)
        self.assertNotEqual(obj1, obj3)
        self.assertNotEqual(obj1, None)
        self.assertNotEqual(obj1, 'BN01:S02')


    def test_switched_segment_link_eq(self):
        obj1 = self.__sample_switched_segment_link()
        obj2 = self.__sample_switched_segment_link()
        obj3 = self.__sample_switched_segment_link_half_null()

        self.assertEqual(obj1, obj2)
        self.assertNotEqual(obj1, obj3)
        self.assertNotEqual(obj1, None)
        self.assertNotEqual(obj1, 'BN01:S02')
