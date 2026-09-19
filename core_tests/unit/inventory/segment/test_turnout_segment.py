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
from mrcs_core.equipment.block.block_enums import BlockHeading
from mrcs_core.equipment.turnout.turnout_configuration import TurnoutConfiguration
from mrcs_core.equipment.turnout.turnout_enums import TurnoutPosition
from mrcs_core.inventory.layout.location import Location
from mrcs_core.inventory.segment.segment import Segment, TurnoutSegment
from mrcs_core.inventory.segment.segment_link import FixedSegmentLink, SwitchedSegmentLink


# --------------------------------------------------------------------------------------------------------------------

class TestTurnoutSegment(unittest.TestCase):

    @classmethod
    def __sample_simple_segment_link(cls):
        return FixedSegmentLink(Location('BN01', 'S02'))


    @classmethod
    def __sample_switched_segment_link(cls):
        return SwitchedSegmentLink(Location('BN01', 'S03'), Location('BN02', 'S01'))


    @classmethod
    def __sample_turnout_configuration(cls, position: TurnoutPosition):
        return TurnoutConfiguration({'TE01': position})


    @classmethod
    def __sample_turnout_segment_1(cls):
        label = 'TN01'
        length = 20
        turnout = 'TE01'
        up_link = cls.__sample_simple_segment_link()
        down_link = cls.__sample_switched_segment_link()
        return TurnoutSegment(label, length, turnout, up_link, down_link)


    @classmethod
    def __sample_turnout_segment_2(cls):
        label = 'TN02'
        length = 25
        turnout = 'TE02'
        up_link = cls.__sample_switched_segment_link()
        down_link = cls.__sample_simple_segment_link()
        return TurnoutSegment(label, length, turnout, up_link, down_link)


    def test_turnout_segment_construct(self):
        obj1 = self.__sample_turnout_segment_1()
        self.assertEqual('TN01', obj1.label)
        self.assertEqual(20, obj1.length)
        self.assertEqual('TE01', obj1.turnout)
        self.assertEqual(self.__sample_simple_segment_link(), obj1.up_link)
        self.assertEqual(self.__sample_switched_segment_link(), obj1.down_link)


    def test_turnout_segment_str(self):
        self.maxDiff = None
        obj1 = self.__sample_turnout_segment_1()
        self.assertEqual('TurnoutSegment:{label:TN01, length:20, turnout:TE01, up_link:FixedSegmentLink:'
                         '{next_location:Location:{block_label:BN01, segment_label:S02}}, '
                         'down_link:SwitchedSegmentLink:{p0_next_location:Location:{block_label:BN01, '
                         'segment_label:S03}, p1_next_location:Location:{block_label:BN02, '
                         'segment_label:S01}}}', str(obj1))


    def test_turnout_segment_as_json(self):
        self.maxDiff = None
        obj1 = self.__sample_turnout_segment_1()
        jdict = obj1.as_json()
        self.assertEqual('TurnoutSegment', jdict['type'])
        self.assertEqual('TN01', jdict['label'])
        self.assertEqual(20, jdict['length'])
        self.assertEqual('TE01', jdict['turnout'])
        self.assertEqual(self.__sample_simple_segment_link(), jdict['up-link'])
        self.assertEqual(self.__sample_switched_segment_link(), jdict['down-link'])


    def test_turnout_segment_jstr(self):
        self.maxDiff = None
        obj1 = self.__sample_turnout_segment_1()
        jstr = JSONify.dumps(obj1)
        self.assertEqual('{"type": "TurnoutSegment", "label": "TN01", "length": 20, "turnout": "TE01", '
                         '"up-link": {"type": "Fixed", "next": ["BN01", "S02"]}, '
                         '"down-link": {"type": "Switched", "p0-next": ["BN01", "S03"], '
                         '"p1-next": ["BN02", "S01"]}}', jstr)


    def test_turnout_segment_jstr_eq(self):
        obj1 = self.__sample_turnout_segment_1()
        jstr = JSONify.dumps(obj1)
        obj2 = TurnoutSegment.construct_from_jdict(json.loads(jstr))
        self.assertEqual(obj2, obj1)


    def test_turnout_segment_construct_from_jdict_invalid_type(self):
        with self.assertRaises(TypeError):
            TurnoutSegment.construct_from_jdict({'type': 'InvalidType'})


    def test_segment_construct_from_jdict(self):
        obj1 = self.__sample_turnout_segment_1()
        jstr = JSONify.dumps(obj1)
        obj2 = Segment.construct_from_jdict(json.loads(jstr))
        self.assertEqual(obj2, obj1)


    def test_turnout_segment_eq(self):
        obj1 = self.__sample_turnout_segment_1()
        obj2 = self.__sample_turnout_segment_1()
        self.assertEqual(obj1, obj2)

        # Different label
        self.assertNotEqual(obj1, TurnoutSegment('TN99', 20, 'TE01', self.__sample_simple_segment_link(),
                                                 self.__sample_switched_segment_link()))
        # Different length
        self.assertNotEqual(obj1, TurnoutSegment('TN01', 50, 'TE01', self.__sample_simple_segment_link(),
                                                 self.__sample_switched_segment_link()))
        # Different turnout
        self.assertNotEqual(obj1, TurnoutSegment('TN01', 20, 'TE99', self.__sample_simple_segment_link(),
                                                 self.__sample_switched_segment_link()))
        # Different up_link
        self.assertNotEqual(obj1, TurnoutSegment('TN01', 20, 'TE01', None, self.__sample_switched_segment_link()))
        # Different down_link
        self.assertNotEqual(obj1, TurnoutSegment('TN01', 20, 'TE01', self.__sample_simple_segment_link(), None))
        # Different type / None
        self.assertNotEqual(obj1, None)
        self.assertNotEqual(obj1, 'TN01')


    def test_turnout_segment_lt(self):
        obj1 = self.__sample_turnout_segment_1()
        obj2 = self.__sample_turnout_segment_2()

        self.assertTrue(obj1 < obj2)
        self.assertFalse(obj2 < obj1)


    def test_turnout_segment_next_location(self):
        obj1 = self.__sample_turnout_segment_1()
        conf_p0 = self.__sample_turnout_configuration(TurnoutPosition.P0)
        conf_p1 = self.__sample_turnout_configuration(TurnoutPosition.P1)

        self.assertEqual(Location('BN01', 'S02'), obj1.next_location(conf_p0, BlockHeading.UP))
        self.assertEqual(Location('BN01', 'S03'), obj1.next_location(conf_p0, BlockHeading.DOWN))
        self.assertEqual(Location('BN02', 'S01'), obj1.next_location(conf_p1, BlockHeading.DOWN))

        with self.assertRaises(ValueError):
            obj1.next_location(conf_p0, BlockHeading.UNASSIGNED)


    def test_turnout_segment_next_up_location(self):
        obj1 = self.__sample_turnout_segment_1()
        conf_p0 = self.__sample_turnout_configuration(TurnoutPosition.P0)
        self.assertEqual(Location('BN01', 'S02'), obj1.next_up_location(conf_p0))

        obj_switched_up = self.__sample_turnout_segment_2()
        conf_te02_p0 = TurnoutConfiguration({'TE02': TurnoutPosition.P0})
        conf_te02_p1 = TurnoutConfiguration({'TE02': TurnoutPosition.P1})
        self.assertEqual(Location('BN01', 'S03'), obj_switched_up.next_up_location(conf_te02_p0))
        self.assertEqual(Location('BN02', 'S01'), obj_switched_up.next_up_location(conf_te02_p1))

        obj_no_link = TurnoutSegment('TN01', 20, 'TE01', None, None)
        self.assertIsNone(obj_no_link.next_up_location(conf_p0))


    def test_turnout_segment_next_down_location(self):
        obj1 = self.__sample_turnout_segment_1()
        conf_p0 = self.__sample_turnout_configuration(TurnoutPosition.P0)
        conf_p1 = self.__sample_turnout_configuration(TurnoutPosition.P1)
        self.assertEqual(Location('BN01', 'S03'), obj1.next_down_location(conf_p0))
        self.assertEqual(Location('BN02', 'S01'), obj1.next_down_location(conf_p1))

        obj_no_link = TurnoutSegment('TN01', 20, 'TE01', None, None)
        self.assertIsNone(obj_no_link.next_down_location(conf_p0))


    def test_turnout_segment_next_locations(self):
        obj1 = self.__sample_turnout_segment_1()
        self.assertEqual([Location('BN01', 'S02')], obj1.next_up_locations())
        self.assertEqual([Location('BN01', 'S03'), Location('BN02', 'S01')], obj1.next_down_locations())
        self.assertEqual([Location('BN01', 'S02'), Location('BN01', 'S03'), Location('BN02', 'S01')],
                         obj1.next_locations())

        obj_no_links = TurnoutSegment('TN01', 20, 'TE01', None, None)
        self.assertEqual([], obj_no_links.next_up_locations())
        self.assertEqual([], obj_no_links.next_down_locations())
        self.assertEqual([], obj_no_links.next_locations())


# --------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    unittest.main()
