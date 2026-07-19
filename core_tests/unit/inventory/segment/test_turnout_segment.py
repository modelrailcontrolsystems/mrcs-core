"""
Created on 11 Jul 2026

@author: Bruno Beloff (bbeloff@me.com)

python -m unittest -v unit/inventory/segment/test_turnout_segment.py

https://realpython.com/python-testing/
https://www.jetbrains.com/help/pycharm/creating-tests.html
"""

import json
import unittest

from mrcs_core.data.json import JSONify
from mrcs_core.equipment.turnout.turnout_configuration import TurnoutConfiguration
from mrcs_core.equipment.turnout.turnout_enums import TurnoutPosition
from mrcs_core.inventory.segment.segment import TurnoutSegment
from mrcs_core.inventory.segment.segment_link import SimpleSegmentLink, SwitchedSegmentLink


# --------------------------------------------------------------------------------------------------------------------

class TestTurnoutSegment(unittest.TestCase):

    @classmethod
    def __sample_simple_segment_link(cls):
        return SimpleSegmentLink('BN01', 'S02')


    @classmethod
    def __sample_switched_segment_link(cls):
        link_p0 = SimpleSegmentLink('BN01', 'S03')
        link_p1 = SimpleSegmentLink('BN02', 'S01')
        return SwitchedSegmentLink(link_p0, link_p1)


    @classmethod
    def __sample_turnout_configuration(cls, position: TurnoutPosition):
        return TurnoutConfiguration({'TN01': position})


    @classmethod
    def __sample_turnout_segment(cls):
        label = 'TN01'
        length = 20
        turnout_address = 123
        switch_is_up = True
        simple_link = cls.__sample_simple_segment_link()
        switched_link = cls.__sample_switched_segment_link()
        return TurnoutSegment(label, length, turnout_address, switch_is_up, simple_link, switched_link)


    def test_turnout_segment_str(self):
        self.maxDiff = None
        obj1 = self.__sample_turnout_segment()
        self.assertEqual('TurnoutSegment:{label:TN01, length:20, turnout_address:123, '
                         'switch_is_up:True, simple_link:SimpleSegmentLink:{block_label:BN01, segment_label:S02}, '
                         'switched_link:SwitchedSegmentLink:{'
                         'link_p0:SimpleSegmentLink:{block_label:BN01, segment_label:S03}, '
                         'link_p1:SimpleSegmentLink:{block_label:BN02, segment_label:S01}}}', str(obj1))


    def test_turnout_segment_jstr(self):
        obj1 = self.__sample_turnout_segment()
        jstr = JSONify.dumps(obj1)
        self.assertEqual('{"type": "TurnoutSegment", "label": "TN01", "length": 20, "addr": 123, '
                         '"switch_is_up": true, "simple": ["BN01", "S02"], '
                         '"switched": {"p0": ["BN01", "S03"], "p1": ["BN02", "S01"]}}', jstr)


    def test_turnout_segment_jstr_eq(self):
        obj1 = self.__sample_turnout_segment()
        jstr = JSONify.dumps(obj1)
        obj2 = TurnoutSegment.construct_from_jdict(json.loads(jstr))
        self.assertEqual(obj2, obj1)


    def test_turnout_segment_up_link_for_config_p0(self):
        obj1 = self.__sample_turnout_segment()
        conf = self.__sample_turnout_configuration(TurnoutPosition.P0)
        self.assertEqual('SimpleSegmentLink:{block_label:BN01, segment_label:S03}',
                         str(obj1.up_link_for_config(conf)))


    def test_turnout_segment_up_link_for_config_p1(self):
        obj1 = self.__sample_turnout_segment()
        conf = self.__sample_turnout_configuration(TurnoutPosition.P1)
        self.assertEqual('SimpleSegmentLink:{block_label:BN02, segment_label:S01}',
                         str(obj1.up_link_for_config(conf)))


    def test_turnout_segment_down_link_for_config_p0(self):
        obj1 = self.__sample_turnout_segment()
        conf = self.__sample_turnout_configuration(TurnoutPosition.P0)
        self.assertEqual('SimpleSegmentLink:{block_label:BN01, segment_label:S02}',
                         str(obj1.down_link_for_config(conf)))


    def test_turnout_segment_down_link_for_config_p1(self):
        obj1 = self.__sample_turnout_segment()
        conf = self.__sample_turnout_configuration(TurnoutPosition.P1)
        self.assertEqual('SimpleSegmentLink:{block_label:BN01, segment_label:S02}',
                         str(obj1.down_link_for_config(conf)))
