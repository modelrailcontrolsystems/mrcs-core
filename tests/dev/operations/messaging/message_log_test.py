#!/usr/bin/env python

# https://www.sqlitetutorial.net/sqlite-python/creating-tables/

import logging

from mrcs_core.data.equipment_identity import EquipmentIdentifier, EquipmentType, EquipmentFilter
from mrcs_core.data.json import JSONify
from mrcs_core.messaging.message import Message
from mrcs_core.messaging.routing_key import PublicationRoutingKey
from mrcs_core.operations.message.message_record import MessageRecord
from mrcs_core.sys.logging import Logging


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

id = message.save()
print(f'id:{id}')
print('-')

result = MessageRecord.find(id)
print(result)
print('-')

for message in MessageRecord.find_all():
    print(message)
print('-')

message = MessageRecord.find(id)
print(JSONify.dumps(message))

# message.save()
