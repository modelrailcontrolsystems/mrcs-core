"""
Created on 24 Oct 2026

@author: Bruno Beloff (bbeloff@me.com)

python -m unittest -v unit/layout/segment/test_prolog_link_set.py

https://realpython.com/python-testing/
https://www.jetbrains.com/help/pycharm/creating-tests.html
"""

import unittest

from mrcs_core.equipment.block.block_enums import BlockHeading
from mrcs_core.equipment.turnout.turnout_enums import TurnoutPosition
from mrcs_core.layout.segment.prolog_link import PrologLink, PrologLinkConstraint
from mrcs_core.layout.segment.prolog_link_set import LinkSet
from mrcs_core.layout.segment.segment_location import SegmentLocation


# --------------------------------------------------------------------------------------------------------------------

class TestPrologLink(unittest.TestCase):

    @classmethod
    def __sample_link_0(cls):
        location = SegmentLocation('BN06', 'TW01')
        next_location = SegmentLocation('BS06', 'TW02')

        return PrologLink(location, next_location, BlockHeading.UP)


    @classmethod
    def __sample_link_1(cls):
        location = SegmentLocation('BN06', 'TW01')
        next_location = SegmentLocation('BS06', 'TW02')
        constraint = PrologLinkConstraint(location, TurnoutPosition.P0, 9)

        return PrologLink(location, next_location, BlockHeading.UP, constraint)


    @classmethod
    def __sample_link_2(cls):
        location = SegmentLocation('BN06', 'TW01')
        next_location = SegmentLocation('BS06', 'TW02')
        constraint_1 = PrologLinkConstraint(location, TurnoutPosition.P0, 9)
        constraint_2 = PrologLinkConstraint(next_location, TurnoutPosition.P0, 9)

        return PrologLink(location, next_location, BlockHeading.UP, constraint_1, constraint_2)


    def test_link_str_1(self):
        link_set = LinkSet.new()
        obj1 = self.__sample_link_1()
        link_set.add(obj1)
        self.assertEqual('PrologLinkSet:{links:{LinkSetKey:{start:SegmentLocation:{block_label:BN06, '
                         'segment_label:TW01}, end:SegmentLocation:{block_label:BS06, segment_label:TW02}}: '
                         'PrologLink:{location:SegmentLocation:{block_label:BN06, segment_label:TW01}, '
                         'next_location:SegmentLocation:{block_label:BS06, segment_label:TW02}, heading:UP{1}, '
                         'constraints:[PrologLinkConstraint:{location:SegmentLocation:{block_label:BN06, '
                         'segment_label:TW01}, position:P0{1}, length:9}]}}', str(link_set))


    def test_link_eq(self):
        self.maxDiff = None
        obj1 = self.__sample_link_1()
        link_set_1 = LinkSet.new()
        link_set_1.add(obj1)
        link_set_2 = LinkSet.new()
        link_set_2.add(obj1)

        self.assertTrue(link_set_1 == link_set_2)


    def test_link_neq(self):
        self.maxDiff = None
        obj1 = self.__sample_link_1()
        link_set_1 = LinkSet.new()
        link_set_1.add(obj1)

        obj2 = self.__sample_link_2()
        link_set_2 = LinkSet.new()
        link_set_2.add(obj2)

        self.assertFalse(link_set_1 == link_set_2)


# --------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    unittest.main()
