"""
Created on 17 Jun 2026

@author: Bruno Beloff (bbeloff@me.com)

python -m unittest -v unit/equipment/block/test_block_status_report.py

https://realpython.com/python-testing/
https://www.jetbrains.com/help/pycharm/creating-tests.html
"""

import json
import unittest

from mrcs_core.data.json import JSONify
from mrcs_core.equipment.block.block_report import BlockStatusReport
from mrcs_core.equipment.block.block_status import BlockStatus


# --------------------------------------------------------------------------------------------------------------------

class TestBlockStatusReport(unittest.TestCase):

    def test_block_status_report(self):
        network_id = 1
        reporter_address = 2
        reporter_input = 3
        status = BlockStatus.OCCUPIED_OVERLOAD_1

        obj1 = BlockStatusReport(network_id, reporter_address, reporter_input, status)
        self.assertEqual(network_id, obj1.network_id)
        self.assertEqual(reporter_address, obj1.reporter_address)
        self.assertEqual(reporter_input, obj1.reporter_input)
        self.assertEqual(status, obj1.status)


    def test_block_status_report_str(self):
        network_id = 1
        reporter_address = 2
        reporter_input = 3
        status = BlockStatus.OCCUPIED_OVERLOAD_1

        obj1 = BlockStatusReport(network_id, reporter_address, reporter_input, status)
        self.assertEqual('BlockStatusReport:{network_id:0x0001, reporter_address:2, reporter_input:3, '
                         'status:OCCUPIED_OVERLOAD_1}', str(obj1))


    def test_block_status_report_jstr(self):
        network_id = 1
        reporter_address = 2
        reporter_input = 3
        status = BlockStatus.OCCUPIED_OVERLOAD_1

        obj1 = BlockStatusReport(network_id, reporter_address, reporter_input, status)
        jstr = JSONify.dumps(obj1)
        self.assertEqual('{"type": "BlockStatusReport", "nid": 1, "reporter": 2, "input": 3, '
                         '"status": "OCCUPIED_OVERLOAD_1"}', jstr)


    def test_control_router_jstr_eq(self):
        network_id = 1
        reporter_address = 2
        reporter_input = 3
        status = BlockStatus.OCCUPIED_OVERLOAD_1

        obj1 = BlockStatusReport(network_id, reporter_address, reporter_input, status)
        jstr = JSONify.dumps(obj1)
        obj2 = BlockStatusReport.construct_from_jdict(json.loads(jstr))
        self.assertEqual(obj1, obj2)


# --------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    unittest.main()
