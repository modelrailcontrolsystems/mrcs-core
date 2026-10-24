"""
Created on 18 Oct 2026

@author: Bruno Beloff (bbeloff@me.com)

Translation between python and prolog segments
"""

from typing import Any

from mrcs_core.layout.segment.segment_location import SegmentLocation


# --------------------------------------------------------------------------------------------------------------------

class PrologSegment(object):
    """
    A segment assertion
    """


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, location: SegmentLocation, length: int):
        self.__location = location
        self.__length = length


    def __eq__(self, other: Any) -> bool:
        return self.location == other.location and self.length == other.length


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def location(self):
        return self.__location


    @property
    def length(self):
        return self.__length


    # ----------------------------------------------------------------------------------------------------------------

    def __repr__(self):
        return f'segment({self.location.as_prolog()}, {self.length}).'


    def __str__(self, *args, **kwargs):
        return f'PrologSegment:{{location:{self.location}, length:{self.length}}}'
