"""
Created on 19 Sep 2026

@author: Bruno Beloff (bbeloff@me.com)

The label for a Platform, in the form StationName/PlatformNumber
"""

from typing import Any, Self

from mrcs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class PlatformLabel(JSONable):
    """
    the label for a Platform, in the form StationName/PlatformNumber
    """


    @classmethod
    def construct_from_shortform(cls, shortform: str) -> Self:
        pieces = shortform.split('/')

        if len(pieces) != 2 or not pieces[0] or not pieces[1]:
            raise ValueError(shortform)

        return cls(pieces[0], int(pieces[1]))


    @classmethod
    def construct_from_jdict(cls, jdict) -> Self:
        return cls.construct_from_shortform(jdict)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, station: str, number: int):
        self.__station = station
        self.__number = number


    def __hash__(self):
        return hash((self.station, self.number))


    # noinspection PyProtectedMember
    def __eq__(self, other: Any):
        try:
            return self.station == other.station and self.number == other.number
        except (AttributeError, TypeError):
            return False


    def __lt__(self, other):
        if self.station < other.station:
            return True

        if self.station > other.station:
            return False

        return self.number < other.number


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        return self.shortform


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def station(self):
        return self.__station


    @property
    def number(self):
        return self.__number


    # ----------------------------------------------------------------------------------------------------------------


    @property
    def shortform(self):
        return '/'.join((self.station, str(self.number)))


    def __str__(self, *args, **kwargs):
        return f'PlatformLabel:{{station:{self.station}, number:{self.number}}}'
