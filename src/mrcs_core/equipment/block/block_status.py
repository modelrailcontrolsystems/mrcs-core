"""
Created on 16 Jun 2026

@author: Bruno Beloff (bbeloff@me.com)

An enumeration of all the LAN_CAN_DETECTOR occupancy status values

Classes in support of the Rocco Z21 DCC command station:
https://www.z21.eu/en/products/z21
"""

from enum import IntEnum, unique

from mrcs_core.data.meta_enum import MetaEnum


# --------------------------------------------------------------------------------------------------------------------

@unique
class BlockStatus(IntEnum, metaclass=MetaEnum):
    """
    An enumeration of all the LAN_CAN_DETECTOR occupancy status values
    """

    FREE_NO_VOLTAGE = 0x0000
    FREE_WITH_VOLTAGE = 0x0100
    OCCUPIED_NO_VOLTAGE = 0x1000
    OCCUPIED_WITH_VOLTAGE = 0x1100
    OCCUPIED_OVERLOAD_1 = 0x1201
    OCCUPIED_OVERLOAD_2 = 0x1202
    OCCUPIED_OVERLOAD_3 = 0x1203
