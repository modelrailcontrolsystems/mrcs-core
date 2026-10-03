"""
Created on 2 Sep 2026

@author: Bruno Beloff (bbeloff@me.com)

python -m unittest -v unit/data/test_dot_dict.py

https://realpython.com/python-testing/
https://www.jetbrains.com/help/pycharm/creating-tests.html
"""

import json
import unittest
from pathlib import Path

from mrcs_core.data.dot_dict import DotDict


# --------------------------------------------------------------------------------------------------------------------

class TestDotDict(unittest.TestCase):
    __dict_filename = Path(__file__).parent / 'data' / 'dot_dict.json'
    __dict = None


    @classmethod
    def setUpClass(cls):
        with open(cls.__dict_filename) as fp:
            cls.__dict = json.load(fp)


    # path -----------------------------------------------------------------------------------------------------------

    def test_path(self):
        self.assertEqual('a', DotDict.path('a'))
        self.assertEqual('c.c1.c100', DotDict.path('c', 'c1', 'c100'))


    def test_path_empty(self):
        self.assertEqual('', DotDict.path())


    # node -----------------------------------------------------------------------------------------------------------

    def test_node_none(self):
        self.assertIsNone(DotDict.node(None, 0))
        self.assertIsNone(DotDict.node(None, 1))


    def test_node_wildcard(self):
        self.assertIsNone(DotDict.node('*', 0))
        self.assertIsNone(DotDict.node('*', 1))


    def test_node_level_1(self):
        self.assertEqual('a', DotDict.node('a', 0))
        self.assertIsNone(DotDict.node('a', 1))


    def test_node_level_2(self):
        self.assertEqual('a', DotDict.node('a.a1', 0))
        self.assertEqual('a1', DotDict.node('a.a1', 1))
        self.assertIsNone(DotDict.node('a.a1', 2))


    # nodes ----------------------------------------------------------------------------------------------------------

    def test_nodes_none(self):
        self.assertIsNone(DotDict.nodes(None))


    def test_nodes_wildcard(self):
        self.assertIsNone(DotDict.nodes('*'))


    def test_nodes(self):
        self.assertEqual(['a'], DotDict.nodes('a'))
        self.assertEqual(['c', 'c1', 'c100'], DotDict.nodes('c.c1.c100'))


    def test_nodes_path_round_trip(self):
        nodes = DotDict.nodes('c.c1.c100')
        if nodes is None:
            return
        self.assertEqual('c.c1.c100', DotDict.path(*nodes))


    # item -----------------------------------------------------------------------------------------------------------

    def test_null_path(self):
        obj1 = DotDict(self.__dict)
        self.assertIs(obj1, obj1.item(None))


    def test_wildcard_path(self):
        obj1 = DotDict(self.__dict)
        self.assertIs(obj1, obj1.item('*'))


    def test_path_level_1a(self):
        obj1 = DotDict(self.__dict)
        obj2 = obj1.item('a')
        self.assertEqual("{'a1': 100, 'a2': 200}", str(obj2))


    def test_path_level_1c(self):
        obj1 = DotDict(self.__dict)
        obj2 = obj1.item('c')
        self.assertEqual("{'c1': {'c100': 1100, 'c200': 2100}, 'c2': {'c110': 1100, 'c210': 2100}}", str(obj2))


    def test_path_level_2a(self):
        obj1 = DotDict(self.__dict)
        obj2 = obj1.item('a.a1')
        self.assertEqual("100", str(obj2))


    def test_path_level_2c(self):
        obj1 = DotDict(self.__dict)
        obj2 = obj1.item('c.c1.c100')
        self.assertEqual("1100", str(obj2))


    def test_path_level_1x_fail(self):
        obj1 = DotDict(self.__dict)

        with self.assertRaises(KeyError) as ctx:
            obj1.item('x.a.b')

        self.assertEqual('x', ctx.exception.args[0])


    def test_path_level_2a_fail(self):
        obj1 = DotDict(self.__dict)

        with self.assertRaises(KeyError) as ctx:
            obj1.item('a.a3')

        self.assertEqual('a.a3', ctx.exception.args[0])


    def test_path_level_2c_fail(self):
        obj1 = DotDict(self.__dict)

        with self.assertRaises(KeyError) as ctx:
            obj1.item('c.x.c100')

        self.assertEqual('c.x', ctx.exception.args[0])


    def test_path_level_3c_fail(self):
        obj1 = DotDict(self.__dict)

        with self.assertRaises(KeyError) as ctx:
            obj1.item('c.c1.c100.x')

        self.assertEqual('c.c1.c100.x', ctx.exception.args[0])
