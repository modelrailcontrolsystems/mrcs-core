"""
Created on 10 Jul 2026

@author: Bruno Beloff (bbeloff@me.com)

A link between segments
"""

from abc import ABC, abstractmethod

from mrcs_core.data.json import JSONable
from mrcs_core.equipment.turnout.turnout_enums import TurnoutPosition
from mrcs_core.inventory.segment.segment_location import SegmentLocation


# --------------------------------------------------------------------------------------------------------------------

class SegmentLink(JSONable, ABC):
    """
    The common interface for segment links
    """


    # ----------------------------------------------------------------------------------------------------------------

    @abstractmethod
    def selected_next_location(self, turnout_position: TurnoutPosition | None) -> SegmentLocation | None:
        pass


    @abstractmethod
    def next_locations(self) -> list[SegmentLocation]:
        pass
