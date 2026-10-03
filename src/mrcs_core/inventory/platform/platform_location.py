"""
Created on 12 Sep 2026

@author: Bruno Beloff (bbeloff@me.com)

A location on a layout, identifying a platform within a station
"""

from typing import Any, Self

from mrcs_core.data.dot import Dot
from mrcs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class PlatformLocation(JSONable):
    """
    A location on a layout
    """


    @classmethod
    def construct_from_dot_path(cls, path: str) -> Self:
        nodes = Dot.nodes(path)

        if len(nodes) != 2 or not nodes[0] or not nodes[1]:
            raise ValueError(path)

        return cls(nodes[0], int(nodes[1]))


    @classmethod
    def construct_from_jdict(cls, jdict) -> Self:
        return cls.construct_from_dot_path(jdict)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, station_label: str, platform_label: int):
        self.__station_label = station_label
        self.__platform_label = platform_label


    def __hash__(self):
        return hash((self.station_label, self.platform_label))


    def __eq__(self, other: Any):
        try:
            return self.station_label == other.station_label and self.platform_label == other.platform_label
        except (AttributeError, TypeError):
            return False


    def __lt__(self, other: Any):
        if self.station_label < other.station_label:
            return True

        if self.station_label > other.station_label:
            return False

        return self.platform_label < other.platform_label


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        return self.dot_path


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def station_label(self):
        return self.__station_label


    @property
    def platform_label(self):
        return self.__platform_label


    # ----------------------------------------------------------------------------------------------------------------


    @property
    def dot_path(self):
        return Dot.path(self.station_label, self.platform_label)


    def __str__(self, *args, **kwargs):
        return f'PlatformLocation:{{station_label:{self.station_label}, platform_label:{self.platform_label}}}'
