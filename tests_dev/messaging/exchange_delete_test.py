#!/usr/bin/env python

# Delete queues before deleting exchanges

import logging

from pika.exceptions import AMQPError

from mrcs_core.messaging.broker import Broker
from mrcs_core.messaging.mqclient import MQManager
from mrcs_core.sys.logging import Logging


# --------------------------------------------------------------------------------------------------------------------

Logging.config('exchange_delete_test', level=logging.WARNING)
logger = Logging.getLogger()

broker = Broker.construct()
logger.warning(broker)

manager = MQManager()
manager.connect()
logger.warning(manager)
logger.warning('-')


# --------------------------------------------------------------------------------------------------------------------

try:
    for exchange in broker.list_exchanges():
        if exchange.name.startswith(MQManager.Mode.OPERATIONS) or exchange.name.startswith(MQManager.Mode.TEST):
            logger.warning(exchange)
            manager.exchange_delete(exchange.name)

    manager.close()         # connection is closed automatically on error

except AMQPError as ex:
    logger.error(ex)
