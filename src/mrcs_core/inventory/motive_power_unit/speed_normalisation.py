"""
Created on 28 Nov 2026

@author: Bruno Beloff (bbeloff@me.com)

Conversion from MPU reported speed to actual Kph.
The slope and offset can be obtained using the mrcs_control_speed_trial CLU.

{
    "slope": 0.492,
    "offset": 1.418
}
"""

from collections import OrderedDict
from typing import Any, Self

from mrcs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class SpeedNormalisation(JSONable):
    """
    conversion from MPU reported speed to actual Kph
    """


    @classmethod
    def construct_from_jdict(cls, jdict) -> Self | None:
        if jdict is None:
            return None

        slope = float(jdict.get('slope'))
        offset = float(jdict.get('offset'))

        return cls(slope, offset)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, slope: float, offset: float):
        self.__slope = slope
        self.__offset = offset


    def __eq__(self, other: Any) -> bool:
        try:
            return self.slope == other.slope and self.offset == other.offset
        except (AttributeError, TypeError):
            return False


    # ----------------------------------------------------------------------------------------------------------------

    def actual_speed(self, reported_speed: int) -> float:
        if reported_speed == 0:
            return 0.0

        return round(reported_speed * self.slope + self.offset, 1)


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        jdict = OrderedDict()

        jdict['slope'] = self.slope
        jdict['offset'] = self.offset

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def slope(self):
        return self.__slope


    @property
    def offset(self):
        return self.__offset


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return f'SpeedNormalisation:{{slope:{self.slope}, offset:{self.offset}}}'
