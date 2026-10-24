"""
Created on 24 Sep 2026

@author: Bruno Beloff (bbeloff@me.com)

python -m unittest -v unit/layout/test_route.py

https://realpython.com/python-testing/
https://www.jetbrains.com/help/pycharm/creating-tests.html
"""

import json
import unittest

from mrcs_core.data.json import JSONify
from mrcs_core.layout.route import Route


# --------------------------------------------------------------------------------------------------------------------

class TestRoute(unittest.TestCase):

    @classmethod
    def __sample_prolog_route(cls):
        pdict = {'truth': True, 'Dir': 'down', 'Length': 2314,
                 'ConfOut': [('te01', 'p0'), ('te02', 'p0'), ('tw01', 'p0'), ('tw02', 'p0')],
                 'Route': ['bs07_sg01', 'bs06_sg02', 'bs06_tw01', 'bn06_tw02', 'bn06_sg01', 'bn05_sg01', 'bn04_sg02',
                           'bn04_te02', 'bs02_te01', 'bs02_sg01', 'bs01_sg01']}
        return pdict


    # ----------------------------------------------------------------------------------------------------------------

    def test_route_construct_from_prolog(self):
        pdict = self.__sample_prolog_route()
        obj1 = Route.construct_from_prolog(pdict)
        self.assertEqual('Route:{direction:DOWN{2}, length:2314, configuration:TurnoutConfiguration:{positions:'
                         '{TE01:P0, TE02:P0, TW01:P0, TW02:P0}}, segments:['
                         'SegmentLocation:{block_label:BS07, segment_label:SG01}, '
                         'SegmentLocation:{block_label:BS06, segment_label:SG02}, '
                         'SegmentLocation:{block_label:BS06, segment_label:TW01}, '
                         'SegmentLocation:{block_label:BN06, segment_label:TW02}, '
                         'SegmentLocation:{block_label:BN06, segment_label:SG01}, '
                         'SegmentLocation:{block_label:BN05, segment_label:SG01}, '
                         'SegmentLocation:{block_label:BN04, segment_label:SG02}, '
                         'SegmentLocation:{block_label:BN04, segment_label:TE02}, '
                         'SegmentLocation:{block_label:BS02, segment_label:TE01}, '
                         'SegmentLocation:{block_label:BS02, segment_label:SG01}, '
                         'SegmentLocation:{block_label:BS01, segment_label:SG01}]}', str(obj1))


    def test_route_json(self):
        pdict = self.__sample_prolog_route()
        obj1 = Route.construct_from_prolog(pdict)
        jstr = JSONify.dumps(obj1)
        self.assertEqual('{"direction": "DOWN", "length": 2314, "conf": {"TE01": "P0", "TE02": "P0", "TW01": "P0", '
                         '"TW02": "P0"}, "segments": ["BS07.SG01", "BS06.SG02", "BS06.TW01", "BN06.TW02", "BN06.SG01", '
                         '"BN05.SG01", "BN04.SG02", "BN04.TE02", "BS02.TE01", "BS02.SG01", "BS01.SG01"]}', jstr)


    def test_route_json_eq(self):
        pdict = self.__sample_prolog_route()
        obj1 = Route.construct_from_prolog(pdict)
        jstr = JSONify.dumps(obj1)
        obj2 = Route.construct_from_jdict(json.loads(jstr))
        self.assertEqual(obj1, obj2)


# --------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    unittest.main()
