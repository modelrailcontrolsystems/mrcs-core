"""
Created on 5 Nov 2026

@author: Bruno Beloff (bbeloff@me.com)

Conversion between model and real-world measurement units

By convention, model measurements are made in metres and metres per second, whereas measurements in kilometres, miles,
kilometres per hour and miles per hour relate to the real-world equivalents.
"""

from enum import IntEnum, unique

from mrcs_core.data.meta_enum import MetaEnum


# --------------------------------------------------------------------------------------------------------------------

class Conv(object):
    """
    conversion between model and real-world measurement units
    """

    METRES_TO_KILOMETRES = 0.001
    METRES_TO_MILES = 0.000621371


# --------------------------------------------------------------------------------------------------------------------


@unique
class Gauge(IntEnum, metaclass=MetaEnum):
    """
    supported model scales
    """

    O = 45
    OO = 76
    TT = 120
    N = 148


    # ----------------------------------------------------------------------------------------------------------------

    def kilometres(self, metres: float) -> float:
        return round(metres * Conv.METRES_TO_KILOMETRES * self.value, 1)


    def miles(self, metres: float) -> float:
        return round(metres * Conv.METRES_TO_MILES * self.value, 1)


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return f'{self.name}{{{self.value}}}'


# --------------------------------------------------------------------------------------------------------------------


@unique
class Scale(IntEnum, metaclass=MetaEnum):
    """
    supported model scales
    """

    O = 45
    OO = 76
    HO = 87
    TT = 120
    N = 148


    # ----------------------------------------------------------------------------------------------------------------

    def kph(self, ms: float) -> float:
        return round(ms * Conv.METRES_TO_KILOMETRES * 60 * 60 * self.value, 1)


    def mph(self, ms: float) -> float:
        return round(ms * Conv.METRES_TO_MILES * 60 * 60 * self.value, 1)


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return f'{self.name}{{{self.value}}}'
