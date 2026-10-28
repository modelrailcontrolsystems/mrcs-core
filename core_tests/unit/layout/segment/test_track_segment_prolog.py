"""
Created on 18 Oct 2026

@author: Bruno Beloff (bbeloff@me.com)

python -m unittest -v unit/layout/segment/test_track_segment_prolog.py

https://realpython.com/python-testing/
https://www.jetbrains.com/help/pycharm/creating-tests.html
"""

import json
import unittest
from pathlib import Path

from mrcs_core.layout.block.block import Block
from mrcs_core.layout.segment.prolog_link_set import LinkSet


# --------------------------------------------------------------------------------------------------------------------

class TestTrackSegmentProlog(unittest.TestCase):
    __block_filename = Path(__file__).parent / 'data' / 'track_block.json'
    __block_jdict = None


    @classmethod
    def setUpClass(cls):
        with open(cls.__block_filename) as fp:
            cls.__block_jdict = json.load(fp)


    def test_as_prolog_segment(self):
        block = Block.construct_from_jdict(self.__block_jdict)

        obj2 = block.segment('SG01')
        obj3 = obj2.as_prolog_segment('BN08')
        self.assertEqual('segment(bn08_sg01, 313).', repr(obj3))


    def test_as_1_prolog_link(self):
        block = Block.construct_from_jdict(self.__block_jdict)
        link_set = LinkSet.new()

        obj2 = block.segment('SG02')
        obj2.as_prolog_links(link_set, 'BN08')
        self.assertEqual(1, len(link_set))
        self.assertEqual('link(bn08_sg02, bn08_sg01, 0, down, Confs, Confs).', repr(link_set.links[0]))


    def test_as_2_prolog_links(self):
        block = Block.construct_from_jdict(self.__block_jdict)
        link_set = LinkSet.new()

        obj2 = block.segment('SG01')
        obj2.as_prolog_links(link_set, 'BN08')
        self.assertEqual(2, len(link_set))
        self.assertEqual('link(bn08_sg01, bn08_sg02, 0, up, Confs, Confs).', repr(link_set.links[0]))
        self.assertEqual('link(bn08_sg01, bn07_sg01, 0, down, Confs, Confs).', repr(link_set.links[1]))


# --------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    unittest.main()
