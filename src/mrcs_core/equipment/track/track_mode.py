"""
Created on 13 Jun 2026

@author: Bruno Beloff (bbeloff@me.com)

An enumeration of all the track modes

Classes in support of the Rocco Z21 DCC command station:
https://www.z21.eu/en/products/z21
"""

from enum import IntEnum, unique

from mrcs_core.data.meta_enum import MetaEnum


# --------------------------------------------------------------------------------------------------------------------

@unique
class TrackMode(IntEnum, metaclass=MetaEnum):
    """
    An enumeration of all the track modes
    """

    POWER_OFF = 0x00
    POWER_ON = 0x01
    PROGRAMMING = 0x02
    SHORT_CIRCUIT = 0x08
    UNKNOWN = 0x82

    COMMAND_POWER_OFF = 0x80
    COMMAND_POWER_ON = 0x81


    # TODO: is there a nice way to implement __str__(..) here?

    def __str__(self, *args, **kwargs):
        return f'TrackMode:{{{self.name:}: 0x{self.value:02x}}}'
