"""
Created on 24 Oct 2026

@author: Bruno Beloff (bbeloff@me.com)

python -m unittest -v unit/layout/segment/test_prolog_link.py

https://realpython.com/python-testing/
https://www.jetbrains.com/help/pycharm/creating-tests.html
"""

import unittest

from mrcs_core.equipment.block.block_enums import BlockHeading
from mrcs_core.equipment.turnout.turnout_enums import TurnoutPosition
from mrcs_core.layout.segment.prolog_link import PrologLink, PrologLinkConstraint
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
        self.maxDiff = None
        obj1 = self.__sample_link_1()
        self.assertEqual('PrologLink:{location:SegmentLocation:{block_label:BN06, segment_label:TW01}, '
                         'next_location:SegmentLocation:{block_label:BS06, segment_label:TW02}, heading:UP{1}, '
                         'constraints:[PrologLinkConstraint:{location:SegmentLocation:{block_label:BN06, '
                         'segment_label:TW01}, position:P0{1}, length:9}]}', str(obj1))


    def test_link_str_2(self):
        self.maxDiff = None
        obj1 = self.__sample_link_2()
        self.assertEqual('PrologLink:{location:SegmentLocation:{block_label:BN06, segment_label:TW01}, '
                         'next_location:SegmentLocation:{block_label:BS06, segment_label:TW02}, heading:UP{1}, '
                         'constraints:[PrologLinkConstraint:{location:SegmentLocation:{block_label:BN06, '
                         'segment_label:TW01}, position:P0{1}, length:9}, '
                         'PrologLinkConstraint:{location:SegmentLocation:{block_label:BS06, segment_label:TW02}, '
                         'position:P0{1}, length:9}]}', str(obj1))


    def test_link_eq(self):
        obj1 = self.__sample_link_1()
        obj2 = self.__sample_link_1()
        self.assertTrue(obj1 == obj2)


    def test_link_neq(self):
        obj1 = self.__sample_link_1()
        obj2 = self.__sample_link_2()
        self.assertFalse(obj1 == obj2)


    def test_link_prolog_0(self):
        obj1 = self.__sample_link_0()
        self.assertEqual('link(bn06_tw01, bs06_tw02, 0, up, Confs, Confs).', repr(obj1))


    def test_link_prolog_1(self):
        obj1 = self.__sample_link_1()
        self.assertEqual('link(bn06_tw01, bs06_tw02, 9, up, ConfsIn, ConfsOut) :- '
                         'add_conf(tw01-p0, ConfsIn, ConfsOut).', repr(obj1))


    def test_link_prolog_2(self):
        obj1 = self.__sample_link_2()
        self.assertEqual('link(bn06_tw01, bs06_tw02, 18, up, ConfsIn, ConfsOut) :- '
                         'add_conf(tw02-p0, ConfsIn, ConfsMid), add_conf(tw01-p0, ConfsMid, ConfsOut).', repr(obj1))


# --------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    unittest.main()
