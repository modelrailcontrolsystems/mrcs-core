"""
Created on 17 Jun 2026

@author: Bruno Beloff (bbeloff@me.com)

python -m unittest -v equipment/block/test_block_status_report.py

https://realpython.com/python-testing/
https://www.jetbrains.com/help/pycharm/creating-tests.html
"""

import json
import unittest

from mrcs_core.equipment.block.block_report import BlockReport


# --------------------------------------------------------------------------------------------------------------------

class TestBlockReport(unittest.TestCase):

    def test_block_report_status(self):
        jstr = '{"type": "BlockStatusReport", "nid": 1, "reporter": 2, "input": 3, "status": "OCCUPIED_OVERLOAD_1"}'

        obj1 = BlockReport.construct_from_jdict(json.loads(jstr))
        self.assertEqual('BlockStatusReport:{network_id:0x0001, reporter_address:2, reporter_input:3, '
                         'status:OCCUPIED_OVERLOAD_1}', str(obj1))


    def test_block_report_occupancy(self):
        jstr = ('{"type": "BlockOccupancyReport", "nid": 1, "reporter": 2, "input": 3, "group": 1, '
                '"occupants": [{"addr": 4660, "face": "REV"}]}')

        obj1 = BlockReport.construct_from_jdict(json.loads(jstr))
        self.assertEqual('BlockOccupancyReport:{network_id:0x0001, reporter_address:2, reporter_input:3, '
                         'occupant_group:1, occupants:[BlockOccupant:{address:4660, face:REV}]}', str(obj1))
