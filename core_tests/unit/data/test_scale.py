"""
Created on 7 Nov 2026

@author: Bruno Beloff (bbeloff@me.com)

python -m unittest -v unit/data/test_scale.py

https://realpython.com/python-testing/
https://www.jetbrains.com/help/pycharm/creating-tests.html
"""

import unittest

from mrcs_core.data.scale import Conv, Gauge, Scale


# --------------------------------------------------------------------------------------------------------------------

class TestConv(unittest.TestCase):

    def test_metres_to_kilometres(self):
        self.assertAlmostEqual(1.0, 1000 * Conv.METRES_TO_KILOMETRES)


    def test_metres_to_miles(self):
        # 1 mile = 1609.344 metres
        self.assertAlmostEqual(1.0, 1609.344 * Conv.METRES_TO_MILES, places=6)


    # ----------------------------------------------------------------------------------------------------------------

    def test_ms(self):
        self.assertEqual(10.0, Conv.ms(36.0))


    def test_ms_rounded(self):
        self.assertEqual(27.778, Conv.ms(100.0))


    def test_ms_zero(self):
        self.assertEqual(0.0, Conv.ms(0.0))


    def test_ms_roundtrip(self):
        for kph in [0.0, 5.0, 36.0, 100.0, 125.5, 200.0]:
            ms = Conv.ms(kph)
            self.assertAlmostEqual(kph, ms * 3.6, places=2)


# --------------------------------------------------------------------------------------------------------------------

class TestGauge(unittest.TestCase):

    def test_gauge_values(self):
        self.assertEqual([45, 76, 120, 148], [gauge.value for gauge in Gauge.items()])


    def test_gauge_contains(self):
        self.assertTrue(76 in Gauge)
        self.assertFalse(87 in Gauge)


    def test_gauge_construct_from_value(self):
        self.assertEqual(Gauge.OO, Gauge(76))


    # ----------------------------------------------------------------------------------------------------------------

    def test_gauge_kilometres(self):
        self.assertAlmostEqual(0.1, Gauge.OO.kilometres(1.0))


    def test_gauge_kilometres_n(self):
        self.assertAlmostEqual(1.5, Gauge.N.kilometres(10.0))


    def test_gauge_kilometres_zero(self):
        self.assertEqual(0.0, Gauge.OO.kilometres(0.0))


    def test_gauge_miles(self):
        self.assertAlmostEqual(0.0, Gauge.OO.miles(1.0))


    def test_gauge_miles_one_real_mile(self):
        # one real-world mile in OO is 1609.344 / 76 model metres
        self.assertAlmostEqual(1.0, Gauge.OO.miles(1609.344 / 76), places=6)


# --------------------------------------------------------------------------------------------------------------------

class TestScale(unittest.TestCase):

    def test_scale_values(self):
        self.assertEqual([45, 76, 87, 120, 148], [scale.value for scale in Scale.items()])


    def test_scale_contains(self):
        self.assertTrue(87 in Scale)
        self.assertFalse(100 in Scale)


    def test_scale_construct_from_value(self):
        self.assertEqual(Scale.HO, Scale(87))


    # ----------------------------------------------------------------------------------------------------------------

    def test_scale_kph(self):
        self.assertAlmostEqual(273.6, Scale.OO.kph(1.0))


    def test_scale_kph_ho(self):
        self.assertAlmostEqual(313.2, Scale.HO.kph(1.0))


    def test_scale_kph_zero(self):
        self.assertEqual(0.0, Scale.OO.kph(0.0))


    def test_scale_mph(self):
        self.assertAlmostEqual(170.0, Scale.OO.mph(1.0))


    def test_scale_mph_n(self):
        self.assertAlmostEqual(33.1, Scale.N.mph(0.1))


# --------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    unittest.main()
