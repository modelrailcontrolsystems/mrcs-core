"""
Created on 24 Oct 2026

@author: Bruno Beloff (bbeloff@me.com)

A route through a Layout, made up of a sequence of segments, together with turnout conditions
"""

from collections import OrderedDict
from typing import Any, Self

from mrcs_core.data.json import JSONable
from mrcs_core.equipment.block.block_enums import BlockHeading
from mrcs_core.equipment.turnout.turnout_configuration import TurnoutConfiguration
from mrcs_core.layout.segment.segment_location import SegmentLocation


# --------------------------------------------------------------------------------------------------------------------

class Route(JSONable):
    """
    a route through a Layout
    """


    @classmethod
    def construct_from_prolog(cls, pdict) -> Self:
        direction = BlockHeading.construct_from_prolog(pdict.get('Dir'))
        length = int(pdict.get('Length'))
        configuration = TurnoutConfiguration.construct_from_prolog(pdict.get('ConfOut'))
        segments = [SegmentLocation.construct_from_prolog(pname) for pname in pdict.get('Route')]

        return cls(direction, length, configuration, segments)


    @classmethod
    def construct_from_jdict(cls, jdict) -> Self:
        direction = BlockHeading[jdict.get('direction')]
        length = int(jdict.get('length'))
        configuration = TurnoutConfiguration.construct_from_jdict(jdict.get('conf'))
        segments = [SegmentLocation.construct_from_jdict(segment) for segment in jdict.get('segments')]

        return cls(direction, length, configuration, segments)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, direction: BlockHeading, length: int, configuration: TurnoutConfiguration,
                 segments: list[SegmentLocation]):
        self.__direction = direction
        self.__length = length
        self.__configuration = configuration
        self.__segments = segments


    def __eq__(self, other: Any):
        try:
            return (self.direction == other.direction and self.length == other.length and
                    self.configuration == other.configuration and self.segments == other.segments)
        except (AttributeError, TypeError):
            return False


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        jdict = OrderedDict()

        jdict['direction'] = self.direction.name
        jdict['length'] = self.length
        jdict['conf'] = self.configuration
        jdict['segments'] = self.segments

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def direction(self):
        return self.__direction


    @property
    def length(self):
        return self.__length


    @property
    def configuration(self):
        return self.__configuration


    @property
    def segments(self):
        return self.__segments


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        segments = '[' + ', '.join(map(str, self.segments)) + ']'

        return (f'Route:{{direction:{self.direction}, length:{self.length}, '
                f'configuration:{self.configuration}, segments:{segments}}}')
