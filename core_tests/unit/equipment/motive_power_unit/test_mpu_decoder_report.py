"""
Created on 1 Jul 2026

@author: Bruno Beloff (bbeloff@me.com)

python -m unittest -v unit/equipment/motive_power_unit/test_mpu_decoder_report.py

https://realpython.com/python-testing/
https://www.jetbrains.com/help/pycharm/creating-tests.html
"""

import json
import unittest

from mrcs_core.data.json import JSONify
from mrcs_core.equipment.motive_power_unit.mpu_decoder_report import MPUDecoderReport


# --------------------------------------------------------------------------------------------------------------------

class TestMPUDecoderReport(unittest.TestCase):

    @staticmethod
    def __sample_mpu_decoder_report():
        address = 0x1234
        receive_count = 456
        error_count = 789
        opts = 0xab
        speed = 90
        qos = 5

        return MPUDecoderReport(address, receive_count, error_count, opts, speed, qos)


    def test_construct_mpu_decoder_report(self):
        obj1 = self.__sample_mpu_decoder_report()
        self.assertEqual('MPUDecoderReport:{address:4660, receive_count:456, error_count:789, opts:0xab, '
                         'speed:90, qos:5}', str(obj1))


    def test_mpu_decoder_report_json(self):
        obj1 = self.__sample_mpu_decoder_report()
        jstr = JSONify.dumps(obj1)
        self.assertEqual('{"type": "MPUDecoderReport", "addr": 4660, "received": 456, "errors": 789, '
                         '"opts": 171, "speed": 90, "qos": 5}', jstr)


    def test_mpu_decoder_report_json_eq(self):
        obj1 = self.__sample_mpu_decoder_report()
        jstr = JSONify.dumps(obj1)
        obj2 = MPUDecoderReport.construct_from_jdict(json.loads(jstr))
        self.assertEqual(obj1, obj2)


    def test_mpu_decoder_report_json_lt(self):
        obj1 = self.__sample_mpu_decoder_report()
        jstr = JSONify.dumps(obj1)
        obj2 = MPUDecoderReport.construct_from_jdict(json.loads(jstr))
        self.assertEqual(obj1 < obj2, False)


# --------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    unittest.main()
