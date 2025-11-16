"""
Created on 15 Nov 2025

@author: Bruno Beloff (bbeloff@me.com)

python -m unittest -v data/test_iso_datetime.py

https://realpython.com/python-testing/
https://www.jetbrains.com/help/pycharm/creating-tests.html
"""

import json
import unittest

from mrcs_core.data.iso_datetime import ISODatetime


# --------------------------------------------------------------------------------------------------------------------

class TestISODatetime(unittest.TestCase):
    def test_construct_from_none_jdict(self):
        obj1 = ISODatetime.construct_from_jdict({})
        self.assertEqual(None, obj1)

    def test_construct_from_jdict(self):
        obj1 = ISODatetime.construct_from_jdict(json.loads('"2025-08-26T01:23:45.678+01:00"'))
        self.assertEqual('ISODatetime:{2025-08-26T01:23:45.678+01:00}', str(obj1))

    def test_construct_from_db(self):
        obj1 = ISODatetime.construct_from_db('2025-08-26 01:23:45.678')
        self.assertEqual('ISODatetime:{2025-08-26T02:23:45.678+01:00}', str(obj1))

    def test_eq(self):
        obj1 = ISODatetime.construct_from_jdict(json.loads('"2025-08-26T01:23:45.678+01:00"'))
        obj2 = ISODatetime.construct_from_jdict(json.loads('"2025-08-26T01:23:45.678+01:00"'))
        self.assertEqual(True, obj1 == obj2)

    def test_neq(self):
        obj1 = ISODatetime.construct_from_jdict(json.loads('"2025-08-26T01:23:45.678+01:00"'))
        obj2 = ISODatetime.construct_from_jdict(json.loads('"2025-08-26T01:23:45.678+02:00"'))
        self.assertEqual(False, obj1 == obj2)

    def test_lt(self):
        obj1 = ISODatetime.construct_from_jdict(json.loads('"2025-08-26T01:23:45.678+01:00"'))
        obj2 = ISODatetime.construct_from_jdict(json.loads('"2025-08-26T01:23:45.678+02:00"'))
        self.assertEqual(False, obj1 < obj2)

    def test_nlt(self):
        obj2 = ISODatetime.construct_from_jdict(json.loads('"2025-08-26T01:23:45.678+02:00"'))
        obj1 = ISODatetime.construct_from_jdict(json.loads('"2025-08-26T01:23:45.678+01:00"'))
        self.assertEqual(False, obj1 < obj2)

    def test_dbformat(self):
        obj1 = ISODatetime.construct_from_jdict(json.loads('"2025-08-26T01:23:45.678+01:00"'))
        self.assertEqual('2025-08-26 00:23:45.678', obj1.dbformat())

    def test_as_json(self):
        obj1 = ISODatetime.construct_from_jdict(json.loads('"2025-08-26T01:23:45.678+01:00"'))
        self.assertEqual('2025-08-26T01:23:45.678+01:00', obj1.as_json())


if __name__ == "__main_":
    unittest.main()
