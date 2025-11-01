#!/usr/bin/env python

from mrcs_core.data.json import JSONify
from mrcs_core.messaging.manager import Manager


# --------------------------------------------------------------------------------------------------------------------

manager = Manager.construct()
print(manager)

queues = manager.list_queues()

for q in queues:
    print(q)
    print(JSONify.dumps(q))
    print('-')
