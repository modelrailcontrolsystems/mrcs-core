#!/usr/bin/env python

import logging
import sys

from mrcs_core.data.equipment_identity import EquipmentIdentifier, EquipmentType, EquipmentFilter
from mrcs_core.data.json import JSONify
from mrcs_core.messaging.client import Endpoint
from mrcs_core.messaging.message import Message
from mrcs_core.messaging.routing_key import PublicationRoutingKey
from mrcs_core.sys.logging import Logging


# --------------------------------------------------------------------------------------------------------------------

equipment_type = EquipmentType.SIG if sys.argv[1] == 's' else EquipmentType.TST
target_serial_number = None if sys.argv[2] == '*' else int(sys.argv[2])

source = EquipmentIdentifier(equipment_type, 1, 1)
target = EquipmentFilter(EquipmentType.MPU, None, target_serial_number)
routing_key = PublicationRoutingKey(source, target)

body = "hello"


# --------------------------------------------------------------------------------------------------------------------

Logging.config('publisher_test', level=logging.WARNING)
logger = Logging.getLogger()

logger.warning(f'identity: {JSONify.dumps(source)}')

publisher = Endpoint.construct_pub(Endpoint.Mode.TEST)

try:
    publisher.connect()
    logger.warning(publisher)

    message = Message(routing_key, body)

    publisher.publish(message)
    logger.warning(f'sent {message}')

except RuntimeError as ex:
    logger.error(ex)

finally:
    publisher.close()
