#!/usr/bin/env python

from mrcs_core.data.json import JSONify
from mrcs_core.messaging.routing_key import RoutingKey


# --------------------------------------------------------------------------------------------------------------------

routings = [
    'VIS001.SEC001.SIG001',
    '*.SEC001.SIG001',
    '.SEC001.SIG001',
]

for routing in routings:
    try:
        key = RoutingKey.construct(routing)
        print(f'source:{key.source}, sector:{key.sector}, device:{key.device}')
        print(JSONify.dumps(key))
        print('-')
    except ValueError as ex:
        print(f'exception: {ex}')
print('-')

key = RoutingKey.construct_for_all()
print(f'source:{key.source}, sector:{key.sector}, device:{key.device}')
