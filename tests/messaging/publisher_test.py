#!/usr/bin/env python

import logging

from mrcs_core.messaging.message import Message
from mrcs_core.messaging.client import Endpoint
from mrcs_core.sys.logging import Logging


# --------------------------------------------------------------------------------------------------------------------

EXCHANGE_NAME = 'mrcs_test_exchange'

# --------------------------------------------------------------------------------------------------------------------

Logging.config('publisher_test', level=logging.WARNING)
logger = Logging.getLogger()

publisher = Endpoint(EXCHANGE_NAME, None, None, None)       # publish only

try:
    publisher.connect()
    logger.warning(publisher)

    message = Message.construct('src0.seg1.dev1', 'hello')

    publisher.publish(message)
    logger.warning(f'sent {message}')

except RuntimeError as ex:
    logger.error(ex)

finally:
    publisher.close()
