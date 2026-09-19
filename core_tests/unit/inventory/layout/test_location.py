"""
Created on 12 Sep 2026

@author: Bruno Beloff (bbeloff@me.com)

python -m unittest -v unit/inventory/layout/test_location.py

https://realpython.com/python-testing/
https://www.jetbrains.com/help/pycharm/creating-tests.html
"""

import json
import unittest

from mrcs_core.data.json import JSONify
from mrcs_core.inventory.layout.location import Location


# --------------------------------------------------------------------------------------------------------------------

class TestLocation(unittest.TestCase):

    @classmethod
    def __sample_location_1(cls):
        return Location('BN01', 'S01')


    @classmethod
    def __sample_location_2(cls):
        return Location('BN01', 'S02')


    @classmethod
    def __sample_location_3(cls):
        return Location('BN02', 'S01')


    def test_location_construct(self):
        obj1 = self.__sample_location_1()
        self.assertEqual('BN01', obj1.block_label)
        self.assertEqual('S01', obj1.segment_label)


    def test_location_str(self):
        obj1 = self.__sample_location_1()
        self.assertEqual('Location:{block_label:BN01, segment_label:S01}', str(obj1))


    def test_location_as_json(self):
        obj1 = self.__sample_location_1()
        self.assertEqual(['BN01', 'S01'], obj1.as_json())


    def test_location_jstr(self):
        obj1 = self.__sample_location_1()
        jstr = JSONify.dumps(obj1)
        self.assertEqual('["BN01", "S01"]', jstr)


    def test_location_jstr_eq(self):
        obj1 = self.__sample_location_1()
        jstr = JSONify.dumps(obj1)
        obj2 = Location.construct_from_jdict(json.loads(jstr))
        self.assertEqual(obj1, obj2)


    def test_location_hash(self):
        obj1 = self.__sample_location_1()
        obj2 = self.__sample_location_1()
        obj3 = self.__sample_location_2()
        obj4 = self.__sample_location_3()

        self.assertEqual(hash(obj1), hash(obj2))

        self.assertNotEqual(hash(obj1), hash(obj3))
        self.assertNotEqual(hash(obj1), hash(obj4))


    def test_location_eq(self):
        obj1 = self.__sample_location_1()
        obj2 = self.__sample_location_1()
        self.assertTrue(obj1 == obj2)


    def test_location_neq(self):
        obj1 = self.__sample_location_1()
        obj2 = self.__sample_location_2()
        obj3 = self.__sample_location_3()

        self.assertFalse(obj1 == obj2)
        self.assertFalse(obj1 == obj3)
        self.assertFalse(obj1 is None)
        self.assertFalse(obj1 == 'BN01:S01')


    def test_location_lt(self):
        obj1 = self.__sample_location_1()
        obj2 = self.__sample_location_2()
        obj3 = self.__sample_location_3()

        self.assertTrue(obj1 < obj2)
        self.assertTrue(obj1 < obj3)
        self.assertTrue(obj2 < obj3)

        self.assertFalse(obj2 < obj1)
        self.assertFalse(obj3 < obj1)
        self.assertFalse(obj3 < obj2)
        self.assertFalse(obj1 < obj1)


# --------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    unittest.main()
