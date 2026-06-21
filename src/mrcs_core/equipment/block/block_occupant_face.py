"""
Created on 14 Jun 2026

@author: Bruno Beloff (bbeloff@me.com)

An enumeration of all the block occupant directions

Classes in support of the Rocco Z21 DCC command station:
https://www.z21.eu/en/products/z21
"""

from enum import IntEnum, unique

from mrcs_core.data.meta_enum import MetaEnum


# --------------------------------------------------------------------------------------------------------------------

@unique
class BlockOccupantFace(IntEnum, metaclass=MetaEnum):
    """
    An enumeration of all the block occupant directions
    """

    UNKNOWN = 0x00
    FWD = 0x02
    REV = 0x03
