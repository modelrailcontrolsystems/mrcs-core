"""
Created on 19 Oct 2026

@author: Bruno Beloff (bbeloff@me.com)

python -m unittest -v unit/layout/block/test_block_prolog.py

https://realpython.com/python-testing/
https://www.jetbrains.com/help/pycharm/creating-tests.html
"""

import json
import unittest
from pathlib import Path

from mrcs_core.layout.block.block import Block
from mrcs_core.layout.segment.prolog_link_set import LinkSet


# --------------------------------------------------------------------------------------------------------------------

class TestBlockProlog(unittest.TestCase):
    __block_filename = Path(__file__).parent / 'data' / 'turnout_block.json'
    __block_jdict = None


    @classmethod
    def setUpClass(cls):
        with open(cls.__block_filename) as fp:
            cls.__block_jdict = json.load(fp)


    def test_as_prolog_segments_str(self):
        block = Block.construct_from_jdict(self.__block_jdict)
        prolog = block.as_prolog_segments()
        self.assertEqual(2, len(prolog))
        self.assertEqual('PrologSegment:{location:SegmentLocation:{block_label:BN06, segment_label:TW01}, '
                         'length:186}', str(prolog[0]))
        self.assertEqual('PrologSegment:{location:SegmentLocation:{block_label:BN06, segment_label:TW02}, '
                         'length:186}', str(prolog[1]))


    def test_as_prolog_segments_repr(self):
        block = Block.construct_from_jdict(self.__block_jdict)
        prolog = block.as_prolog_segments()
        self.assertEqual(2, len(prolog))
        self.assertEqual('segment(bn06_tw01, 186).', repr(prolog[0]))
        self.assertEqual('segment(bn06_tw02, 186).', repr(prolog[1]))


    def test_as_prolog_links_str(self):
        block = Block.construct_from_jdict(self.__block_jdict)
        link_set = LinkSet.new()

        block.as_prolog_links(link_set)
        self.assertEqual(8, len(link_set))
        self.assertEqual('PrologLink:{location:SegmentLocation:{block_label:BN06, segment_label:TW01}, '
                         'next_location:SegmentLocation:{block_label:BS06, segment_label:TW01}, heading:UP{1}, '
                         'constraints:[PrologLinkConstraint:{location:SegmentLocation:{block_label:BN06, '
                         'segment_label:TW01}, position:P0{1}, length:9}]}', str(link_set.links[0]))
        self.assertEqual('PrologLink:{location:SegmentLocation:{block_label:BS06, segment_label:TW01}, '
                         'next_location:SegmentLocation:{block_label:BN06, segment_label:TW01}, heading:DOWN{2}, '
                         'constraints:[PrologLinkConstraint:{location:SegmentLocation:{block_label:BN06, '
                         'segment_label:TW01}, position:P0{1}, length:9}]}', str(link_set.links[1]))
        self.assertEqual('PrologLink:{location:SegmentLocation:{block_label:BN06, segment_label:TW01}, '
                         'next_location:SegmentLocation:{block_label:BN06, segment_label:TW02}, heading:UP{1}, '
                         'constraints:[PrologLinkConstraint:{location:SegmentLocation:{block_label:BN06, '
                         'segment_label:TW01}, position:P1{2}, length:0}, PrologLinkConstraint:{location:'
                         'SegmentLocation:{block_label:BN06, segment_label:TW02}, position:P1{2}, length:0}]}',
                         str(link_set.links[2]))
        self.assertEqual('PrologLink:{location:SegmentLocation:{block_label:BN06, segment_label:TW02}, '
                         'next_location:SegmentLocation:{block_label:BN06, segment_label:TW01}, heading:DOWN{2}, '
                         'constraints:[PrologLinkConstraint:{location:SegmentLocation:{block_label:BN06, '
                         'segment_label:TW01}, position:P1{2}, length:0}, PrologLinkConstraint:{location:'
                         'SegmentLocation:{block_label:BN06, segment_label:TW02}, position:P1{2}, length:0}]}',
                         str(link_set.links[3]))
        self.assertEqual('PrologLink:{location:SegmentLocation:{block_label:BN06, segment_label:TW01}, '
                         'next_location:SegmentLocation:{block_label:BN05, segment_label:SG01}, heading:DOWN{2}, '
                         'constraints:[]}', str(link_set.links[4]))
        self.assertEqual('PrologLink:{location:SegmentLocation:{block_label:BN06, segment_label:TW02}, '
                         'next_location:SegmentLocation:{block_label:BN07, segment_label:SG01}, heading:UP{1}, '
                         'constraints:[]}', str(link_set.links[5]))
        self.assertEqual('PrologLink:{location:SegmentLocation:{block_label:BN06, segment_label:TW02}, '
                         'next_location:SegmentLocation:{block_label:BS07, segment_label:TW03}, heading:DOWN{2}, '
                         'constraints:[PrologLinkConstraint:{location:SegmentLocation:{block_label:BN06, '
                         'segment_label:TW02}, position:P0{1}, length:9}]}', str(link_set.links[6]))
        self.assertEqual('PrologLink:{location:SegmentLocation:{block_label:BS07, segment_label:TW03}, '
                         'next_location:SegmentLocation:{block_label:BN06, segment_label:TW02}, heading:UP{1}, '
                         'constraints:[PrologLinkConstraint:{location:SegmentLocation:{block_label:BN06, '
                         'segment_label:TW02}, position:P0{1}, length:9}]}', str(link_set.links[7]))


    def test_as_prolog_links_repr(self):
        block = Block.construct_from_jdict(self.__block_jdict)
        link_set = LinkSet.new()

        block.as_prolog_links(link_set)
        self.assertEqual(8, len(link_set))
        self.assertEqual('link(bn06_tw01, bs06_tw01, 9, up, ConfsIn, ConfsOut) :- '
                         'add_conf(tw01-p0, ConfsIn, ConfsOut).', repr(link_set.links[0]))
        self.assertEqual('link(bs06_tw01, bn06_tw01, 9, down, ConfsIn, ConfsOut) :- '
                         'add_conf(tw01-p0, ConfsIn, ConfsOut).', repr(link_set.links[1]))
        self.assertEqual('link(bn06_tw01, bn06_tw02, 0, up, ConfsIn, ConfsOut) :- '
                         'add_conf(tw02-p1, ConfsIn, ConfsMid), add_conf(tw01-p1, ConfsMid, ConfsOut).',
                         repr(link_set.links[2]))
        self.assertEqual('link(bn06_tw02, bn06_tw01, 0, down, ConfsIn, ConfsOut) :- '
                         'add_conf(tw02-p1, ConfsIn, ConfsMid), add_conf(tw01-p1, ConfsMid, ConfsOut).',
                         repr(link_set.links[3]))
        self.assertEqual('link(bn06_tw01, bn05_sg01, 0, down, Confs, Confs).', repr(link_set.links[4]))
        self.assertEqual('link(bn06_tw02, bn07_sg01, 0, up, Confs, Confs).', repr(link_set.links[5]))
        self.assertEqual('link(bn06_tw02, bs07_tw03, 9, down, ConfsIn, ConfsOut) :- '
                         'add_conf(tw02-p0, ConfsIn, ConfsOut).', repr(link_set.links[6]))
        self.assertEqual('link(bs07_tw03, bn06_tw02, 9, up, ConfsIn, ConfsOut) :- '
                         'add_conf(tw02-p0, ConfsIn, ConfsOut).', repr(link_set.links[7]))
