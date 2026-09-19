"""
Created on 9 Jul 2026

@author: Bruno Beloff (bbeloff@me.com)

A simple represenation of the state of all the Turnouts, typically within a Block
Intended for use in determining the active path edges in a Block design
"""

from typing import Any, Dict, OrderedDict, Self

from mrcs_core.data.json import JSONable
from mrcs_core.equipment.turnout.turnout_enums import TurnoutPosition
from mrcs_core.equipment.turnout.turnout_status import TurnoutStatus


# --------------------------------------------------------------------------------------------------------------------

class TurnoutConfiguration(JSONable):
    """
    A simple represenation of the state of all the Turnouts, typically within a Block
    """


    @classmethod
    def construct_from_jdict(cls, jdict) -> Self:
        positions = OrderedDict()
        for label, position in jdict.items():
            positions[label] = TurnoutPosition[position]

        return cls(positions)


    @classmethod
    def construct_from_turnouts(cls, *turnouts: TurnoutStatus) -> TurnoutConfiguration:
        positions = {turnout.label: turnout.position for turnout in sorted(turnouts)}

        return cls(positions)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, positions: Dict[str, TurnoutPosition]):
        self.__positions = positions


    def __eq__(self, other: Any):
        try:
            return self.positions == other.positions
        except (AttributeError, TypeError):
            return False


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self) -> bool:
        return all(position.is_valid() for position in self.__positions.values())


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        return {label: position.name for label, position in self.__positions.items()}


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def positions(self):
        return self.__positions


    def position(self, label: str) -> TurnoutPosition | None:
        try:
            return self.__positions[label]
        except KeyError:
            return None


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        positions = '{' + ', '.join(f'{label}:{position.name}' for label, position in self.__positions.items()) + '}'
        return f'TurnoutConfiguration:{{positions:{positions}}}'
