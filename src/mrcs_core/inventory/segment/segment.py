"""
Created on 9 Jul 2026

@author: Bruno Beloff (bbeloff@me.com)

A component of a Block
"""

from abc import ABC, abstractmethod
from collections import OrderedDict
from typing import Any

from mrcs_core.data.json import JSONable
from mrcs_core.equipment.block.block_enums import BlockHeading
from mrcs_core.equipment.turnout.turnout_configuration import TurnoutConfiguration
from mrcs_core.inventory.layout.location import Location
from mrcs_core.inventory.segment.segment_link import SegmentLink


# --------------------------------------------------------------------------------------------------------------------

class Segment(JSONable, ABC):
    """
    An abstract componet of a Block
    """


    @classmethod
    def construct_from_jdict(cls, jdict) -> Segment:
        type_name = jdict.get('type')

        if type_name == TrackSegment.type_name():
            return TrackSegment.construct_from_jdict(jdict)

        if type_name == TurnoutSegment.type_name():
            return TurnoutSegment.construct_from_jdict(jdict)

        raise TypeError(f'invalid segment type: {type_name}')


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, label: str, length: int, up_link: SegmentLink | None, down_link: SegmentLink | None):
        self.__label = label
        self.__length = length  # mm
        self.__up_link = up_link
        self.__down_link = down_link


    def __lt__(self, other: Any):
        return self.label < other.label


    # ----------------------------------------------------------------------------------------------------------------

    def next_location(self, config: TurnoutConfiguration, heading: BlockHeading) -> Location | None:
        if heading == BlockHeading.UNASSIGNED:
            raise ValueError('cannot get next segment for UNASSIGNED heading')

        return self.next_up_location(config) if heading == BlockHeading.UP else self.next_down_location(config)


    @abstractmethod
    def next_up_location(self, config: TurnoutConfiguration) -> Location | None:
        pass


    @abstractmethod
    def next_down_location(self, config: TurnoutConfiguration) -> Location | None:
        pass


    # ----------------------------------------------------------------------------------------------------------------

    def next_locations(self):
        return self.next_up_locations() + self.next_down_locations()


    # noinspection unresolved-references
    def next_up_locations(self) -> list[Location]:
        return [] if self.up_link is None else self.up_link.next_locations()


    # noinspection unresolved-references
    def next_down_locations(self) -> list[Location]:
        return [] if self.down_link is None else self.down_link.next_locations()


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def label(self):
        return self.__label


    @property
    def length(self):
        return self.__length


    @property
    def up_link(self):
        return self.__up_link


    @property
    def down_link(self):
        return self.__down_link


# --------------------------------------------------------------------------------------------------------------------

class TrackSegment(Segment):
    """
    A track component of a Block
    """


    @classmethod
    def construct_from_jdict(cls, jdict) -> TrackSegment:
        type_name = jdict.get('type')

        if type_name != cls.type_name():
            raise TypeError(f'required type:{cls.type_name()} got:{type_name}')

        label = jdict.get('label')
        length = jdict.get('length')

        up_link = SegmentLink.construct_from_jdict(jdict.get('up-link'))
        down_link = SegmentLink.construct_from_jdict(jdict.get('down-link'))

        return cls(label, length, up_link, down_link)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, label: str, length: int, up_link: SegmentLink | None, down_link: SegmentLink | None):
        super().__init__(label, length, up_link, down_link)


    def __eq__(self, other: Any):
        try:
            return (self.label == other.label and self.length == other.length and
                    self.up_link == other.up_link and self.down_link == other.down_link)
        except (AttributeError, TypeError):
            return False


    # ----------------------------------------------------------------------------------------------------------------

    # noinspection unresolved-references
    def next_up_location(self, config: TurnoutConfiguration) -> Location | None:
        if self.up_link is None:
            return None

        return self.up_link.selected_next_location(None)


    # noinspection unresolved-references
    def next_down_location(self, config: TurnoutConfiguration) -> Location | None:
        if self.down_link is None:
            return None

        return self.down_link.selected_next_location(None)


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        jdict = OrderedDict()

        jdict['type'] = self.type_name()

        jdict['label'] = self.label
        jdict['length'] = self.length

        jdict['up-link'] = self.up_link
        jdict['down-link'] = self.down_link

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return (f'TrackSegment:{{label:{self.label}, length:{self.length}, '
                f'up_link:{self.up_link}, down_link:{self.down_link}}}')


# --------------------------------------------------------------------------------------------------------------------

class TurnoutSegment(Segment):
    """
    A turnout component of a Block
    """


    @classmethod
    def construct_from_jdict(cls, jdict) -> TurnoutSegment:
        type_name = jdict.get('type')

        if type_name != cls.type_name():
            raise TypeError(f'required type:{cls.type_name()} got:{type_name}')

        label = jdict.get('label')
        length = jdict.get('length')
        turnout = jdict.get('turnout')

        up_link = SegmentLink.construct_from_jdict(jdict.get('up-link'))
        down_link = SegmentLink.construct_from_jdict(jdict.get('down-link'))

        return cls(label, length, turnout, up_link, down_link)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, label: str, length: int, turnout: str, up_link: SegmentLink | None,
                 down_link: SegmentLink | None):
        super().__init__(label, length, up_link, down_link)
        self.__turnout = turnout


    def __eq__(self, other: Any):
        try:
            return (self.label == other.label and self.length == other.length and self.turnout == other.turnout and
                    self.up_link == other.up_link and self.down_link == other.down_link)
        except (AttributeError, TypeError):
            return False


    # ----------------------------------------------------------------------------------------------------------------

    # noinspection unresolved-references
    def next_up_location(self, config: TurnoutConfiguration) -> Location | None:
        if self.up_link is None:
            return None

        return self.up_link.selected_next_location(config.position(self.turnout))


    # noinspection unresolved-references
    def next_down_location(self, config: TurnoutConfiguration) -> Location | None:
        if self.down_link is None:
            return None

        return self.down_link.selected_next_location(config.position(self.turnout))


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        jdict = OrderedDict()

        jdict['type'] = self.type_name()

        jdict['label'] = self.label
        jdict['length'] = self.length
        jdict['turnout'] = self.turnout

        jdict['up-link'] = self.up_link
        jdict['down-link'] = self.down_link

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def turnout(self):
        return self.__turnout


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return (f'TurnoutSegment:{{label:{self.label}, length:{self.length}, turnout:{self.turnout}, '
                f'up_link:{self.up_link}, down_link:{self.down_link}}}')
