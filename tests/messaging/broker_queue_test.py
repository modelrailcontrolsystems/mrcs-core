#!/usr/bin/env python

from mrcs_core.messaging.broker import Broker


# --------------------------------------------------------------------------------------------------------------------

broker = Broker.construct()
print(broker)

queues = broker.list_queues()

for queue in queues:
    print(queue)
