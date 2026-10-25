"""
Created on 26 Sep 2026

@author: Bruno Beloff (bbeloff@me.com)

A turnout component of a Block
The segment has an up link and a down link, either of which can be a SwitchedSegmentLink, a FixedSegmentLink or none
"""

from collections import OrderedDict
from typing import Any

from mrcs_core.equipment.block.block_enums import BlockHeading
from mrcs_core.equipment.turnout.turnout_configuration import TurnoutConfiguration
from mrcs_core.equipment.turnout.turnout_enums import TurnoutPosition
from mrcs_core.equipment.turnout.turnout_status import TurnoutStatus
from mrcs_core.layout.segment.prolog_link import PrologLink, PrologLinkConstraint
from mrcs_core.layout.segment.prolog_link_set import LinkSet
from mrcs_core.layout.segment.prolog_segment import PrologSegment
from mrcs_core.layout.segment.segment import Segment
from mrcs_core.layout.segment.segment_location import SegmentLocation
from mrcs_core.layout.segment_link.fixed_segment_link import FixedSegmentLink
from mrcs_core.layout.segment_link.segment_link import SegmentLink
from mrcs_core.layout.segment_link.segment_link_builder import SegmentLinkBuilder
from mrcs_core.layout.segment_link.switched_segment_link import SwitchedSegmentLink


# --------------------------------------------------------------------------------------------------------------------

class TurnoutSegment(Segment):
    """
    A turnout component of a Block
    """


    @classmethod
    def construct_from_jdict(cls, jdict) -> TurnoutSegment:
        try:
            type_name = jdict.get('type')

            if type_name != cls.type_name():
                raise TypeError(jdict)

            label = jdict.get('label')
            address = int(jdict.get('addr'))

            up_link = SegmentLinkBuilder.construct_from_jdict(jdict.get('up-link'))
            down_link = SegmentLinkBuilder.construct_from_jdict(jdict.get('down-link'))

            p0_length = int(jdict.get('p0-length'))
            p1_length = int(jdict.get('p1-length'))

        except (TypeError, ValueError):
            raise ValueError(jdict)

        return cls(label, address, up_link, down_link, p0_length, p1_length)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, label: str, address: int, up_link: SegmentLink | None, down_link: SegmentLink | None,
                 p0_length: int, p1_length: int):
        super().__init__(label, up_link, down_link)

        self.__address = address
        self.__p0_length = p0_length
        self.__p1_length = p1_length


    def __eq__(self, other: Any):
        try:
            return (self.label == other.label and self.address == other.address and self.up_link == other.up_link and
                    self.down_link == other.down_link and self.p0_length == other.p0_length and
                    self.p1_length == other.p1_length)
        except (AttributeError, TypeError):
            return False


    # ----------------------------------------------------------------------------------------------------------------

    def status(self, block_label: str):
        return TurnoutStatus(self.label, block_label, self.address, TurnoutPosition.UNKNOWN)


    # ----------------------------------------------------------------------------------------------------------------

    def next_up_location(self, config: TurnoutConfiguration) -> SegmentLocation | None:
        if self.up_link is None:
            return None

        return self.up_link.selected_next_location(config.position(self.label))


    def next_down_location(self, config: TurnoutConfiguration) -> SegmentLocation | None:
        if self.down_link is None:
            return None

        return self.down_link.selected_next_location(config.position(self.label))


    def length(self, config: TurnoutConfiguration) -> int:
        turnout_position = config.position(self.label)

        if turnout_position == TurnoutPosition.P0:
            return self.p0_length

        if turnout_position == TurnoutPosition.P1:
            return self.p1_length

        raise ValueError(f'length cannot be determined for turnout position {turnout_position}')


    # ----------------------------------------------------------------------------------------------------------------

    def as_prolog_segment(self, block_label: str) -> PrologSegment:
        location = self.location(block_label)
        length = min(self.p0_length, self.p1_length)

        return PrologSegment(location, length)


    def as_prolog_links(self, link_set: LinkSet, block_label: str) -> None:
        location = self.location(block_label)
        delta = self.p0_length - self.p1_length

        if isinstance(self.up_link, SwitchedSegmentLink):
            link: SwitchedSegmentLink = self.up_link
            for position, next_location in link.next_location_items():
                p0_length = delta if position == TurnoutPosition.P0 else 0
                constraint = PrologLinkConstraint(location, position, p0_length)
                link_set.add(PrologLink(location, next_location, BlockHeading.UP, constraint))
                link_set.add(PrologLink(next_location, location, BlockHeading.DOWN, constraint))

        elif isinstance(self.up_link, FixedSegmentLink):
            link: FixedSegmentLink = self.up_link
            link_set.add(PrologLink(location, link.next_location, BlockHeading.UP))

        if isinstance(self.down_link, SwitchedSegmentLink):
            link: SwitchedSegmentLink = self.down_link
            for position, next_location in link.next_location_items():
                p0_length = delta if position == TurnoutPosition.P0 else 0
                constraint = PrologLinkConstraint(location, position, p0_length)
                link_set.add(PrologLink(location, next_location, BlockHeading.DOWN, constraint))
                link_set.add(PrologLink(next_location, location, BlockHeading.UP, constraint))

        elif isinstance(self.down_link, FixedSegmentLink):
            link: FixedSegmentLink = self.down_link
            link_set.add(PrologLink(location, link.next_location, BlockHeading.DOWN))


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        jdict = OrderedDict()

        jdict['type'] = self.type_name()

        jdict['label'] = self.label
        jdict['addr'] = self.address

        jdict['p0-length'] = self.p0_length
        jdict['p1-length'] = self.p1_length

        jdict['up-link'] = self.up_link
        jdict['down-link'] = self.down_link

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def address(self):
        return self.__address


    @property
    def p0_length(self):
        return self.__p0_length


    @property
    def p1_length(self):
        return self.__p1_length


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return (f'TurnoutSegment:{{label:{self.label}, address:{self.address}, up_link:{self.up_link}, '
                f'down_link:{self.down_link}, p0_length:{self.p0_length}, p1_length:{self.p1_length}}}')
