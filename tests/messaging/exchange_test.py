#!/usr/bin/env python

import json

from mrcs_core.data.json import JSONify
from mrcs_core.messaging.exchange import Exchange


# --------------------------------------------------------------------------------------------------------------------

with open('data/rabbitmq_exchange.json') as fp:
    jdict = json.load(fp)

print(jdict)
print('-')

exchange1 = Exchange.construct_from_jdict(jdict)
print(exchange1)
print('-')

jstr = JSONify.dumps(exchange1, indent=4)
print(jstr)
print('-')

exchange2 = Exchange.construct_from_jdict(json.loads(jstr))
print(exchange2)
print('-')

print(f'equal: {exchange1 == exchange2}')
