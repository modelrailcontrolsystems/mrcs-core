"""
Created on 19 Sep 2026

@author: Bruno Beloff (bbeloff@me.com)

A platform, alongside one or more segments.

The alignment indicates whether the platform is located on the left or right-hand side of a train travelling
with an UP heading. Island platforms should be represented by two platform items, one for each track.

The origin indicates the layout segment of the down-most part of the platform, the offset is the distance (in mm)
from the down-most point in the platform to the down-most point in the segment.

The length field indicates the length of the level part of the platform, start / end ramps are ignored.
"""

from collections import OrderedDict
from typing import Any

from mrcs_core.data.json import JSONable
from mrcs_core.inventory.layout.location import Location
from mrcs_core.inventory.platform.platform_alignment import PlatformAlignment
from mrcs_core.inventory.platform.platform_label import PlatformLabel


# --------------------------------------------------------------------------------------------------------------------

class Platform(JSONable):
    """
    a platform, alongside one or more segments
    """


    @classmethod
    def construct_from_jdict(cls, jdict) -> Platform:
        label = PlatformLabel.construct_from_jdict(jdict.get('label'))
        alignment = PlatformAlignment(jdict.get('alignment'))
        origin = Location.construct_from_jdict(jdict.get('origin'))
        offset = jdict.get('offset')
        length = jdict.get('length')

        return cls(label, alignment, origin, offset, length)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, label: PlatformLabel, alignment: PlatformAlignment, origin: Location, offset: int, length: int):
        self.__label = label
        self.__alignment = alignment
        self.__origin = origin
        self.__offset = offset
        self.__length = length


    # noinspection PyProtectedMember
    def __eq__(self, other: Any):
        try:
            return (self.label == other.label and self.alignment == other.alignment and self.origin == other.origin
                    and self.offset == other.offset and self.length == other.length)
        except (AttributeError, TypeError):
            return False


    def __lt__(self, other):
        return self.label < other.label


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        jdict = OrderedDict()

        jdict['label'] = self.label
        jdict['alignment'] = self.alignment
        jdict['origin'] = self.origin
        jdict['offset'] = self.offset
        jdict['length'] = self.length

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def label(self):
        return self.__label


    @property
    def alignment(self):
        return self.__alignment


    @property
    def origin(self):
        return self.__origin


    @property
    def offset(self):
        return self.__offset


    @property
    def length(self):
        return self.__length


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return (f'Platform:{{label:{self.label}, alignment:{self.alignment.name}, origin:{self.origin}, '
                f'offset:{self.offset}, length:{self.length}}}')
