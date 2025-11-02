#!/usr/bin/env python

from mrcs_core.data.json import JSONify
from mrcs_core.messaging.broker import Broker


# --------------------------------------------------------------------------------------------------------------------

broker = Broker.construct()
print(broker)

exchanges = broker.list_exchanges()

for ex in exchanges:
    print(JSONify.dumps(ex))
