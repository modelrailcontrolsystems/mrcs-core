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
from mrcs_core.equipment.turnout.turnout_configuration import TurnoutConfiguration
from mrcs_core.inventory.segment.segment import TrackSegment
from mrcs_core.inventory.segment.segment_link import TrackSegmentLink


# --------------------------------------------------------------------------------------------------------------------

class TestTrackSegment(unittest.TestCase):

    @classmethod
    def __sample_track_segment_link(cls):
        return TrackSegmentLink('BN01', 'S02')


    @classmethod
    def __sample_track_segment(cls):
        label = 'S01'
        length = 60
        up_link = cls.__sample_track_segment_link()
        down_link = None
        return TrackSegment(label, length, up_link, down_link)


    def test_track_segment_str(self):
        obj1 = self.__sample_track_segment()
        self.assertEqual('TrackSegment:{label:S01, length:60, '
                         'up_link:TrackSegmentLink:{block_label:BN01, segment_label:S02}, down_link:None}', str(obj1))


    def test_track_segment_jstr(self):
        obj1 = self.__sample_track_segment()
        jstr = JSONify.dumps(obj1)
        self.assertEqual('{"type": "TrackSegment", "label": "S01", "length": 60, '
                         '"up_link": {"type": "TrackSegmentLink", "link": ["BN01", "S02"]}, "down_link": null}', jstr)


    def test_track_segment_jstr_eq(self):
        obj1 = self.__sample_track_segment()
        jstr = JSONify.dumps(obj1)
        obj2 = TrackSegment.construct_from_jdict(json.loads(jstr))
        self.assertEqual(obj2, obj1)


    def test_track_segment_up_link_for_config(self):
        obj1 = self.__sample_track_segment()
        conf = TurnoutConfiguration({})
        self.assertEqual(obj1.up_link_for_config(conf), self.__sample_track_segment_link())


    def test_track_segment_down_link_for_config(self):
        obj1 = self.__sample_track_segment()
        conf = TurnoutConfiguration({})
        self.assertEqual(obj1.down_link_for_config(conf), None)
