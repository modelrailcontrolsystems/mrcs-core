"""
Created on 7 Oct 2026

@author: Bruno Beloff (bbeloff@me.com)

python -m unittest -v unit/equipment/configuration_variable/test_cv_report.py

https://realpython.com/python-testing/
https://www.jetbrains.com/help/pycharm/creating-tests.html
"""

import json
import unittest

from mrcs_core.data.json import JSONify
from mrcs_core.equipment.conviguration_variable.cv_report import CVReport


# --------------------------------------------------------------------------------------------------------------------

class TestCVReport(unittest.TestCase):

    def test_cv_report_str(self):
        obj1 = CVReport(1, 2)
        self.assertEqual('CVReport:{cv_address:1, value:2}', str(obj1))


    def test_cv_report_lt(self):
        obj1 = CVReport(1, 2)
        obj2 = CVReport(2, 1)
        self.assertTrue(obj1 < obj2)


    def test_cv_report_jstr(self):
        obj1 = CVReport(1, 2)
        jstr = JSONify.dumps(obj1)
        self.assertEqual('{"type": "CVReport", "addr": 1, "value": 2}', jstr)


    def test_cv_report_jstr_round_trip(self):
        obj1 = CVReport(1, 2)
        jstr = JSONify.dumps(obj1)
        obj2 = CVReport.construct_from_jdict(json.loads(jstr))
        self.assertEqual(obj1, obj2)


# --------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    unittest.main()
