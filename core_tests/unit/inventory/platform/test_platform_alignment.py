"""
Created on 19 Sep 2026

@author: Bruno Beloff (bbeloff@me.com)

python -m unittest -v unit/inventory/platform/test_platform_alignment.py

https://realpython.com/python-testing/
https://www.jetbrains.com/help/pycharm/creating-tests.html
"""

import unittest

from mrcs_core.data.json import JSONify
from mrcs_core.inventory.platform.platform_alignment import PlatformAlignment


# --------------------------------------------------------------------------------------------------------------------

class TestPlatformAlignment(unittest.TestCase):

    def test_platform_alignment_members(self):
        self.assertEqual(['UP_LEFT', 'UP_RIGHT'], list(PlatformAlignment.keys()))


    def test_platform_alignment_values(self):
        self.assertEqual('LEFT', PlatformAlignment.UP_LEFT.value)
        self.assertEqual('RIGHT', PlatformAlignment.UP_RIGHT.value)


    def test_platform_alignment_construct_from_value(self):
        self.assertEqual(PlatformAlignment.UP_LEFT, PlatformAlignment('LEFT'))
        self.assertEqual(PlatformAlignment.UP_RIGHT, PlatformAlignment('RIGHT'))

        with self.assertRaises(ValueError):
            PlatformAlignment('SIDEWAYS')

        # an island platform is two Platform items, not an alignment of its own
        with self.assertRaises(ValueError):
            PlatformAlignment('BOTH')


    def test_platform_alignment_contains(self):
        self.assertIn('LEFT', PlatformAlignment)
        self.assertIn('RIGHT', PlatformAlignment)

        self.assertNotIn('BOTH', PlatformAlignment)
        self.assertNotIn('SIDEWAYS', PlatformAlignment)
        self.assertNotIn('UP_LEFT', PlatformAlignment)


    def test_platform_alignment_is_a_str(self):
        self.assertIsInstance(PlatformAlignment.UP_LEFT, str)
        self.assertEqual('LEFT', str(PlatformAlignment.UP_LEFT))


    def test_platform_alignment_jstr(self):
        self.assertEqual('"LEFT"', JSONify.dumps(PlatformAlignment.UP_LEFT))
        self.assertEqual('"RIGHT"', JSONify.dumps(PlatformAlignment.UP_RIGHT))


# --------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    unittest.main()
