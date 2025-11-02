#!/usr/bin/env python

import logging
import sys

from mrcs_core.messaging.message import Message
from mrcs_core.messaging.subscriber import Subscriber
from mrcs_core.messaging.routing_key import RoutingKey
from mrcs_core.sys.logging import Logging


# --------------------------------------------------------------------------------------------------------------------

def test_callback(message: Message):
    logger.warning(f'message:{message}')


# --------------------------------------------------------------------------------------------------------------------

Logging.config('subscriber_test', level=logging.WARNING)
logger = Logging.getLogger()

subscriber = Subscriber('test_exchange', 'subscriber_test_queue', test_callback)
subscriber.connect()
logger.warning(subscriber)

routing_key1 = RoutingKey.construct('*.seg1.dev1')
logger.warning(routing_key1)

try:
    subscriber.subscribe(routing_key1)
except KeyboardInterrupt:
    print(file=sys.stderr)
    sys.exit(0)
