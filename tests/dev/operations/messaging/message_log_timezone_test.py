#!/usr/bin/env python

"""
2025-10-26 00:30:00.00  - BST
2025-10-26 01:00:00.00  - BST
2025-10-26 01:30:00.00  - BST
2025-10-26 02:00:00.00  - GMT
2025-10-26 02:30:00.00  - GMT
2025-10-26 03:00:00.00  - GMT

https://www.sqlitetutorial.net/sqlite-python/creating-tables/
"""

import logging

from mrcs_core.data.equipment_identity import EquipmentIdentifier, EquipmentType, EquipmentFilter
from mrcs_core.messaging.message import Message
from mrcs_core.messaging.routing_key import PublicationRoutingKey
from mrcs_core.operations.message.message_record import MessageRecord
from mrcs_core.sys.logging import Logging


# --------------------------------------------------------------------------------------------------------------------

recs = [
    '2025-10-26 00:00:00.123',
    '2025-10-26 00:30:00.123',
    '2025-10-26 01:00:00.123',
    '2025-10-26 01:30:00.123',
    '2025-10-26 02:00:00.123',
]

# --------------------------------------------------------------------------------------------------------------------

Logging.config('db_connection_test', level=logging.INFO)
logger = Logging.getLogger()

Message.drop_tables()
Message.create_tables()

source = EquipmentIdentifier(EquipmentType.TST, 1, 2)
target = EquipmentFilter(None, None, None)
routing_key = PublicationRoutingKey(source, target)
message = Message(routing_key, {"greeting": "hello"})
print(message)
print('-')


for rec in recs:
    id = Message.test_insert(rec, message)
    print(f'id:{id}')


for message in MessageRecord.find_all():
    print(message)

"""
expected:
2025-10-26T01:00:00.123+01:00
2025-10-26T01:30:00.123+01:00
2025-10-26T01:00:00.123+00:00
2025-10-26T01:30:00.123+00:00
2025-10-26T02:00:00.123+00:00
"""
