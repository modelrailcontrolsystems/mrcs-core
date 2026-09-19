"""
Created on 14 Sep 2026

@author: Bruno Beloff (bbeloff@me.com)

A route through a Layout, made up of a sequence of path edges
"""

from collections import OrderedDict
from typing import Any, Self

from mrcs_core.data.json import JSONable
from mrcs_core.inventory.layout.location import Location
from mrcs_core.inventory.segment.segment import Segment


# --------------------------------------------------------------------------------------------------------------------

class PathEdge(JSONable):
    """
    a path component
    """


    @classmethod
    def construct_from_jdict(cls, jdict) -> Self:
        segment_type_name = jdict.get('type')
        length = jdict.get('length')
        location = Location.construct_from_jdict(jdict.get('location'))

        return cls(segment_type_name, length, location)


    @classmethod
    def construct(cls, block_label: str, segment: Segment) -> Self:
        return cls(segment.type_name(), segment.length, Location(block_label, segment.label))


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, segment_type_name: str, length: int, location: Location):
        self.__segment_type_name = segment_type_name
        self.__length = length
        self.__location = location


    def __eq__(self, other: Any):
        try:
            return (self.segment_type_name == other.segment_type_name and self.length == other.length and
                    self.location == other.location)
        except (AttributeError, TypeError):
            return False


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        jdict = OrderedDict()

        jdict['type'] = self.segment_type_name
        jdict['length'] = self.length
        jdict['location'] = self.location

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def segment_type_name(self):
        return self.__segment_type_name


    @property
    def length(self):
        return self.__length


    @property
    def location(self):
        return self.__location


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return (f'PathEdge:{{segment_type_name:{self.segment_type_name}, length:{self.length}, '
                f'location:{self.location}}}')


# --------------------------------------------------------------------------------------------------------------------

class Path(JSONable):
    """
    a route through a Layout
    """


    @classmethod
    def construct_from_jdict(cls, jdict) -> Self:
        edges = [PathEdge.construct_from_jdict(edge_jdict) for edge_jdict in jdict]
        return cls(*edges)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, *edges: PathEdge):
        self.__edges = list(edges)


    def __eq__(self, other: Any):
        try:
            return self.edges == other.edges
        except (AttributeError, TypeError):
            return False


    # ----------------------------------------------------------------------------------------------------------------

    def append(self, block_label: str, segment: Segment):
        self.edges.append(PathEdge.construct(block_label, segment))


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        return self.edges


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def edges(self):
        return self.__edges


    @property
    def total_length(self) -> int:
        return sum(edge.length for edge in self.edges)


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        edges = '[' + ', '.join([str(edge) for edge in self.edges]) + ']'
        return f'Path:{{edges:{edges}}}'
