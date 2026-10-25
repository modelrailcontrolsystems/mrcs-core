"""
Created on 9 Jul 2026

@author: Bruno Beloff (bbeloff@me.com)

A simple represenation of the state of all the Turnouts
"""

from typing import Any, Dict, Self

from mrcs_core.data.json import JSONable
from mrcs_core.equipment.turnout.turnout_enums import TurnoutPosition
from mrcs_core.equipment.turnout.turnout_status import TurnoutStatus


# --------------------------------------------------------------------------------------------------------------------

class TurnoutConfiguration(JSONable):
    """
    A simple represenation of the state of all the Turnouts
    """


    @classmethod
    def construct_from_prolog(cls, pdict) -> Self:
        positions = {pair[0].upper(): TurnoutPosition.construct_from_prolog(pair[1]) for pair in pdict}

        return cls(positions)


    @classmethod
    def construct_from_jdict(cls, jdict) -> Self:
        positions = {label: TurnoutPosition[position] for label, position in jdict.items()}

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
        return {label: position.name for label, position in self.positions.items()}


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def positions(self):
        return dict(sorted(self.__positions.items()))


    def position(self, label: str) -> TurnoutPosition | None:
        try:
            return self.__positions[label]
        except KeyError:
            return None


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        positions = '{' + ', '.join(f'{label}:{position.name}' for label, position in self.__positions.items()) + '}'
        return f'TurnoutConfiguration:{{positions:{positions}}}'
