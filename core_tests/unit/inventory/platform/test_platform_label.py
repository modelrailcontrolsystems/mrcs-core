"""
Created on 19 Sep 2026

@author: Bruno Beloff (bbeloff@me.com)

python -m unittest -v unit/inventory/platform/test_platform_label.py

https://realpython.com/python-testing/
https://www.jetbrains.com/help/pycharm/creating-tests.html
"""

import json
import unittest

from mrcs_core.data.json import JSONify
from mrcs_core.inventory.platform.platform_label import PlatformLabel


# --------------------------------------------------------------------------------------------------------------------

class TestPlatformLabel(unittest.TestCase):

    @classmethod
    def __sample_platform_label_1(cls):
        return PlatformLabel('KGX', 1)


    @classmethod
    def __sample_platform_label_2(cls):
        return PlatformLabel('KGX', 2)


    @classmethod
    def __sample_platform_label_3(cls):
        return PlatformLabel('PAD', 1)


    def test_platform_label_construct(self):
        obj1 = self.__sample_platform_label_1()
        self.assertEqual('KGX', obj1.station)
        self.assertEqual(1, obj1.number)


    def test_platform_label_shortform(self):
        self.assertEqual('KGX/1', self.__sample_platform_label_1().shortform)
        self.assertEqual('KGX/12', PlatformLabel('KGX', 12).shortform)


    def test_platform_label_construct_from_shortform(self):
        self.assertEqual(self.__sample_platform_label_1(), PlatformLabel.construct_from_shortform('KGX/1'))
        self.assertEqual(PlatformLabel('KGX', 12), PlatformLabel.construct_from_shortform('KGX/12'))

        # the number is parsed as an int, not kept as a string
        self.assertIsInstance(PlatformLabel.construct_from_shortform('KGX/1').number, int)


    def test_platform_label_shortform_round_trip(self):
        obj1 = self.__sample_platform_label_1()
        self.assertEqual(obj1, PlatformLabel.construct_from_shortform(obj1.shortform))


    def test_platform_label_construct_from_shortform_malformed(self):
        for malformed in ('KGX', 'KGX/1/2', '', '/1', 'KGX/'):
            with self.assertRaises(ValueError):
                PlatformLabel.construct_from_shortform(malformed)

        # a non-numeric platform number
        with self.assertRaises(ValueError):
            PlatformLabel.construct_from_shortform('KGX/A')


    def test_platform_label_construct_from_jdict(self):
        self.assertEqual(self.__sample_platform_label_1(), PlatformLabel.construct_from_jdict('KGX/1'))
        self.assertEqual(PlatformLabel('KGX', 12), PlatformLabel.construct_from_jdict('KGX/12'))

        # the number is parsed as an int, not kept as a string
        self.assertIsInstance(PlatformLabel.construct_from_jdict('KGX/1').number, int)


    def test_platform_label_construct_from_jdict_malformed(self):
        for malformed in ('KGX', 'KGX/1/2', ''):
            with self.assertRaises(ValueError):
                PlatformLabel.construct_from_jdict(malformed)

        # a non-numeric platform number
        with self.assertRaises(ValueError):
            PlatformLabel.construct_from_jdict('KGX/A')


    def test_platform_label_str(self):
        obj1 = self.__sample_platform_label_1()
        self.assertEqual('PlatformLabel:{station:KGX, number:1}', str(obj1))


    def test_platform_label_as_json(self):
        obj1 = self.__sample_platform_label_1()
        self.assertEqual('KGX/1', obj1.as_json())


    def test_platform_label_jstr(self):
        obj1 = self.__sample_platform_label_1()
        self.assertEqual('"KGX/1"', JSONify.dumps(obj1))


    def test_platform_label_jstr_eq(self):
        obj1 = self.__sample_platform_label_1()
        jstr = JSONify.dumps(obj1)
        obj2 = PlatformLabel.construct_from_jdict(json.loads(jstr))
        self.assertEqual(obj1, obj2)


    def test_platform_label_eq(self):
        obj1 = self.__sample_platform_label_1()
        obj2 = self.__sample_platform_label_1()
        self.assertEqual(obj1, obj2)

        # Different station
        self.assertNotEqual(obj1, self.__sample_platform_label_3())
        # Different number
        self.assertNotEqual(obj1, self.__sample_platform_label_2())
        # Different type / None
        self.assertNotEqual(obj1, None)
        self.assertNotEqual(obj1, 'KGX/1')


    def test_platform_label_hash(self):
        obj1 = self.__sample_platform_label_1()
        obj2 = self.__sample_platform_label_1()
        obj3 = self.__sample_platform_label_2()
        obj4 = self.__sample_platform_label_3()

        self.assertEqual(hash(obj1), hash(obj2))

        self.assertNotEqual(hash(obj1), hash(obj3))
        self.assertNotEqual(hash(obj1), hash(obj4))


    def test_platform_label_as_dict_key(self):
        # Layout keys its platforms by PlatformLabel, so an equal label must find the same entry
        labels = {self.__sample_platform_label_1(): 'one', self.__sample_platform_label_2(): 'two'}

        self.assertEqual('one', labels[PlatformLabel('KGX', 1)])
        self.assertEqual('two', labels[PlatformLabel('KGX', 2)])
        self.assertNotIn(PlatformLabel('KGX', 9), labels)


    def test_platform_label_lt(self):
        obj1 = self.__sample_platform_label_1()
        obj2 = self.__sample_platform_label_2()
        obj3 = self.__sample_platform_label_3()

        # same station, ordered by number
        self.assertTrue(obj1 < obj2)
        self.assertFalse(obj2 < obj1)

        # different station, ordered by station
        self.assertTrue(obj1 < obj3)
        self.assertFalse(obj3 < obj1)
        self.assertTrue(obj2 < obj3)
        self.assertFalse(obj3 < obj2)

        self.assertFalse(obj1 < obj1)


    def test_platform_label_sorted(self):
        obj1 = self.__sample_platform_label_1()
        obj2 = self.__sample_platform_label_2()
        obj3 = self.__sample_platform_label_3()

        self.assertEqual([obj1, obj2, obj3], sorted([obj3, obj2, obj1]))


# --------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    unittest.main()
