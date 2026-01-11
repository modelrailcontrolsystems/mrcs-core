"""
Created on 26 Dec 2025

@author: Bruno Beloff (bbeloff@me.com)

python -m unittest -v operations/test_clock.py

https://realpython.com/python-testing/
https://www.jetbrains.com/help/pycharm/creating-tests.html
https://stackoverflow.com/questions/8047736/how-to-load-data-from-a-file-for-a-unit-test-in-python
"""

import json
import unittest

from mrcs_core.data.equipment_identity import EquipmentIdentifier, EquipmentType
from mrcs_core.data.iso_datetime import ISODatetime
from mrcs_core.data.json import JSONify
from mrcs_core.operations.time.cronjob import Cronjob


# --------------------------------------------------------------------------------------------------------------------

class TestCronjob(unittest.TestCase):

    def test_construct(self):
        target = EquipmentIdentifier(EquipmentType.OSC, None, 1)
        event_id = 'abc'
        on_datetime = ISODatetime(2025, month=12, day=31, hour=6, minute=0)
        obj1 = Cronjob(target, event_id, on_datetime)
        self.assertEqual(obj1.target.equipment_type, EquipmentType.OSC)
        self.assertEqual(obj1.event_id, event_id)
        self.assertEqual(obj1.on_datetime.year, 2025)

    def test_json(self):
        target = EquipmentIdentifier(EquipmentType.OSC, None, 1)
        event_id = 'abc'
        on_datetime = ISODatetime(2025, month=12, day=31, hour=6, minute=0)
        obj1 = Cronjob(target, event_id, on_datetime)
        jstr = JSONify.dumps(obj1)
        obj2 = Cronjob.construct_from_jdict(json.loads(jstr))
        self.assertEqual(obj1, obj2)

    def test_lt(self):
        target = EquipmentIdentifier(EquipmentType.OSC, None, 1)
        on_datetime = ISODatetime(2025, month=12, day=31, hour=6, minute=0)
        obj1 = Cronjob(target, 'abc', on_datetime)
        obj2 = Cronjob(target, 'abd', on_datetime)
        self.assertLess(obj1, obj2)


if __name__ == "__main_":
    unittest.main()
