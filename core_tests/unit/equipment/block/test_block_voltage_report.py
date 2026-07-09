"""
Created on 17 Jun 2026

@author: Bruno Beloff (bbeloff@me.com)

python -m unittest -v unit/equipment/block/test_block_voltage_report.py

https://realpython.com/python-testing/
https://www.jetbrains.com/help/pycharm/creating-tests.html
"""

import json
import unittest

from mrcs_core.data.json import JSONify
from mrcs_core.equipment.block.block_enums import BlockVoltage
from mrcs_core.equipment.block.block_id import BlockID
from mrcs_core.equipment.block.block_report import BlockVoltageReport


# --------------------------------------------------------------------------------------------------------------------

class TestBlockVoltageReport(unittest.TestCase):

    @staticmethod
    def __sample_block_voltage_report():
        detector_address = 5
        channel = 6
        reporter_id = 0x1234
        block_id = BlockID(detector_address, channel, reporter_id)

        voltage = BlockVoltage.OCCUPIED_OVERLOAD_1

        return BlockVoltageReport(block_id, voltage)


    def test_block_voltage_report_str(self):
        obj1 = self.__sample_block_voltage_report()
        self.assertEqual('BlockVoltageReport:{block_id:BlockID:{detector_address:5, channel:6, '
                         'reporter_id:0x1234}, voltage:OCCUPIED_OVERLOAD_1}', str(obj1))


    def test_block_voltage_report_jstr(self):
        obj1 = self.__sample_block_voltage_report()
        jstr = JSONify.dumps(obj1)
        self.assertEqual('{"type": "BlockVoltageReport", "id": {"addr": 5, "channel": 6, "rid": 4660}, '
                         '"voltage": "OCCUPIED_OVERLOAD_1"}', jstr)


    def test_block_voltage_report_jstr_eq(self):
        obj1 = self.__sample_block_voltage_report()
        jstr = JSONify.dumps(obj1)
        obj2 = BlockVoltageReport.construct_from_jdict(json.loads(jstr))
        self.assertEqual(obj1, obj2)


# --------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    unittest.main()
