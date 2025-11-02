#!/usr/bin/env python

from mrcs_core.data.json import JSONify
from mrcs_core.messaging.broker import Broker


# --------------------------------------------------------------------------------------------------------------------

broker = Broker.construct()
print(broker)

queues = broker.list_queues()

for q in queues:
    print(q)
    print(JSONify.dumps(q))
    print('-')
