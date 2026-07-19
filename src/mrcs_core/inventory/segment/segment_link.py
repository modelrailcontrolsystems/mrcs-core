"""
Created on 10 Jul 2026

@author: Bruno Beloff (bbeloff@me.com)

A link between segments
"""

from abc import ABC, abstractmethod
from collections import OrderedDict

from mrcs_core.data.json import JSONable
from mrcs_core.equipment.turnout.turnout_enums import TurnoutPosition


# --------------------------------------------------------------------------------------------------------------------

class SegmentLink(JSONable, ABC):
    """
    The common interface for segment links
    """


    @abstractmethod
    def link_for_config(self, position: TurnoutPosition | None) -> SegmentLink | None:
        pass


    def find_segment(self, layout):
        # TODO: implement find_segment(..)
        pass


# --------------------------------------------------------------------------------------------------------------------

class SimpleSegmentLink(SegmentLink):
    """
    A simple link between segments
    """


    @classmethod
    def construct_from_jdict(cls, jdict) -> SimpleSegmentLink | None:
        if jdict is None:
            return None

        return cls(jdict[0], jdict[1])


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, block_label: str, segment_label: str):
        self.__block_label = block_label
        self.__segment_label = segment_label


    def __eq__(self, other):
        try:
            return self.block_label == other.block_label and self.segment_label == other.segment_label
        except (AttributeError, TypeError):
            return False


    # ----------------------------------------------------------------------------------------------------------------

    def link_for_config(self, position: TurnoutPosition | None) -> SegmentLink | None:
        return self


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        return [self.block_label, self.segment_label]


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def block_label(self):
        return self.__block_label


    @property
    def segment_label(self):
        return self.__segment_label


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return f'SimpleSegmentLink:{{block_label:{self.block_label}, segment_label:{self.segment_label}}}'


# --------------------------------------------------------------------------------------------------------------------

class SwitchedSegmentLink(SegmentLink):
    """
    A link between segments, dependent on turnout position
    """


    @classmethod
    def construct_from_jdict(cls, jdict) -> SwitchedSegmentLink | None:
        if jdict is None:
            return None

        p0 = jdict.get('p0')
        link_p0 = None if p0 is None else SimpleSegmentLink(p0[0], p0[1])

        p1 = jdict.get('p1')
        link_p1 = None if p1 is None else SimpleSegmentLink(p1[0], p1[1])

        return cls(link_p0, link_p1)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, link_p0: SimpleSegmentLink | None, link_p1: SimpleSegmentLink | None):
        self.__link_p0 = link_p0
        self.__link_p1 = link_p1


    def __eq__(self, other):
        try:
            return self.link_p0 == other.link_p0 and self.link_p1 == other.link_p1
        except (AttributeError, TypeError):
            return False


    # ----------------------------------------------------------------------------------------------------------------

    def link_for_config(self, position: TurnoutPosition | None) -> SegmentLink | None:
        if position == TurnoutPosition.P0:
            return self.link_p0

        if position == TurnoutPosition.P1:
            return self.link_p1

        raise ValueError(f'invalid position:{position}')


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        jdict = OrderedDict()

        jdict['p0'] = self.link_p0
        jdict['p1'] = self.link_p1

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def link_p0(self):
        return self.__link_p0


    @property
    def link_p1(self):
        return self.__link_p1


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return f'SwitchedSegmentLink:{{link_p0:{self.link_p0}, link_p1:{self.link_p1}}}'
