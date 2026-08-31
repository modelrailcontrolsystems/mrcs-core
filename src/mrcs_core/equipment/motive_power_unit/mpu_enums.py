"""
Created on 6 Jun 2026

@author: Bruno Beloff (bbeloff@me.com)

The enumerated types used by MPU equipment

Classes in support of the Rocco Z21 DCC control router station:
https://www.z21.eu/en/products/z21

Based on code:
https://github.com/botmonster/z21aio/tree/main
https://gitlab.com/z21-fpm/z21_python
"""

from enum import IntEnum, unique

from mrcs_core.data.meta_enum import MetaEnum


# --------------------------------------------------------------------------------------------------------------------

@unique
class MPUDirection(IntEnum, metaclass=MetaEnum):
    """
    An enumeration of all the possible MPU directions
    """

    FORWARD = 0
    REVERSE = 1
    UNKNOWN = 2


    @classmethod
    def from_reverse(cls, reverse: bool):
        return cls.REVERSE if reverse else cls.FORWARD


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return f'{self.name}{{{self.value}}}'


# --------------------------------------------------------------------------------------------------------------------

@unique
class ThrottleSteps(IntEnum, metaclass=MetaEnum):
    """
    An enumeration of all the possible DCC throttle step resolutions
    """

    STEPS_14 = 0
    STEPS_28 = 2
    STEPS_128 = 4


    # ----------------------------------------------------------------------------------------------------------------

    def to_speed_byte(self) -> int:
        """Convert to speed command byte prefix."""
        match self:
            case self.STEPS_14:
                return 0x10
            case self.STEPS_28:
                return 0x12
            case self.STEPS_128:
                return 0x13


    @property
    def max_speed(self) -> int:
        """Maximum speed value for this throttle mode."""
        match self:
            case self.STEPS_14:
                return 14
            case self.STEPS_28:
                return 28
            case self.STEPS_128:
                return 128


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return f'{self.name}{{{self.value}}}'
