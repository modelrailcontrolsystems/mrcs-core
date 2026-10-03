"""
Created on 3 Oct 2026

@author: Bruno Beloff (bbeloff@me.com)

python -m unittest -v unit/inventory/station/test_station.py

https://realpython.com/python-testing/
https://www.jetbrains.com/help/pycharm/creating-tests.html
"""

import json
import unittest
from collections import OrderedDict

from mrcs_core.data.json import JSONify
from mrcs_core.inventory.platform.platform import Platform
from mrcs_core.inventory.platform.platform_alignment import PlatformAlignment
from mrcs_core.inventory.segment.segment_location import SegmentLocation
from mrcs_core.inventory.station.station import Station


# --------------------------------------------------------------------------------------------------------------------

class TestStation(unittest.TestCase):

    @classmethod
    def __sample_station_1(cls):
        p1 = Platform(1, PlatformAlignment.UP_RIGHT, SegmentLocation('BS01', 'SG01'), 0, 100)
        p2 = Platform(2, PlatformAlignment.UP_RIGHT, SegmentLocation('BN01', 'SG01'), 0, 100)
        return Station('Alpha', OrderedDict({1: p1, 2: p2}))


    @classmethod
    def __sample_station_2(cls):
        p1 = Platform(1, PlatformAlignment.UP_RIGHT, SegmentLocation('BS04', 'SG01'), 0, 100)
        p2 = Platform(2, PlatformAlignment.UP_RIGHT, SegmentLocation('BN04', 'SG01'), 0, 100)
        return Station('Beta', OrderedDict({1: p1, 2: p2}))


    def test_station_construct(self):
        obj1 = self.__sample_station_1()
        self.assertEqual('Station:{label:Alpha, platforms:[Platform:{label:1, alignment:UP_RIGHT, '
                         'origin:SegmentLocation:{block_label:BS01, segment_label:SG01}, offset:0, length:100}, '
                         'Platform:{label:2, alignment:UP_RIGHT, origin:SegmentLocation:{block_label:BN01, '
                         'segment_label:SG01}, offset:0, length:100}]}', str(obj1))


    def test_station_json(self):
        obj1 = self.__sample_station_1()
        obj2 = JSONify.dumps(obj1)
        self.assertEqual('{"label": "Alpha", "platforms": [{"label": 1, "alignment": "RIGHT", "origin": '
                         '"BS01.SG01", "offset": 0, "length": 100}, {"label": 2, "alignment": "RIGHT", "origin": '
                         '"BN01.SG01", "offset": 0, "length": 100}]}', obj2)


    def test_station_json_rountrip(self):
        obj1 = self.__sample_station_1()
        obj2 = JSONify.dumps(obj1)
        obj3 = Station.construct_from_jdict(json.loads(obj2))
        self.assertEqual(obj1, obj3)


    def test_eq(self):
        obj1 = self.__sample_station_1()
        obj2 = self.__sample_station_1()
        self.assertEqual(obj1, obj2)


    def test_neq(self):
        obj1 = self.__sample_station_1()
        obj2 = self.__sample_station_2()
        self.assertNotEqual(obj1, obj2)


    def test_lt(self):
        obj1 = self.__sample_station_1()
        obj2 = self.__sample_station_2()
        self.assertLess(obj1, obj2)
