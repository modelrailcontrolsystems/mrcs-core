#!/usr/bin/env python

import logging
import sys

from mrcs_core.data.equipment_identity import EquipmentIdentifier, EquipmentFilter, EquipmentType
from mrcs_core.data.json import JSONify
from mrcs_core.messaging.client import Endpoint
from mrcs_core.messaging.message import Message
from mrcs_core.messaging.routing_key import SubscriptionRoutingKey
from mrcs_core.sys.logging import Logging


# --------------------------------------------------------------------------------------------------------------------

serial_number = None if sys.argv[1] == '*' else int(sys.argv[1])

QUEUE_NAME = 'mrcs_test1_queue'

identity = EquipmentIdentifier(EquipmentType.MPU, None, serial_number)

source_filter = EquipmentFilter(EquipmentType.SIG, 1, None)
target_filter = EquipmentFilter(EquipmentType.MPU, None, None)


# --------------------------------------------------------------------------------------------------------------------

def test_callback(message: Message):
    if message.routing_key.matches(routing_key1):
        logger.warning("message from route 1")

    if message.routing_key.matches(routing_key2):
        logger.warning("message from route 2")

    source = message.routing_key.source
    logger.warning(f'source:{JSONify.dumps(source)}')


# --------------------------------------------------------------------------------------------------------------------

Logging.config(f'endpoint_test_{identity.as_json()}', level=logging.WARNING)
logger = Logging.getLogger()

queue_suffix = sys.argv[1]
logger.warning(f'queue_suffix:{queue_suffix}')

endpoint = Endpoint.construct_sub(Endpoint.Mode.TEST, identity, test_callback)
endpoint.connect()
logger.warning(endpoint)

routing_key1 = SubscriptionRoutingKey(EquipmentFilter.all(), identity)
logger.warning(f'subscription: {JSONify.dumps(routing_key1)}')

routing_key2 = SubscriptionRoutingKey(source_filter, target_filter)
logger.warning(f'subscription: {JSONify.dumps(routing_key2)}')

try:
    endpoint.subscribe(routing_key1, routing_key2)
except KeyboardInterrupt:
    print(file=sys.stderr)
    sys.exit(0)
