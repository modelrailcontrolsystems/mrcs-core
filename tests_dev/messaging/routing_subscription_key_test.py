#!/usr/bin/env python

import json

from mrcs_core.data.equipment_identity import EquipmentType, EquipmentFilter
from mrcs_core.data.json import JSONify
from mrcs_core.messaging.routing_key import SubscriptionRoutingKey


# --------------------------------------------------------------------------------------------------------------------

subscription_routings = []
subscription_routing_specifications = [
    [
        EquipmentFilter(EquipmentType.SIG, 1, 2),
        EquipmentFilter(None, 1, None)
    ],
    [
        EquipmentFilter(None, None, None),
        EquipmentFilter(EquipmentType.MPU, None, 100)
    ],
    [
        EquipmentFilter(None, None, None),
        EquipmentFilter(EquipmentType.MPU, None, None)
    ],
]

for [equipment_identifier, equipment_filter] in subscription_routing_specifications:
    try:
        routing1 = SubscriptionRoutingKey(equipment_identifier, equipment_filter)
        print(routing1)
        jstr = JSONify.dumps(routing1)
        print(jstr)
        routing2 = SubscriptionRoutingKey.construct_from_jdict(json.loads(jstr))
        print(routing2)
        print(f'equal: {routing1 == routing2}')
        subscription_routings.append(routing1)
        print('-')
    except ValueError as ex:
        print(f'exception: {ex}')
print('-')

print('subscription_routings...')
for subscription_routing in sorted(subscription_routings):
    print(subscription_routing)
