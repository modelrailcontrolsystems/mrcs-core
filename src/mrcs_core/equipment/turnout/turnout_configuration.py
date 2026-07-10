"""
Created on 9 Jul 2026

@author: Bruno Beloff (bbeloff@me.com)

A simple represenation of the state of the Turnouts, typically within a Block
Intended for use in determining the active paths in a Block or Sector design
"""

from typing import Dict

from mrcs_core.equipment.turnout.turnout_enums import TurnoutPosition
from mrcs_core.equipment.turnout.turnout_status import TurnoutStatus


# --------------------------------------------------------------------------------------------------------------------

class TurnoutConfiguration(object):
    """
    A simple represenation of the state of the Turnouts, typically within a Block
    """


    @classmethod
    def construct_from_turnouts(cls, *turnouts: TurnoutStatus) -> TurnoutConfiguration:
        positions = {turnout.label: turnout.position for turnout in turnouts}

        return cls(positions)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, positions: Dict[str, TurnoutPosition]):
        self.__positions = positions


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self) -> bool:
        return all(position.is_valid() for position in self.__positions.values())


    # ----------------------------------------------------------------------------------------------------------------

    def position(self, label: str) -> TurnoutPosition | None:
        try:
            return self.__positions[label]
        except KeyError:
            return None


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        positions = '{' + ', '.join(f'{label}:{position.name}' for label, position in self.__positions.items()) + '}'
        return f'TurnoutConfiguration:{{positions:{positions}}}'
