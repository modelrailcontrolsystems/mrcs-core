"""
Created on 9 Jul 2026

@author: Bruno Beloff (bbeloff@me.com)

A component of a Block

"""

from abc import ABC
from collections import OrderedDict

from mrcs_core.data.json import JSONable
from mrcs_core.equipment.turnout.turnout_configuration import TurnoutConfiguration
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


    # ----------------------------------------------------------------------------------------------------------------

    def up_link_for_config(self, config: TurnoutConfiguration) -> SegmentLink | None:
        up_link = self.up_link

        if up_link is None:
            return None

        return up_link.link_for_config(config.position(self.label))


    def down_link_for_config(self, config: TurnoutConfiguration) -> SegmentLink | None:
        down_link = self.down_link

        if down_link is None:
            return None

        return down_link.link_for_config(config.position(self.label))


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
    def construct_from_jdict(cls, jdict) -> Segment:
        label = jdict.get('label')
        length = jdict.get('length')

        up_link = SegmentLink.construct_from_jdict(jdict.get('up_link'))
        down_link = SegmentLink.construct_from_jdict(jdict.get('down_link'))

        return cls(label, length, up_link, down_link)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, label: str, length: int, up_link: SegmentLink | None, down_link: SegmentLink | None):
        super().__init__(label, length, up_link, down_link)


    def __eq__(self, other):
        try:
            return (self.label == other.label and self.length == other.length and
                    self.up_link == other.up_link and self.down_link == other.down_link)
        except (AttributeError, TypeError):
            return False


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        jdict = OrderedDict()

        jdict['type'] = self.type_name()

        jdict['label'] = self.label
        jdict['length'] = self.length

        jdict['up_link'] = self.up_link
        jdict['down_link'] = self.down_link

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
    def construct_from_jdict(cls, jdict) -> Segment:
        label = jdict.get('label')
        length = jdict.get('length')

        up_link = SegmentLink.construct_from_jdict(jdict.get('up_link'))
        down_link = SegmentLink.construct_from_jdict(jdict.get('down_link'))

        return cls(label, length, up_link, down_link)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, label: str, length: int, up_link: SegmentLink | None, down_link: SegmentLink | None):
        super().__init__(label, length, up_link, down_link)


    def __eq__(self, other):
        try:
            return (self.label == other.label and self.length == other.length and
                    self.up_link == other.up_link and self.down_link == other.down_link)
        except (AttributeError, TypeError):
            return False


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        jdict = OrderedDict()

        jdict['type'] = self.type_name()

        jdict['label'] = self.label
        jdict['length'] = self.length

        jdict['up_link'] = self.up_link
        jdict['down_link'] = self.down_link

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return (f'TurnoutSegment:{{label:{self.label}, length:{self.length}, '
                f'up_link:{self.up_link}, down_link:{self.down_link}}}')
