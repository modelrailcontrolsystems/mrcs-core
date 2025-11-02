#!/usr/bin/env python

import json

from mrcs_core.data.json import JSONify
from mrcs_core.messaging.queue import Queue


# --------------------------------------------------------------------------------------------------------------------

with open('rabbitmq_queue.json') as fp:
    jdict = json.load(fp)

print(jdict)
print('-')

queue1 = Queue.construct_from_jdict(jdict)
print(queue1)
print('-')

jstr = JSONify.dumps(queue1, indent=4)
print(jstr)
print('-')

queue2 = Queue.construct_from_jdict(json.loads(jstr))
print(queue2)
print('-')

print(f'equal: {queue1 == queue2}')
