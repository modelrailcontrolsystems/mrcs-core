#!/usr/bin/env python

import json

from mrcs_core.data.json import JSONify
from mrcs_core.messaging.message import Message


# --------------------------------------------------------------------------------------------------------------------

message1 = Message.construct('src1.sec1.dev1', 'hello')
print(message1)
jstr1 = JSONify.dumps(message1, indent=4)
print(jstr1)
print('-')

message2 = Message.construct_from_jdict(json.loads(jstr1))
print(message2)

print(f'equal: {message1 == message2}')
