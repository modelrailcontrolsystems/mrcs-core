"""
Created on 26 Sep 2026

@author: Bruno Beloff (bbeloff@me.com)

A component of a Block
"""

from mrcs_core.inventory.segment.segment import Segment
from mrcs_core.inventory.segment.track_segment import TrackSegment
from mrcs_core.inventory.segment.turnout_segment import TurnoutSegment


# --------------------------------------------------------------------------------------------------------------------

class SegmentBuilder(object):
    """
    The common interface for segment links
    """


    @classmethod
    def construct_from_jdict(cls, jdict) -> Segment:
        type_name = jdict.get('type')

        if type_name == TrackSegment.type_name():
            return TrackSegment.construct_from_jdict(jdict)

        if type_name == TurnoutSegment.type_name():
            return TurnoutSegment.construct_from_jdict(jdict)

        raise TypeError(f'invalid segment type: {type_name}')
