#!/usr/bin/env python

import json

from mrcs_core.data.equipment_identity import EquipmentIdentifier, EquipmentType, EquipmentFilter
from mrcs_core.data.json import JSONify
from mrcs_core.messaging.routing_key import PublicationRoutingKey


# --------------------------------------------------------------------------------------------------------------------

publication_routings = []
publication_routing_specifications = [
    [
        EquipmentIdentifier(EquipmentType.MPU, None, 100),
        EquipmentFilter(None, 1, None)
    ],
    [
        EquipmentIdentifier(EquipmentType.SIG, 1, 2),
        EquipmentFilter(None, 1, None)
    ],
    [
        EquipmentIdentifier(EquipmentType.SIG, 1, 2),
        EquipmentFilter(EquipmentType.MPU, 1, None)
    ],
    [
        EquipmentIdentifier(EquipmentType.VIS, 1, 1),
        EquipmentFilter(EquipmentType.MPU, 1, None)
    ],
]

for [equipment_identifier, equipment_filter] in publication_routing_specifications:
    try:
        routing1 = PublicationRoutingKey(equipment_identifier, equipment_filter)
        print(routing1)
        jstr = JSONify.dumps(routing1)
        print(jstr)
        routing2 = PublicationRoutingKey.construct_from_jdict(json.loads(jstr))
        print(routing2)
        print(f'equal: {routing1 == routing2}')
        publication_routings.append(routing1)
        print('-')
    except ValueError as ex:
        print(f'exception: {ex}')
print('=')

print('publication_routings...')
for publication_routing in sorted(publication_routings):
    print(publication_routing)
