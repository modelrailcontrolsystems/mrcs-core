"""
Created on 1 Oct 2026

@author: Bruno Beloff (bbeloff@me.com)

The address of a Block, in the form DetectorNumber/ChannelNumber
"""

from typing import Any, Self

from mrcs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class BlockAddress(JSONable):
    """
    the address of a Block, in the form DetectorNumber/ChannelNumber
    """


    @classmethod
    def construct_from_shortform(cls, shortform: str) -> Self:
        pieces = shortform.split('/')

        if len(pieces) != 2 or not pieces[0] or not pieces[1]:
            raise ValueError(shortform)

        return cls(int(pieces[0]), int(pieces[1]))


    @classmethod
    def construct_from_jdict(cls, jdict) -> Self:
        return cls.construct_from_shortform(jdict)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, detector: int, channel: int):
        self.__detector = detector
        self.__channel = channel


    # noinspection PyProtectedMember
    def __eq__(self, other: Any):
        try:
            return self.detector == other.detector and self.channel == other.channel
        except (AttributeError, TypeError):
            return False


    def __lt__(self, other):
        if self.detector < other.detector:
            return True

        if self.detector > other.detector:
            return False

        return self.channel < other.channel


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        return self.shortform


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def detector(self):
        return self.__detector


    @property
    def channel(self):
        return self.__channel


    # ----------------------------------------------------------------------------------------------------------------


    @property
    def shortform(self):
        return '/'.join((str(self.detector), str(self.channel)))


    def __str__(self, *args, **kwargs):
        return f'BlockAddress:{{detector:{self.detector}, channel:{self.channel}}}'
