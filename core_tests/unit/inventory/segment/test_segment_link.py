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
from mrcs_core.inventory.segment.segment_link import SegmentLink, TrackSegmentLink, TurnoutSegmentLink


# --------------------------------------------------------------------------------------------------------------------

class TestSegmentLink(unittest.TestCase):

    @classmethod
    def __sample_track_segment_link_1(cls):
        return TrackSegmentLink('BN01', 'S02')


    @classmethod
    def __sample_track_segment_link_2(cls):
        return TrackSegmentLink('BN02', 'S01')


    @classmethod
    def __sample_turnout_segment_link(cls):
        return TurnoutSegmentLink(cls.__sample_track_segment_link_1(), cls.__sample_track_segment_link_2())


    @classmethod
    def __sample_turnout_segment_link_half_null(cls):
        return TurnoutSegmentLink(cls.__sample_track_segment_link_1(), None)


    def test_track_segment_link_str(self):
        obj1 = self.__sample_track_segment_link_1()
        self.assertEqual('TrackSegmentLink:{block_label:BN01, segment_label:S02}', str(obj1))


    def test_track_segment_link_jstr(self):
        obj1 = self.__sample_track_segment_link_1()
        jstr = JSONify.dumps(obj1)
        self.assertEqual('{"type": "TrackSegmentLink", "link": ["BN01", "S02"]}', jstr)


    def test_track_segment_jstr_eq(self):
        obj1 = self.__sample_track_segment_link_1()
        jstr = JSONify.dumps(obj1)
        obj2 = TrackSegmentLink.construct_from_jdict(json.loads(jstr))
        self.assertEqual(obj2, obj1)


    def test_track_segment_link(self):
        obj1 = self.__sample_track_segment_link_1()
        link = obj1.link_for_config(TurnoutPosition.P0)
        self.assertEqual('TrackSegmentLink:{block_label:BN01, segment_label:S02}', str(link))


    def test_turnout_segment_link_str(self):
        obj1 = self.__sample_turnout_segment_link()
        self.assertEqual('TurnoutSegmentLink:{link_p0:TrackSegmentLink:{block_label:BN01, segment_label:S02}, '
                         'link_p1:TrackSegmentLink:{block_label:BN02, segment_label:S01}}', str(obj1))


    def test_turnout_segment_link_jstr(self):
        obj1 = self.__sample_turnout_segment_link()
        jstr = JSONify.dumps(obj1)
        self.assertEqual('{"type": "TurnoutSegmentLink", "p0": ["BN01", "S02"], "p1": ["BN02", "S01"]}', jstr)


    def test_turnout_segment_link_jstr_eq(self):
        obj1 = self.__sample_turnout_segment_link()
        jstr = JSONify.dumps(obj1)
        obj2 = TurnoutSegmentLink.construct_from_jdict(json.loads(jstr))
        self.assertEqual(obj2, obj1)


    def test_turnout_segment_link_half_null_jstr(self):
        obj1 = self.__sample_turnout_segment_link_half_null()
        jstr = JSONify.dumps(obj1)
        self.assertEqual('{"type": "TurnoutSegmentLink", "p0": ["BN01", "S02"], "p1": null}', jstr)


    def test_turnout_segment_link_half_null_jstr_eq(self):
        obj1 = self.__sample_turnout_segment_link_half_null()
        jstr = JSONify.dumps(obj1)
        obj2 = TurnoutSegmentLink.construct_from_jdict(json.loads(jstr))
        self.assertEqual(obj2, obj1)


    def test_turnout_segment_link_p0(self):
        obj1 = self.__sample_turnout_segment_link()
        link = obj1.link_for_config(TurnoutPosition.P0)
        self.assertEqual('TrackSegmentLink:{block_label:BN01, segment_label:S02}', str(link))


    def test_turnout_segment_link_p1(self):
        obj1 = self.__sample_turnout_segment_link()
        link = obj1.link_for_config(TurnoutPosition.P1)
        self.assertEqual('TrackSegmentLink:{block_label:BN02, segment_label:S01}', str(link))


    def test_segment_link_track(self):
        obj1 = self.__sample_track_segment_link_1()
        jstr = JSONify.dumps(obj1)
        obj2 = SegmentLink.construct_from_jdict(json.loads(jstr))
        self.assertEqual(obj2, obj1)


    def test_segment_link_turnout(self):
        obj1 = self.__sample_turnout_segment_link()
        jstr = JSONify.dumps(obj1)
        obj2 = SegmentLink.construct_from_jdict(json.loads(jstr))
        self.assertEqual(obj2, obj1)
