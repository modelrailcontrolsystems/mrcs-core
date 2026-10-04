"""
Created on 3 Oct 2026

@author: Bruno Beloff (bbeloff@me.com)

A component of a Layout, monitored by a block detector
Blocks contain track and turnout platforms. A Block may have a fixed direction, or may be reversible.
"""

from collections import OrderedDict
from typing import Any

from mrcs_core.data.json import JSONable
from mrcs_core.layout.platform.platform import Platform


# --------------------------------------------------------------------------------------------------------------------

class Station(JSONable):
    """
    A component of a layout, monitored by a block detector
    """


    @classmethod
    def construct_from_jdict(cls, jdict) -> Station:
        label = jdict.get('label')

        platforms = OrderedDict()
        for platform_jdict in jdict.get('platforms', []):
            platform = Platform.construct_from_jdict(platform_jdict)
            platforms[platform.label] = platform

        return cls(label, platforms)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, label: str, platforms: OrderedDict[int, Platform]):
        self.__label = label
        self.__platforms = platforms


    def __eq__(self, other: Any):
        try:
            return self.label == other.label and self.platforms == other.platforms
        except (AttributeError, TypeError):
            return False


    def __lt__(self, other: Any):
        return self.label < other.label


    # ----------------------------------------------------------------------------------------------------------------

    def platform_report(self, platform_label: int | None) -> Station:
        try:
            platforms = self.__platforms if platform_label is None else {
                platform_label: self.__platforms[platform_label]}
        except KeyError:
            raise KeyError(platform_label)

        return Station(self.label, OrderedDict(platforms))


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        jdict = OrderedDict()

        jdict['label'] = self.label
        jdict['platforms'] = self.platforms

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def label(self):
        return self.__label


    @property
    def platforms(self):
        return tuple(self.__platforms.values())


    def platform(self, label):
        try:
            return self.__platforms[label]
        except KeyError:
            return None


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        platforms = '[' + ', '.join([str(platform) for platform in self.platforms]) + ']'
        return f'Station:{{label:{self.label}, platforms:{platforms}}}'
