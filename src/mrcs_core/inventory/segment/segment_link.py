"""
Created on 10 Jul 2026

@author: Bruno Beloff (bbeloff@me.com)

A link between segments
"""

from abc import ABC, abstractmethod
from collections import OrderedDict
from typing import Any

from mrcs_core.data.json import JSONable
from mrcs_core.equipment.turnout.turnout_enums import TurnoutPosition
from mrcs_core.inventory.layout.location import Location


# TODO: add JSON examples to all JSONable class header comments
# --------------------------------------------------------------------------------------------------------------------

class SegmentLink(JSONable, ABC):
    """
    The common interface for segment links
    """


    @classmethod
    def construct_from_jdict(cls, jdict) -> SegmentLink | None:
        if jdict is None:
            return None

        type_name = jdict.get('type')

        if type_name == FixedSegmentLink.type_name():
            return FixedSegmentLink.construct_from_jdict(jdict)

        if type_name == SwitchedSegmentLink.type_name():
            return SwitchedSegmentLink.construct_from_jdict(jdict)

        raise TypeError(f'invalid segment type: {type_name}')


    # ----------------------------------------------------------------------------------------------------------------

    @abstractmethod
    def selected_next_location(self, turnout_position: TurnoutPosition | None) -> Location | None:
        pass


    @abstractmethod
    def next_locations(self) -> list[Location]:
        pass


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

        next_location = Location.construct_from_jdict(jdict.get('next'))

        return cls(next_location)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, next_location: Location):
        self.__next_location = next_location


    def __eq__(self, other: Any):
        try:
            return self.next_location == other.next_location
        except (AttributeError, TypeError):
            return False


    # ----------------------------------------------------------------------------------------------------------------

    def selected_next_location(self, turnout_position: TurnoutPosition | None) -> Location | None:
        return self.next_location


    def next_locations(self) -> list[Location]:
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
        p0_next_location = None if p0 is None else Location.construct_from_jdict(p0)

        p1 = jdict.get('p1-next')
        p1_next_location = None if p1 is None else Location.construct_from_jdict(p1)

        return cls(p0_next_location, p1_next_location)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, p0_next_location: Location | None, p1_next_location: Location | None):
        self.__p0_next_location = p0_next_location
        self.__p1_next_location = p1_next_location


    def __eq__(self, other: Any):
        try:
            return self.p0_next_location == other.p0_next_location and self.p1_next_location == other.p1_next_location
        except (AttributeError, TypeError):
            return False


    # ----------------------------------------------------------------------------------------------------------------

    # noinspection unresolved-references,unresolved-references
    def selected_next_location(self, turnout_position: TurnoutPosition | None) -> Location | None:
        if turnout_position == TurnoutPosition.P0:
            return self.p0_next_location

        if turnout_position == TurnoutPosition.P1:
            return self.p1_next_location

        raise ValueError(f'selected_next_location cannot be determined for turnout position {turnout_position}')


    # noinspection unresolved-references
    def next_locations(self) -> list[Location]:
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
