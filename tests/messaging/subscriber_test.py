#!/usr/bin/env python

import logging
import sys

from mrcs_core.data.json import JSONify
from mrcs_core.messaging.message import Message
from mrcs_core.messaging.client import Subscriber
from mrcs_core.messaging.routing_key import RoutingKey
from mrcs_core.sys.logging import Logging


# --------------------------------------------------------------------------------------------------------------------

EXCHANGE_NAME = 'mrcs_test_exchange'
QUEUE_NAME = 'mrcs_test_queue'


# --------------------------------------------------------------------------------------------------------------------

def test_callback(message: Message):
    logger.warning(f'message:{JSONify.dumps(message)}')


# --------------------------------------------------------------------------------------------------------------------

Logging.config('subscriber_test', level=logging.WARNING)
logger = Logging.getLogger()

subscriber = Subscriber(EXCHANGE_NAME, QUEUE_NAME, test_callback)
subscriber.connect()
logger.warning(subscriber)

routing_key1 = RoutingKey.construct('*.seg1.dev1')
logger.warning(routing_key1)

try:
    subscriber.subscribe(routing_key1)
except KeyboardInterrupt:
    print(file=sys.stderr)
    sys.exit(0)
