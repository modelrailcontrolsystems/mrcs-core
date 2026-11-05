"""
Created on 1 Nov 2026

@author: Bruno Beloff (bbeloff@me.com)

python -m unittest -v unit/data/test_linear_regression.py

https://realpython.com/python-testing/
https://www.jetbrains.com/help/pycharm/creating-tests.html
"""

import unittest

from mrcs_core.data.linear_regression import LinearRegression


# --------------------------------------------------------------------------------------------------------------------

class TestLinearRegression(unittest.TestCase):

    @classmethod
    def __sample_exact_data(cls):
        # y = 2x + 1
        return [(0.0, 1.0), (1.0, 3.0), (2.0, 5.0), (3.0, 7.0)]


    @classmethod
    def __sample_scattered_data(cls):
        # least squares fit: y = 0.6x + 2.2
        return [(1.0, 2.0), (2.0, 4.0), (3.0, 5.0), (4.0, 4.0), (5.0, 5.0)]


    # ----------------------------------------------------------------------------------------------------------------

    def test_len(self):
        regression = LinearRegression(self.__sample_exact_data())
        self.assertEqual(4, len(regression))


    def test_len_empty(self):
        regression = LinearRegression([])
        self.assertEqual(0, len(regression))


    def test_data(self):
        data = self.__sample_exact_data()
        regression = LinearRegression(data)
        self.assertEqual(data, regression.data)


    def test_str(self):
        regression = LinearRegression([(0.0, 1.0), (1.0, 3.0)])
        self.assertEqual('LinearRegression:{data:[(0.0, 1.0), (1.0, 3.0)]}', str(regression))


    # ----------------------------------------------------------------------------------------------------------------

    def test_fit_exact(self):
        slope, intercept = LinearRegression(self.__sample_exact_data()).fit()
        self.assertAlmostEqual(2.0, slope)
        self.assertAlmostEqual(1.0, intercept)


    def test_fit_scattered(self):
        slope, intercept = LinearRegression(self.__sample_scattered_data()).fit()
        self.assertAlmostEqual(0.6, slope)
        self.assertAlmostEqual(2.2, intercept)


    def test_fit_two_points(self):
        slope, intercept = LinearRegression([(1.0, 1.0), (3.0, 5.0)]).fit()
        self.assertAlmostEqual(2.0, slope)
        self.assertAlmostEqual(-1.0, intercept)


    def test_fit_negative_slope(self):
        slope, intercept = LinearRegression([(0.0, 10.0), (1.0, 7.0), (2.0, 4.0)]).fit()
        self.assertAlmostEqual(-3.0, slope)
        self.assertAlmostEqual(10.0, intercept)


    def test_fit_horizontal(self):
        slope, intercept = LinearRegression([(0.0, 4.0), (1.0, 4.0), (2.0, 4.0)]).fit()
        self.assertAlmostEqual(0.0, slope)
        self.assertAlmostEqual(4.0, intercept)


    def test_fit_unordered(self):
        data = self.__sample_scattered_data()
        slope1, intercept1 = LinearRegression(data).fit()
        slope2, intercept2 = LinearRegression(list(reversed(data))).fit()
        self.assertAlmostEqual(slope1, slope2)
        self.assertAlmostEqual(intercept1, intercept2)


    def test_fit_int_data(self):
        slope, intercept = LinearRegression([(0, 1), (1, 3), (2, 5)]).fit()
        self.assertAlmostEqual(2.0, slope)
        self.assertAlmostEqual(1.0, intercept)


    # ----------------------------------------------------------------------------------------------------------------

    def test_fit_empty(self):
        with self.assertRaises(ValueError):
            LinearRegression([]).fit()


    def test_fit_single_point(self):
        with self.assertRaises(ValueError):
            LinearRegression([(1.0, 2.0)]).fit()


    def test_fit_vertical(self):
        with self.assertRaises(ValueError):
            LinearRegression([(1.0, 1.0), (1.0, 2.0), (1.0, 3.0)]).fit()


    def test_fit_vertical_inexact(self):
        # 0.3 is not exactly representable, so the sums do not cancel to zero
        with self.assertRaises(ValueError):
            LinearRegression([(0.3, 1.0), (0.3, 2.0), (0.3, 3.0)]).fit()


# --------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    unittest.main()
