"""
Created on 13 Jun 2026

@author: Bruno Beloff (bbeloff@me.com)

An enumeration of all the turnout positions

Classes in support of the Rocco Z21 DCC command station:
https://www.z21.eu/en/products/z21

Based on code:
https://github.com/botmonster/z21aio/tree/main
https://gitlab.com/z21-fpm/z21_python
"""

from enum import IntEnum, unique

from mrcs_core.data.meta_enum import MetaEnum


# --------------------------------------------------------------------------------------------------------------------

@unique
class TurnoutPosition(IntEnum, metaclass=MetaEnum):
    """
    An enumeration of all the turnout positions
    """

    UNKNOWN = 0
    P0 = 1
    P1 = 2
    INVALID = 3
