"""
Created on 18 Oct 2026

@author: Bruno Beloff (bbeloff@me.com)

python -m unittest -v unit/layout/test_layout_prolog.py

https://realpython.com/python-testing/
https://www.jetbrains.com/help/pycharm/creating-tests.html
"""

import json
import unittest

from pydantic import FilePath

from mrcs_core.layout.layout import Layout
from mrcs_core.layout.segment.segment_location import SegmentLocation


# --------------------------------------------------------------------------------------------------------------------

class TestLayoutProlog(unittest.TestCase):
    __data_dir = FilePath(__file__).parent / 'data'

    __layout = None


    @classmethod
    def setUpClass(cls):
        with open(cls.__data_dir / 'test_001_layout.json') as fp:
            cls.__layout = Layout.construct_from_jdict(json.load(fp), name='test_001')


    def test_segments(self):
        obj1 = self.__layout
        start = SegmentLocation('B01', 'S01')
        end = SegmentLocation('B04', 'S01')
        obj2 = obj1.segment_route(start, end)
        self.assertEqual(1, len(obj2))
        self.assertEqual('Route:{direction:UP{1}, length:450, configuration:TurnoutConfiguration:'
                         '{positions:{S02:P1}}, segments:[SegmentLocation:{block_label:B01, segment_label:S01}, '
                         'SegmentLocation:{block_label:B02, segment_label:S01}, SegmentLocation:{block_label:B02, '
                         'segment_label:S02}, SegmentLocation:{block_label:B04, segment_label:S01}]}', str(obj2[0]))


# --------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    unittest.main()
