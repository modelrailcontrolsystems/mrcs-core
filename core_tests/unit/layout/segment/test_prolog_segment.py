"""
Created on 24 Oct 2026

@author: Bruno Beloff (bbeloff@me.com)

python -m unittest -v unit/layout/segment/test_prolog_segment.py

https://realpython.com/python-testing/
https://www.jetbrains.com/help/pycharm/creating-tests.html
"""

import unittest

from mrcs_core.layout.segment.prolog_segment import PrologSegment
from mrcs_core.layout.segment.segment_location import SegmentLocation


# --------------------------------------------------------------------------------------------------------------------

class TestPrologSegment(unittest.TestCase):

    def test_properties(self):
        location = SegmentLocation('BN06', 'TW02')
        obj1 = PrologSegment(location, 186)

        self.assertEqual(location, obj1.location)
        self.assertEqual(186, obj1.length)


    def test_repr(self):
        obj1 = PrologSegment(SegmentLocation('BN06', 'TW02'), 186)
        self.assertEqual('segment(bn06_tw02, 186).', repr(obj1))


    def test_str(self):
        obj1 = PrologSegment(SegmentLocation('BN06', 'TW02'), 186)
        self.assertEqual('PrologSegment:{location:SegmentLocation:{block_label:BN06, segment_label:TW02}, '
                         'length:186}', str(obj1))


    def test_eq(self):
        obj1 = PrologSegment(SegmentLocation('BN06', 'TW02'), 186)
        obj2 = PrologSegment(SegmentLocation('BN06', 'TW02'), 186)
        self.assertTrue(obj1 == obj2)


    def test_neq(self):
        obj1 = PrologSegment(SegmentLocation('BN06', 'TW02'), 186)
        obj2 = PrologSegment(SegmentLocation('BN06', 'TW02'), 187)
        self.assertFalse(obj1 == obj2)


# --------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    unittest.main()
