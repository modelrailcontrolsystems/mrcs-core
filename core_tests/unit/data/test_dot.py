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

from mrcs_core.data.dot import Dot


# --------------------------------------------------------------------------------------------------------------------

class TestDot(unittest.TestCase):
    __dict_filename = Path(__file__).parent / 'data' / 'dot_dict.json'
    __dict = None


    @classmethod
    def setUpClass(cls):
        with open(cls.__dict_filename) as fp:
            cls.__dict = json.load(fp)


    # path -----------------------------------------------------------------------------------------------------------

    def test_path(self):
        self.assertEqual('a', Dot.path('a'))
        self.assertEqual('c.c1.c100', Dot.path('c', 'c1', 'c100'))


    def test_path_empty(self):
        self.assertEqual('', Dot.path())


    def test_path_non_str(self):
        self.assertEqual('Alpha.1', Dot.path('Alpha', 1))


    # node -----------------------------------------------------------------------------------------------------------

    def test_node_none(self):
        self.assertIsNone(Dot.node(None, 0))
        self.assertIsNone(Dot.node(None, 1))


    def test_node_wildcard(self):
        self.assertIsNone(Dot.node('*', 0))
        self.assertIsNone(Dot.node('*', 1))


    def test_node_level_1(self):
        self.assertEqual('a', Dot.node('a', 0))
        self.assertIsNone(Dot.node('a', 1))


    def test_node_level_2(self):
        self.assertEqual('a', Dot.node('a.a1', 0))
        self.assertEqual('a1', Dot.node('a.a1', 1))
        self.assertIsNone(Dot.node('a.a1', 2))


    # nodes ----------------------------------------------------------------------------------------------------------

    def test_nodes_none(self):
        self.assertEqual([], Dot.nodes(None))


    def test_nodes_wildcard(self):
        self.assertEqual([], Dot.nodes('*'))


    def test_nodes(self):
        self.assertEqual(['a'], Dot.nodes('a'))
        self.assertEqual(['c', 'c1', 'c100'], Dot.nodes('c.c1.c100'))


    def test_nodes_path_round_trip(self):
        nodes = Dot.nodes('c.c1.c100')
        self.assertEqual('c.c1.c100', Dot.path(*nodes))
