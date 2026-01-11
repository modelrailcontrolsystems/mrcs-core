"""
Created on 8 Jan 2025

@author: Bruno Beloff (bbeloff@me.com)

python -m unittest -v operations/test_message_record.py

https://realpython.com/python-testing/
https://www.jetbrains.com/help/pycharm/creating-tests.html
https://stackoverflow.com/questions/8047736/how-to-load-data-from-a-file-for-a-unit-test-in-python
"""

import json
import unittest

from mrcs_core.data.equipment_identity import EquipmentIdentifier, EquipmentType, EquipmentFilter
from mrcs_core.data.iso_datetime import ISODatetime
from mrcs_core.data.json import JSONify
from mrcs_core.messaging.routing_key import PublicationRoutingKey
from mrcs_core.operations.recorder.message_record import MessageRecord


# --------------------------------------------------------------------------------------------------------------------

class TestMessageRecord(unittest.TestCase):

    def test_construct(self):
        source = EquipmentIdentifier(EquipmentType.OSC, None, 1)
        target = EquipmentFilter(EquipmentType.ICO, None, None)
        body = {'field': 'test'}
        rec = ISODatetime(2025, month=12, day=31, hour=6, minute=0)
        routing_key = PublicationRoutingKey(source, target)
        obj1 = MessageRecord(1, rec, routing_key, body)

        self.assertEqual(str(obj1), "MessageRecord:{uid:1, rec:ISODatetime:{2025-12-31T06:00:00.000+00:00}, "
                                    "routing_key:PublicationRoutingKey:{source:EquipmentIdentifier:{"
                                    "equipment_type:SCH, sector_number:None, serial_number:1}, "
                                    "target:EquipmentFilter:{equipment_type:CRN, sector_number:None, "
                                    "serial_number:None}}, body:{'field': 'test'}}")

    def test_json(self):
        source = EquipmentIdentifier(EquipmentType.OSC, None, 1)
        target = EquipmentFilter(EquipmentType.ICO, None, None)
        body = {'field': 'test'}
        rec = ISODatetime(2025, month=12, day=31, hour=6, minute=0)
        routing_key = PublicationRoutingKey(source, target)
        obj1 = MessageRecord(1, rec, routing_key, body)
        jstr = JSONify.dumps(obj1)

        self.assertEqual(jstr, '{"uid": 1, "rec": "2025-12-31T06:00:00.000+00:00", '
                               '"routing": "SCH.*.001.CRN.*.*", "body": {"field": "test"}}')

        obj2 = MessageRecord.construct_from_jdict(json.loads(jstr))
        self.assertEqual(obj1, obj2)


if __name__ == "__main_":
    unittest.main()
