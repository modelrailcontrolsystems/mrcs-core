#!/usr/bin/env python

from mrcs_core.messaging.broker import Broker


# --------------------------------------------------------------------------------------------------------------------

broker = Broker.construct()
print(broker)

exchanges = broker.list_exchanges()

for exchange in exchanges:
    print(exchange)
