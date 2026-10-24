"""
Created on 18 Oct 2026

@author: Bruno Beloff (bbeloff@me.com)

Translation between prolog and python segments
"""

from enum import StrEnum, unique
from typing import Any

from mrcs_core.data.meta_enum import MetaEnum
from mrcs_core.equipment.block.block_enums import BlockHeading
from mrcs_core.equipment.turnout.turnout_enums import TurnoutPosition
from mrcs_core.layout.segment.segment_location import SegmentLocation


# --------------------------------------------------------------------------------------------------------------------


@unique
class ConstraintFormat(StrEnum, metaclass=MetaEnum):
    """
    An enumeration of all the possible PrologLinkConstraint formats
    """

    SINGLE = 'SINGLE'
    LEFT = 'LEFT'
    RIGHT = 'RIGHT'


# --------------------------------------------------------------------------------------------------------------------

class PrologLinkConstraint(object):
    """
    A constraint on a link, specifically a turnout position requirement
    """


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, location: SegmentLocation, position: TurnoutPosition, length: int):
        if not position.is_valid():
            raise ValueError(f'invalid position: {position}')

        self.__location = location
        self.__position = position
        self.__length = length


    def __hash__(self):
        return hash((self.location, self.position))


    def __eq__(self, other: Any) -> bool:
        try:
            return (self.location.segment_label == other.location.segment_label and
                    self.position == other.position and self.length == other.length)
        except (AttributeError, TypeError):
            return False


    def __lt__(self, other: Any) -> bool:
        if self.location < other.location:
            return True

        if self.location > other.location:
            return False

        return self.position < other.position


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def location(self):
        return self.__location


    @property
    def position(self):
        return self.__position


    @property
    def length(self):
        return self.__length


    # ----------------------------------------------------------------------------------------------------------------

    def as_prolog(self, fmt: ConstraintFormat):
        turnout_label = self.location.segment_label.lower()
        turnout_position = self.position.name.lower()

        conf = '-'.join((turnout_label, turnout_position))

        if fmt == ConstraintFormat.SINGLE:
            return f'add_conf({conf}, ConfsIn, ConfsOut).'

        if fmt == ConstraintFormat.LEFT:
            return f'add_conf({conf}, ConfsIn, ConfsMid),'

        if fmt == ConstraintFormat.RIGHT:
            return f'add_conf({conf}, ConfsMid, ConfsOut).'

        raise ValueError(format)


    def __str__(self, *args, **kwargs):
        return f'PrologLinkConstraint:{{location:{self.location}, position:{self.position}, length:{self.length}}}'


# --------------------------------------------------------------------------------------------------------------------

class PrologLink(object):
    """
    A link assertion
    """


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, location: SegmentLocation, next_location: SegmentLocation,
                 heading: BlockHeading, *constraints: PrologLinkConstraint):
        if not heading.is_valid():
            raise ValueError(f'invalid heading: {heading}')

        self.__location = location
        self.__next_location = next_location
        self.__heading = heading
        self.__constraints = set(constraints)


    def __eq__(self, other: Any) -> bool:
        try:
            return (self.location == other.location and self.next_location == other.next_location and
                    self.heading == other.heading and self.constraints == other.constraints)
        except (AttributeError, TypeError):
            return False


    # ----------------------------------------------------------------------------------------------------------------

    def add(self, *constraints: PrologLinkConstraint):
        for constraint in constraints:
            self.__constraints.add(constraint)


    def length(self):
        return sum([constraint.length for constraint in self.constraints])


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def location(self):
        return self.__location


    @property
    def next_location(self):
        return self.__next_location


    @property
    def heading(self):
        return self.__heading


    @property
    def constraints(self):
        return sorted(self.__constraints)


    # ----------------------------------------------------------------------------------------------------------------

    def __repr__(self):
        location = self.location.as_prolog()
        next_location = self.next_location.as_prolog()
        heading = self.heading.name.lower()
        constraints = self.constraints

        if len(constraints) == 0:
            return f'link({location}, {next_location}, 0, {heading}, Confs, Confs).'

        prolog_constraints = []

        if len(constraints) == 1:
            prolog_constraints.append(constraints.pop().as_prolog(fmt=ConstraintFormat.SINGLE))

        elif len(constraints) == 2:
            prolog_constraints.append(constraints.pop().as_prolog(fmt=ConstraintFormat.LEFT))
            prolog_constraints.append(constraints.pop().as_prolog(fmt=ConstraintFormat.RIGHT))

        return (f'link({location}, {next_location}, {self.length()}, {heading}, ConfsIn, ConfsOut) :- '
                f'{' '.join(prolog_constraints)}')


    def __str__(self, *args, **kwargs):
        constraints = '[' + ', '.join([str(constraint) for constraint in self.constraints]) + ']'

        return (f'PrologLink:{{location:{self.location}, next_location:{self.next_location}, '
                f'heading:{self.heading}, constraints:{constraints}}}')
