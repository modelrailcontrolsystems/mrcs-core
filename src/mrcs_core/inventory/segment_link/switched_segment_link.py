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

class SwitchedSegmentLink(SegmentLink):
    """
    A link between segments, dependent on turnout position
    """


    @classmethod
    def type_name(cls) -> str:
        return 'Switched'


    @classmethod
    def construct_from_jdict(cls, jdict) -> SwitchedSegmentLink | None:
        if jdict is None:
            return None

        p0 = jdict.get('p0-next')
        p0_next_location = None if p0 is None else SegmentLocation.construct_from_jdict(p0)

        p1 = jdict.get('p1-next')
        p1_next_location = None if p1 is None else SegmentLocation.construct_from_jdict(p1)

        return cls(p0_next_location, p1_next_location)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, p0_next_location: SegmentLocation | None, p1_next_location: SegmentLocation | None):
        self.__p0_next_location = p0_next_location
        self.__p1_next_location = p1_next_location


    def __eq__(self, other: Any):
        try:
            return self.p0_next_location == other.p0_next_location and self.p1_next_location == other.p1_next_location
        except (AttributeError, TypeError):
            return False


    # ----------------------------------------------------------------------------------------------------------------

    # noinspection unresolved-references,unresolved-references
    def selected_next_location(self, turnout_position: TurnoutPosition | None) -> SegmentLocation | None:
        if turnout_position == TurnoutPosition.P0:
            return self.p0_next_location

        if turnout_position == TurnoutPosition.P1:
            return self.p1_next_location

        raise ValueError(f'selected_next_location cannot be determined for turnout position {turnout_position}')


    # noinspection unresolved-references
    def next_locations(self) -> list[SegmentLocation]:
        p0_next_location = [] if self.p0_next_location is None else [self.p0_next_location]
        p1_next_location = [] if self.p1_next_location is None else [self.p1_next_location]

        return p0_next_location + p1_next_location


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        jdict = OrderedDict()

        jdict['type'] = self.type_name()

        jdict['p0-next'] = self.p0_next_location
        jdict['p1-next'] = self.p1_next_location

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def p0_next_location(self):
        return self.__p0_next_location


    @property
    def p1_next_location(self):
        return self.__p1_next_location


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return (f'SwitchedSegmentLink:{{p0_next_location:{self.p0_next_location}, '
                f'p1_next_location:{self.p1_next_location}}}')
