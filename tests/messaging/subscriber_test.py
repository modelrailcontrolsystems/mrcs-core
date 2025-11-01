#!/usr/bin/env python

import json
import sys

from mrcs_core.messaging.subscriber import Subscriber
from mrcs_core.messaging.routing_key import RoutingKey


# --------------------------------------------------------------------------------------------------------------------

def test_callback(ch, method, properties, body):
    jdict = json.loads(body.decode())
    print(f'method:{method}, properties:{properties}, body:{jdict}')

    Subscriber.ack(ch, method)


# --------------------------------------------------------------------------------------------------------------------

subscriber = Subscriber('test_exchange', 'subscriber_test_queue', test_callback)
print(subscriber)

subscriber.connect()
print(subscriber)

routing_key = RoutingKey.construct('src1.seg1.dev1')
print(routing_key)

try:
    subscriber.subscribe(routing_key)
except KeyboardInterrupt:
    print('KeyboardInterrupt', file=sys.stderr)
    sys.exit(0)
