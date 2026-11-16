"""
Created on 15 Nov 2026

@author: Bruno Beloff (bbeloff@me.com)

python -m unittest -v unit/operations/alert/test_alert.py

https://realpython.com/python-testing/
https://www.jetbrains.com/help/pycharm/creating-tests.html
"""

import json
import unittest

from mrcs_core.data.iso_datetime import ISODatetime
from mrcs_core.data.json import JSONify
from mrcs_core.equipment.alert.alert import Alert
from mrcs_core.equipment.alert.alert_enums import Impact, Severity, Subject


# --------------------------------------------------------------------------------------------------------------------

class TestAlert(unittest.TestCase):

    @classmethod
    def __sample_alert(cls):
        raised_at = ISODatetime.construct_from_jdict('2026-11-15T08:43:56.970+00:00')
        return Alert(None, Severity.HIGH, Impact.GLOBAL, Subject.TRACK, 'short happened', raised_at, None)


    # ----------------------------------------------------------------------------------------------------------------

    def test_construct(self):
        obj1 = self.__sample_alert()
        self.assertEqual('Alert:{id:None, severity:HIGH{0}, impact:GLOBAL, subject:TRACK, text:short happened, '
                         'raised_at:ISODatetime:{2026-11-15T08:43:56.970+00:00}, resolved_at:None}', str(obj1))


    def test_constructor(self):
        obj1 = Alert.construct(Severity.HIGH, Impact.GLOBAL, Subject.TRACK, 'short happened')
        self.assertEqual('HIGH{0}', str(obj1.severity))
        self.assertEqual('GLOBAL', str(obj1.impact))
        self.assertEqual('TRACK', str(obj1.subject))
        self.assertEqual('short happened', str(obj1.text))


    def test_json(self):
        obj1 = self.__sample_alert()
        jstr = JSONify.dumps(obj1)
        self.assertEqual('{"type": "Alert", "id": null, "severity": "HIGH", "impact": "GLOBAL", '
                         '"subject": "TRACK", "text": "short happened", "raised": "2026-11-15T08:43:56.970+00:00", '
                         '"resolved": null}', jstr)


    def test_json_eq(self):
        obj1 = self.__sample_alert()
        jstr = JSONify.dumps(obj1)
        obj2 = Alert.construct_from_jdict(json.loads(jstr))
        self.assertTrue(obj1 == obj2)


    def test_resolve(self):
        obj1 = self.__sample_alert()
        obj1.resolve()
        self.assertIsNotNone(obj1.resolved_at)


    def test_json_neq(self):
        obj1 = self.__sample_alert()
        jstr = JSONify.dumps(obj1)
        obj2 = Alert.construct_from_jdict(json.loads(jstr))
        obj2.resolve()
        self.assertFalse(obj1 == obj2)


    def test_lt(self):
        obj1 = self.__sample_alert()
        obj2 = Alert.construct(Severity.HIGH, Impact.GLOBAL, Subject.TRACK, 'short happened')
        self.assertTrue(obj1 < obj2)


# --------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    unittest.main()
