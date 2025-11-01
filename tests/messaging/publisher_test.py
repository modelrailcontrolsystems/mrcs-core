#!/usr/bin/env python
from pyexpat.errors import messages

from mrcs_core.data.json import JSONify
from mrcs_core.messaging.publisher import Publisher
from mrcs_core.messaging.routing_key import RoutingKey


# --------------------------------------------------------------------------------------------------------------------

publisher = Publisher('test_exchange')
print(publisher)

publisher.connect()
print(publisher)

routing_key = RoutingKey.construct('src1.seg1.dev1')
print(routing_key)

message = "hello"
publisher.publish(routing_key, message)

print(f" [x] Sent {routing_key}:{message}")

publisher.close()

