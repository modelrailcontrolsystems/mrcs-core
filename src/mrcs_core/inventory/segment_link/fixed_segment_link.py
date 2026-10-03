"""
Created on 26 Sep 2026

@author: Bruno Beloff (bbeloff@me.com)

A link between segments
"""

from collections import OrderedDict
from typing import Any

from mrcs_core.equipment.turnout.turnout_enums import TurnoutPosition
from mrcs_core.inventory.segment.segment_location import SegmentLocation
from mrcs_core.inventory.segment_link.segment_link import SegmentLink


# --------------------------------------------------------------------------------------------------------------------

class FixedSegmentLink(SegmentLink):
    """
    A simple link between segments
    """


    @classmethod
    def type_name(cls) -> str:
        return 'Fixed'


    @classmethod
    def construct_from_jdict(cls, jdict) -> FixedSegmentLink | None:
        if jdict is None:
            return None

        type_name = jdict.get('type')

        if type_name != cls.type_name():
            raise TypeError(f'required type:{cls.type_name()} got:{type_name}')

        next_location = SegmentLocation.construct_from_jdict(jdict.get('next'))

        return cls(next_location)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, next_location: SegmentLocation):
        self.__next_location = next_location


    def __eq__(self, other: Any):
        try:
            return self.next_location == other.next_location
        except (AttributeError, TypeError):
            return False


    # ----------------------------------------------------------------------------------------------------------------

    def selected_next_location(self, turnout_position: TurnoutPosition | None) -> SegmentLocation | None:
        return self.next_location


    def next_locations(self) -> list[SegmentLocation]:
        return [] if self.next_location is None else [self.next_location]


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        jdict = OrderedDict()

        jdict['type'] = self.type_name()
        jdict['next'] = self.next_location

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def next_location(self):
        return self.__next_location


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return f'FixedSegmentLink:{{next_location:{self.next_location}}}'
