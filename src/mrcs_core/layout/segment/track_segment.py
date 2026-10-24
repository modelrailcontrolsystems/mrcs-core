"""
Created on 26 Sep 2026

@author: Bruno Beloff (bbeloff@me.com)

A track component of a Block
The segment has an up link and a down link, either of which can be a FixedSegmentLink or none
"""

from collections import OrderedDict
from typing import Any

from mrcs_core.equipment.block.block_enums import BlockHeading
from mrcs_core.equipment.turnout.turnout_configuration import TurnoutConfiguration
from mrcs_core.layout.segment.prolog_link import PrologLink
from mrcs_core.layout.segment.prolog_link_set import LinkSet
from mrcs_core.layout.segment.prolog_segment import PrologSegment
from mrcs_core.layout.segment.segment import Segment
from mrcs_core.layout.segment.segment_location import SegmentLocation
from mrcs_core.layout.segment_link.fixed_segment_link import FixedSegmentLink
from mrcs_core.layout.segment_link.segment_link import SegmentLink
from mrcs_core.layout.segment_link.segment_link_builder import SegmentLinkBuilder


# --------------------------------------------------------------------------------------------------------------------

class TrackSegment(Segment):
    """
    A track component of a Block
    """


    @classmethod
    def construct_from_jdict(cls, jdict) -> TrackSegment:
        type_name = jdict.get('type')

        if type_name != cls.type_name():
            raise TypeError(jdict)

        label = jdict.get('label')
        length = jdict.get('length')

        up_link = SegmentLinkBuilder.construct_from_jdict(jdict.get('up-link'))
        down_link = SegmentLinkBuilder.construct_from_jdict(jdict.get('down-link'))

        return cls(label, up_link, down_link, length)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, label: str, up_link: SegmentLink | None, down_link: SegmentLink | None, length: int):
        super().__init__(label, up_link, down_link)

        self._length = length


    # noinspection PyProtectedMember
    def __eq__(self, other: Any):
        try:
            return (self.label == other.label and self.up_link == other.up_link and self.down_link == other.down_link
                    and self._length == other._length)
        except (AttributeError, TypeError):
            return False


    # ----------------------------------------------------------------------------------------------------------------

    # noinspection unresolved-references
    def next_up_location(self, config: TurnoutConfiguration) -> SegmentLocation | None:
        if self.up_link is None:
            return None

        return self.up_link.selected_next_location(None)


    # noinspection unresolved-references
    def next_down_location(self, config: TurnoutConfiguration) -> SegmentLocation | None:
        if self.down_link is None:
            return None

        return self.down_link.selected_next_location(None)


    def length(self, config: TurnoutConfiguration) -> int:
        return self._length


    # ----------------------------------------------------------------------------------------------------------------

    def as_prolog_segment(self, block_label: str) -> PrologSegment:
        location = self.location(block_label)
        return PrologSegment(location, self._length)


    def as_prolog_links(self, link_set: LinkSet, block_label: str) -> None:
        location = self.location(block_label)

        if isinstance(self.up_link, FixedSegmentLink):
            link: FixedSegmentLink = self.up_link
            link_set.add(PrologLink(location, link.next_location, BlockHeading.UP))

        if isinstance(self.down_link, FixedSegmentLink):
            link: FixedSegmentLink = self.down_link
            link_set.add(PrologLink(location, link.next_location, BlockHeading.DOWN))


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        jdict = OrderedDict()

        jdict['type'] = self.type_name()

        jdict['label'] = self.label
        jdict['length'] = self._length

        jdict['up-link'] = self.up_link
        jdict['down-link'] = self.down_link

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def address(self):
        return None


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return (
            f'TrackSegment:{{label:{self.label}, up_link:{self.up_link}, down_link:{self.down_link}, '
            f'length:{self._length}}}')
