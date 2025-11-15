#!/usr/bin/env python

import json

from mrcs_core.data.equipment_identity import EquipmentFilter, EquipmentIdentifier, EquipmentType
from mrcs_core.data.json import JSONify


# --------------------------------------------------------------------------------------------------------------------

types = list(EquipmentType)
print(types)
print('=')

equipment_type_1 = EquipmentType.BOS
print(equipment_type_1)
print(str(equipment_type_1))
print('-')

# --------------------------------------------------------------------------------------------------------------------

equipment_identifier_1 = EquipmentIdentifier(EquipmentType.BOS, 1, 2)
print(equipment_identifier_1)
jstr = JSONify.dumps(equipment_identifier_1)
print(jstr)
print('-')

equipment_identifier_2a = EquipmentIdentifier(EquipmentType.MPU, None, 3)
print(equipment_identifier_2a)
jstr = JSONify.dumps(equipment_identifier_2a)
print(jstr)
print('-')

equipment_identifier_2b = EquipmentIdentifier.construct_from_jdict(json.loads(jstr))
print(equipment_identifier_2b)

print("equals:", equipment_identifier_1 == equipment_identifier_2b)
print("equals:", equipment_identifier_2a == equipment_identifier_2b)
print('-')

try:
    equipment_identifier_3 = EquipmentIdentifier.construct_from_jdict(json.loads('"XXX.-.02"'))
    print(equipment_identifier_3)
except ValueError as ex:
    print(f'ValueError: {ex}')
    print('-')

try:
    equipment_identifier_3 = EquipmentIdentifier.construct_from_jdict(json.loads('"BOS.xxx.02"'))
    print(equipment_identifier_3)
except ValueError as ex:
    print(f'ValueError: {ex}')
    print('=')

# --------------------------------------------------------------------------------------------------------------------

equipment_filter_1 = EquipmentFilter(EquipmentType.BOS, None, None)
print(equipment_filter_1)
jstr = JSONify.dumps(equipment_filter_1)
print(jstr)
print('-')

