"""
Created on 27 Oct 2026

@author: Bruno Beloff (bbeloff@me.com)

python -m unittest -v unit/data/test_csv.py

https://realpython.com/python-testing/
https://www.jetbrains.com/help/pycharm/creating-tests.html
"""

import os.path
import unittest

from mrcs_core.data.csv import CSV
from mrcs_core.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

class TestCSV(unittest.TestCase):

    @classmethod
    def __test_dir(cls):
        return os.path.join(Host.mrcs_abs_dir(), Host.test_dir())


    @classmethod
    def __test_abs_filename(cls):
        return os.path.join(cls.__test_dir(), 'test_csv_1.csv')


    @classmethod
    def setUpClass(cls):
        try:
            os.mkdir(cls.__test_dir())
        except FileExistsError:
            pass


    @classmethod
    def tearDownClass(cls):
        try:
            os.remove(cls.__test_abs_filename())
        except FileNotFoundError:
            pass


    def setUp(self):
        try:
            abs_filename = os.path.join(Host.mrcs_abs_dir(), Host.test_dir(), 'test_csv_1.csv')
            os.remove(abs_filename)
        except FileNotFoundError:
            pass


    @classmethod
    def __sample_dict_initial_array_1(cls):
        return [
            {'a': 1, 'b': 'one', 'c': '', 'd': None, 'e': 1.1},
            {'a': 2, 'b': 'two', 'c': '', 'd': None, 'e': 2.2}
        ]


    @classmethod
    def __sample_dict_initial_array_2(cls):
        return [
            {'a': 3, 'b': 'three', 'c': '', 'd': None, 'e': 3.3},
            {'a': 4, 'b': 'four', 'c': '', 'd': None, 'e': 4.4}
        ]


    @classmethod
    def __sample_dict_final_array_1(cls):
        return [
            {'a': 1.0, 'b': 'one', 'c': '', 'd': None, 'e': 1.1},
            {'a': 2.0, 'b': 'two', 'c': '', 'd': None, 'e': 2.2}
        ]


    @classmethod
    def __sample_dict_final_array_2(cls):
        return [
            {'a': 1.0, 'b': 'one', 'c': '', 'd': None, 'e': 1.1},
            {'a': 2.0, 'b': 'two', 'c': '', 'd': None, 'e': 2.2},
            {'a': 3.0, 'b': 'three', 'c': '', 'd': None, 'e': 3.3},
            {'a': 4.0, 'b': 'four', 'c': '', 'd': None, 'e': 4.4}
        ]


    # ----------------------------------------------------------------------------------------------------------------

    def test_csv_write(self):
        data1 = self.__sample_dict_initial_array_1()
        abs_filename = os.path.join(Host.mrcs_abs_dir(), Host.test_dir(), 'test_csv_1.csv')
        CSV.write(data1, filename=abs_filename)
        data2 = CSV.read(filename=abs_filename)
        self.assertEqual(self.__sample_dict_final_array_1(), data2)


    def test_csv_write_empty(self):
        data1 = []
        abs_filename = self.__test_abs_filename()
        CSV.write(data1, filename=abs_filename)
        data2 = CSV.read(filename=abs_filename)
        self.assertEqual([], data2)


    def test_csv_append(self):
        abs_filename = self.__test_abs_filename()
        CSV.write(self.__sample_dict_initial_array_1(), filename=abs_filename)
        CSV.write(self.__sample_dict_initial_array_2(), filename=abs_filename, append=True)
        data2 = CSV.read(filename=abs_filename)
        self.assertEqual(self.__sample_dict_final_array_2(), data2)


# --------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    unittest.main()
