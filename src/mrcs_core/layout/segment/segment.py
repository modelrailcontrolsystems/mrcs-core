"""
Created on 9 Jul 2026

@author: Bruno Beloff (bbeloff@me.com)

A component of a Block
"""

from abc import ABC, abstractmethod
from typing import Any

from mrcs_core.data.json import JSONable
from mrcs_core.equipment.block.block_enums import BlockHeading
from mrcs_core.equipment.turnout.turnout_configuration import TurnoutConfiguration
from mrcs_core.layout.segment.segment_location import SegmentLocation
from mrcs_core.layout.segment_link.segment_link import SegmentLink


# --------------------------------------------------------------------------------------------------------------------

class Segment(JSONable, ABC):
    """
    An abstract componet of a Block
    """


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, label: str, up_link: SegmentLink | None, down_link: SegmentLink | None):
        self.__label = label
        self.__up_link = up_link
        self.__down_link = down_link


    def __lt__(self, other: Any):
        return self.label < other.label


    # ----------------------------------------------------------------------------------------------------------------

    def next_location(self, config: TurnoutConfiguration, heading: BlockHeading) -> SegmentLocation | None:
        if heading == BlockHeading.UNASSIGNED:
            raise ValueError('cannot get next segment for UNASSIGNED heading')

        return self.next_up_location(config) if heading == BlockHeading.UP else self.next_down_location(config)


    @abstractmethod
    def next_up_location(self, config: TurnoutConfiguration) -> SegmentLocation | None:
        pass


    @abstractmethod
    def next_down_location(self, config: TurnoutConfiguration) -> SegmentLocation | None:
        pass


    @abstractmethod
    def length(self, config: TurnoutConfiguration) -> int:
        pass


    # ----------------------------------------------------------------------------------------------------------------

    def next_locations(self):
        return self.next_up_locations() + self.next_down_locations()


    # noinspection unresolved-references
    def next_up_locations(self) -> list[SegmentLocation]:
        return [] if self.up_link is None else self.up_link.next_locations()


    # noinspection unresolved-references
    def next_down_locations(self) -> list[SegmentLocation]:
        return [] if self.down_link is None else self.down_link.next_locations()


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def label(self):
        return self.__label


    @property
    @abstractmethod
    def address(self):
        pass


    @property
    def up_link(self):
        return self.__up_link


    @property
    def down_link(self):
        return self.__down_link
