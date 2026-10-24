"""
Created on 18 Oct 2026

@author: Bruno Beloff (bbeloff@me.com)

python -m unittest -v unit/layout/segment/test_turnout_segment_prolog.py

https://realpython.com/python-testing/
https://www.jetbrains.com/help/pycharm/creating-tests.html
"""

import json
import unittest
from pathlib import Path

from mrcs_core.layout.block.block import Block
from mrcs_core.layout.segment.prolog_link_set import LinkSet


# --------------------------------------------------------------------------------------------------------------------

class TestTurnoutSegmentProlog(unittest.TestCase):
    __block_filename = Path(__file__).parent / 'data' / 'turnout_block.json'
    __block_jdict = None


    @classmethod
    def setUpClass(cls):
        with open(cls.__block_filename) as fp:
            cls.__block_jdict = json.load(fp)


    def test_as_prolog_segment(self):
        block = Block.construct_from_jdict(self.__block_jdict)

        obj2 = block.segment('TW02')
        obj3 = obj2.as_prolog_segment('BN06')
        self.assertEqual('segment(bn06_tw02, 186).', repr(obj3))


    def test_as_prolog_links(self):
        block = Block.construct_from_jdict(self.__block_jdict)
        link_set = LinkSet.construct()

        obj2 = block.segment('TW01')
        obj2.as_prolog_links(link_set, 'BN06')

        self.assertEqual(5, len(link_set))
        self.assertEqual('link(bn06_tw01, bs06_tw01, 9, up, ConfsIn, ConfsOut) :- '
                         'add_conf(tw01-p0, ConfsIn, ConfsOut).', repr(link_set.links[0]))
        self.assertEqual('link(bs06_tw01, bn06_tw01, 9, down, ConfsIn, ConfsOut) :- '
                         'add_conf(tw01-p0, ConfsIn, ConfsOut).', repr(link_set.links[1]))
        self.assertEqual('link(bn06_tw01, bn06_tw02, 0, up, ConfsIn, ConfsOut) :- '
                         'add_conf(tw01-p1, ConfsIn, ConfsOut).', repr(link_set.links[2]))
        self.assertEqual('link(bn06_tw02, bn06_tw01, 0, down, ConfsIn, ConfsOut) :- '
                         'add_conf(tw01-p1, ConfsIn, ConfsOut).', repr(link_set.links[3]))
        self.assertEqual('link(bn06_tw01, bn05_sg01, 0, down, Confs, Confs).', repr(link_set.links[4]))


# --------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    unittest.main()
