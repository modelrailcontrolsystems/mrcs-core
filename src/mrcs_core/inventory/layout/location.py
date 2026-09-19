"""
Created on 12 Sep 2026

@author: Bruno Beloff (bbeloff@me.com)

A location on a layout, identifying a segment within a block
"""

from typing import Any

from mrcs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class Location(JSONable):
    """
    A location on a layout
    """


    @classmethod
    def construct_from_shortform(cls, shortform: str) -> Location:
        pieces = shortform.split('/')

        if len(pieces) != 2 or len(pieces[0]) < 4 or len(pieces[1]) < 4:
            raise ValueError(shortform)

        return cls(pieces[0], pieces[1])


    @classmethod
    def construct_from_jdict(cls, jdict) -> Location:
        return cls(jdict[0], jdict[1])


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, block_label: str, segment_label: str):
        self.__block_label = block_label
        self.__segment_label = segment_label


    def __hash__(self):
        return hash((self.block_label, self.segment_label))


    def __eq__(self, other: Any):
        try:
            return self.block_label == other.block_label and self.segment_label == other.segment_label
        except (AttributeError, TypeError):
            return False


    def __lt__(self, other: Any):
        if self.block_label < other.block_label:
            return True

        if self.block_label > other.block_label:
            return False

        return self.segment_label < other.segment_label


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

    @property
    def shortform(self):
        return '/'.join((self.block_label, self.segment_label))


    def __str__(self, *args, **kwargs):
        return f'Location:{{block_label:{self.block_label}, segment_label:{self.segment_label}}}'
