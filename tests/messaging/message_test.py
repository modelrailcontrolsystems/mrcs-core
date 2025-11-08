#!/usr/bin/env python

import json

from mrcs_core.data.equipment_identity import EquipmentIdentifier, EquipmentType, EquipmentFilter
from mrcs_core.data.json import JSONify
from mrcs_core.messaging.message import Message
from mrcs_core.messaging.routing_key import PublicationRoutingKey


# --------------------------------------------------------------------------------------------------------------------

source = EquipmentIdentifier(EquipmentType.TST, 1, 2)
target = EquipmentFilter(EquipmentType.MPU, 1, 100)
routing_key = PublicationRoutingKey(source, target)

body = "hello"

message1 = Message(routing_key, body)
print(message1)
jstr1 = JSONify.dumps(message1, indent=4)
print(jstr1)
print('-')

message2 = Message.construct_from_jdict(json.loads(jstr1))
print(message2)

print(f'equal: {message1 == message2}')
