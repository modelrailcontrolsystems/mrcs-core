#!/usr/bin/env python

import sys

import dateutil.tz

from mrcs_core.data.iso_datetime import ISODatetime
from mrcs_core.data.json import JSONify


# --------------------------------------------------------------------------------------------------------------------

print(sys.version_info)
print('-')

dt = ISODatetime.construct_from_db('2025-08-26 00:00:00.123')
print(f'dt: {dt}')
print(f"isoformat: {dt.isoformat(timespec='milliseconds')}")
print('-')

dt = ISODatetime.construct_from_jdict('2025-08-26T01:00:00.123+05:00')
print(f'dt: {dt}')
dbformat = dt.dbformat()
print(f'dbformat: {dbformat}')
print('-')

now = ISODatetime.now(tz=dateutil.tz.tzlocal())
print(f'now: {now}')
print(JSONify.dumps(now))
print('-')

