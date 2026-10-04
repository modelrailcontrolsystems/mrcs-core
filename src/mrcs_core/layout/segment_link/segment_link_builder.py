"""
Created on 26 Sep 2026

@author: Bruno Beloff (bbeloff@me.com)

A link between segments
"""

from mrcs_core.layout.segment_link.fixed_segment_link import FixedSegmentLink
from mrcs_core.layout.segment_link.segment_link import SegmentLink
from mrcs_core.layout.segment_link.switched_segment_link import SwitchedSegmentLink


# --------------------------------------------------------------------------------------------------------------------

class SegmentLinkBuilder(object):
    """
    The common interface for segment links
    """


    @classmethod
    def construct_from_jdict(cls, jdict) -> SegmentLink | None:
        if jdict is None:
            return None

        type_name = jdict.get('type')

        if type_name == FixedSegmentLink.type_name():
            return FixedSegmentLink.construct_from_jdict(jdict)

        if type_name == SwitchedSegmentLink.type_name():
            return SwitchedSegmentLink.construct_from_jdict(jdict)

        raise TypeError(f'invalid segment type: {type_name}')
