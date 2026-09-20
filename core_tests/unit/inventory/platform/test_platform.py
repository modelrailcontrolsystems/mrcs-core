"""
Created on 19 Sep 2026

@author: Bruno Beloff (bbeloff@me.com)

python -m unittest -v unit/inventory/platform/test_platform.py

https://realpython.com/python-testing/
https://www.jetbrains.com/help/pycharm/creating-tests.html
"""

import json
import unittest

from mrcs_core.data.json import JSONify
from mrcs_core.inventory.layout.location import Location
from mrcs_core.inventory.platform.platform import Platform
from mrcs_core.inventory.platform.platform_alignment import PlatformAlignment
from mrcs_core.inventory.platform.platform_label import PlatformLabel


# --------------------------------------------------------------------------------------------------------------------

class TestPlatform(unittest.TestCase):

    @classmethod
    def __sample_platform_1(cls):
        label = PlatformLabel('KGX', 1)
        alignment = PlatformAlignment.UP_LEFT
        origin = Location('BN01', 'S01')
        offset = 150
        length = 1200
        return Platform(label, alignment, origin, offset, length)


    @classmethod
    def __sample_platform_2(cls):
        label = PlatformLabel('KGX', 2)
        alignment = PlatformAlignment.UP_RIGHT
        origin = Location('BN02', 'S01')
        offset = 0
        length = 900
        return Platform(label, alignment, origin, offset, length)


    def test_platform_construct(self):
        obj1 = self.__sample_platform_1()
        self.assertEqual(PlatformLabel('KGX', 1), obj1.label)
        self.assertEqual(PlatformAlignment.UP_LEFT, obj1.alignment)
        self.assertEqual(Location('BN01', 'S01'), obj1.origin)
        self.assertEqual(150, obj1.offset)
        self.assertEqual(1200, obj1.length)


    def test_platform_length_is_a_property(self):
        # unlike Segment.length, Platform.length takes no turnout configuration
        obj1 = self.__sample_platform_1()
        self.assertEqual(1200, obj1.length)


    def test_platform_str(self):
        self.maxDiff = None
        obj1 = self.__sample_platform_1()
        # the alignment is reported by member name, whereas as_json emits its value
        self.assertEqual('Platform:{label:PlatformLabel:{station:KGX, number:1}, alignment:UP_LEFT, '
                         'origin:Location:{block_label:BN01, segment_label:S01}, offset:150, length:1200}',
                         str(obj1))


    def test_platform_as_json(self):
        obj1 = self.__sample_platform_1()
        jdict = obj1.as_json()
        self.assertEqual(PlatformLabel('KGX', 1), jdict['label'])
        self.assertEqual(PlatformAlignment.UP_LEFT, jdict['alignment'])
        self.assertEqual(Location('BN01', 'S01'), jdict['origin'])
        self.assertEqual(150, jdict['offset'])
        self.assertEqual(1200, jdict['length'])


    def test_platform_jstr(self):
        self.maxDiff = None
        obj1 = self.__sample_platform_1()
        jstr = JSONify.dumps(obj1)
        self.assertEqual('{"label": "KGX/1", "alignment": "LEFT", "origin": "BN01/S01", '
                         '"offset": 150, "length": 1200}', jstr)

        obj2 = self.__sample_platform_2()
        self.assertEqual('{"label": "KGX/2", "alignment": "RIGHT", "origin": "BN02/S01", '
                         '"offset": 0, "length": 900}', JSONify.dumps(obj2))


    def test_platform_jstr_eq(self):
        obj1 = self.__sample_platform_1()
        jstr = JSONify.dumps(obj1)
        obj2 = Platform.construct_from_jdict(json.loads(jstr))

        self.assertEqual(obj1, obj2)
        self.assertEqual(obj1.label, obj2.label)
        self.assertEqual(obj1.alignment, obj2.alignment)
        self.assertEqual(obj1.origin, obj2.origin)
        self.assertEqual(obj1.offset, obj2.offset)
        self.assertEqual(obj1.length, obj2.length)


    def test_platform_construct_from_jdict(self):
        jdict = {'label': 'PAD/3', 'alignment': 'RIGHT', 'origin': 'BN04/S02', 'offset': 25, 'length': 750}
        obj1 = Platform.construct_from_jdict(jdict)

        self.assertEqual(PlatformLabel('PAD', 3), obj1.label)
        self.assertEqual(PlatformAlignment.UP_RIGHT, obj1.alignment)
        self.assertEqual(Location('BN04', 'S02'), obj1.origin)
        self.assertEqual(25, obj1.offset)
        self.assertEqual(750, obj1.length)


    def test_platform_construct_from_jdict_invalid_alignment(self):
        jdict = {'label': 'KGX/1', 'alignment': 'SIDEWAYS', 'origin': 'BN01/S01', 'offset': 150, 'length': 1200}

        with self.assertRaises(ValueError):
            Platform.construct_from_jdict(jdict)


    def test_platform_construct_from_jdict_invalid_label(self):
        jdict = {'label': 'KGX', 'alignment': 'LEFT', 'origin': 'BN01/S01', 'offset': 150, 'length': 1200}

        with self.assertRaises(ValueError):
            Platform.construct_from_jdict(jdict)


    def test_platform_construct_from_jdict_invalid_origin(self):
        jdict = {'label': 'KGX/1', 'alignment': 'LEFT', 'origin': 'BN01', 'offset': 150, 'length': 1200}

        with self.assertRaises(ValueError):
            Platform.construct_from_jdict(jdict)


    def test_platform_eq(self):
        obj1 = self.__sample_platform_1()
        obj2 = self.__sample_platform_1()
        self.assertEqual(obj1, obj2)

        # Different label
        self.assertNotEqual(obj1, Platform(PlatformLabel('KGX', 9), PlatformAlignment.UP_LEFT,
                                           Location('BN01', 'S01'), 150, 1200))
        # Different alignment
        self.assertNotEqual(obj1, Platform(PlatformLabel('KGX', 1), PlatformAlignment.UP_RIGHT,
                                           Location('BN01', 'S01'), 150, 1200))
        # Different origin
        self.assertNotEqual(obj1, Platform(PlatformLabel('KGX', 1), PlatformAlignment.UP_LEFT,
                                           Location('BN09', 'S01'), 150, 1200))
        # Different offset
        self.assertNotEqual(obj1, Platform(PlatformLabel('KGX', 1), PlatformAlignment.UP_LEFT,
                                           Location('BN01', 'S01'), 0, 1200))
        # Different length
        self.assertNotEqual(obj1, Platform(PlatformLabel('KGX', 1), PlatformAlignment.UP_LEFT,
                                           Location('BN01', 'S01'), 150, 500))
        # Different type / None
        self.assertNotEqual(obj1, None)
        self.assertNotEqual(obj1, 'KGX/1')


    def test_platform_lt(self):
        obj1 = self.__sample_platform_1()
        obj2 = self.__sample_platform_2()

        # ordered by label
        self.assertTrue(obj1 < obj2)
        self.assertFalse(obj2 < obj1)
        self.assertFalse(obj1 < obj1)


    def test_platform_island_is_two_platforms(self):
        # an island platform is represented by one Platform item per track
        origin = Location('BN01', 'S01')
        up_side = Platform(PlatformLabel('KGX', 1), PlatformAlignment.UP_LEFT, origin, 150, 1200)
        down_side = Platform(PlatformLabel('KGX', 2), PlatformAlignment.UP_RIGHT, origin, 150, 1200)

        self.assertNotEqual(up_side, down_side)
        self.assertEqual(up_side.origin, down_side.origin)
        self.assertEqual([up_side, down_side], sorted([down_side, up_side]))


# --------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    unittest.main()
