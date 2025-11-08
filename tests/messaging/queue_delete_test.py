#!/usr/bin/env python

# Delete queues before deleting exchanges

import logging

from pika.exceptions import AMQPError

from mrcs_core.messaging.broker import Broker
from mrcs_core.messaging.client import Manager
from mrcs_core.sys.logging import Logging


# --------------------------------------------------------------------------------------------------------------------

Logging.config('queue_delete_test', level=logging.WARNING)
logger = Logging.getLogger()

broker = Broker.construct()
logger.warning(broker)

manager = Manager()
manager.connect()
logger.warning(manager)

logger.warning('-')


# --------------------------------------------------------------------------------------------------------------------

try:
    for queue in broker.list_queues():
        if queue.name.startswith(Manager.Mode.OPERATIONS) or queue.name.startswith(Manager.Mode.TEST):
            logger.warning(queue)
            manager.queue_delete(queue.name)

    manager.close()         # connection is closed automatically on error

except AMQPError as ex:
    logger.error(ex)
