#!/usr/bin/env python
import logging

from mrcs_core.messaging.message import Message
from mrcs_core.messaging.publisher import Publisher
from mrcs_core.sys.logging import Logging


# --------------------------------------------------------------------------------------------------------------------

Logging.config('publisher_test', level=logging.WARNING)
logger = Logging.getLogger()

publisher = Publisher('test_exchange')

try:
    publisher.connect()
    print(publisher)

    message = Message.construct('src2.seg1.dev1', 'hello')

    publisher.publish(message)
    logger.warning(f'sent {message}')

except RuntimeError as ex:
    print(ex)

finally:
    publisher.close()
