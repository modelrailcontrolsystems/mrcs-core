#!/usr/bin/env python

import logging
import sys

from mrcs_core.data.json import JSONify
from mrcs_core.messaging.message import Message
from mrcs_core.messaging.client import Endpoint
from mrcs_core.messaging.routing_key import RoutingKey
from mrcs_core.sys.logging import Logging


# --------------------------------------------------------------------------------------------------------------------

EXCHANGE_NAME = 'mrcs_test_exchange'
QUEUE_NAME = 'mrcs_test1_queue'

IDENTITY = 'src1'


# --------------------------------------------------------------------------------------------------------------------

def test_callback(message: Message):
    logger.warning(f'message:{JSONify.dumps(message)}')

    message = Message.construct(f'{IDENTITY}.seg1.dev1', message.body)

    endpoint.publish(message)
    logger.warning(f'sent {message}')


# --------------------------------------------------------------------------------------------------------------------

Logging.config(f'endpoint_test_{IDENTITY}', level=logging.WARNING)
logger = Logging.getLogger()

endpoint = Endpoint(EXCHANGE_NAME, IDENTITY, QUEUE_NAME, test_callback)
endpoint.connect()
logger.warning(endpoint)

routing_key1 = RoutingKey.construct('src0.seg1.dev1')
logger.warning(routing_key1)

try:
    endpoint.subscribe(routing_key1)
except KeyboardInterrupt:
    print(file=sys.stderr)
    sys.exit(0)
