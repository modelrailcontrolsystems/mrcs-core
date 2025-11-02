#!/usr/bin/env python

import logging

from mrcs_core.messaging.client import Manager
from mrcs_core.sys.logging import Logging

# TODO: implement
# --------------------------------------------------------------------------------------------------------------------

Logging.config('exchange_delete_test', level=logging.WARNING)
logger = Logging.getLogger()

manager = Manager()
logger.warning(manager)

manager.connect()
logger.warning(manager)


manager.close()
logger.warning(manager)
