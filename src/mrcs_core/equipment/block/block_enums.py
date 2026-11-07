"""
Created on 3 Jul 2026

@author: Bruno Beloff (bbeloff@me.com)

The enumerated types used by block equipment

Classes in support of the Rocco Z21 DCC control router station:
https://www.z21.eu/en/products/z21
"""

from enum import IntEnum, unique

from mrcs_core.data.json import JSONable
from mrcs_core.data.meta_enum import ABCMetaEnum


# --------------------------------------------------------------------------------------------------------------------

@unique
class BlockHeading(JSONable, IntEnum, metaclass=ABCMetaEnum):
    """
    An enumeration of all the block occupant directions
    """

    UNASSIGNED = 0
    UP = 1
    DOWN = 2


    @classmethod
    def construct_from_prolog(cls, pname: str):
        return BlockHeading[pname.upper()]


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self) -> bool:
        return self == BlockHeading.UP or self == BlockHeading.DOWN


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        return self.name


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return f'{self.name}{{{self.value}}}'


# --------------------------------------------------------------------------------------------------------------------

@unique
class BlockOccupantFace(JSONable, IntEnum, metaclass=ABCMetaEnum):
    """
    An enumeration of all the block occupant directions
    """

    UNKNOWN = 0x00
    FACE_FORWARD = 0x02
    FACE_BACKWARD = 0x03


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        return self.name


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return f'{self.name}{{0x{self.value:02x}}}'


# --------------------------------------------------------------------------------------------------------------------

@unique
class BlockVoltage(JSONable, IntEnum, metaclass=ABCMetaEnum):
    """
    An enumeration of all the LAN_CAN_DETECTOR occupancy status values
    """

    UNKNOWN = 0xffff

    FREE_NO_VOLTAGE = 0x0000
    FREE_WITH_VOLTAGE = 0x0100
    OCCUPIED_NO_VOLTAGE = 0x1000
    OCCUPIED_WITH_VOLTAGE = 0x1100
    OCCUPIED_OVERLOAD_1 = 0x1201
    OCCUPIED_OVERLOAD_2 = 0x1202
    OCCUPIED_OVERLOAD_3 = 0x1203


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        return self.name


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return f'{self.name}{{0x{self.value:04x}}}'
