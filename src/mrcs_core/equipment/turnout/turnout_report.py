"""
Created on 13 Jun 2026

@author: Bruno Beloff (bbeloff@me.com)

A reported turnout state

{
  "type": "TurnoutReport",
  "addr": 3,
  "position": "P1"
}
"""

from collections import OrderedDict
from typing import Any

from mrcs_core.data.json import JSONable
from mrcs_core.equipment.turnout.turnout_enums import TurnoutPosition


# --------------------------------------------------------------------------------------------------------------------

class TurnoutReport(JSONable):
    """
    A reported turnout state
    """


    @classmethod
    def construct_from_jdict(cls, jdict) -> TurnoutReport:
        type_name = jdict.get('type')

        if type_name != cls.__name__:
            raise TypeError(f'required type:{cls.__name__} got:{type_name}')

        turnout_address = jdict.get('addr')

        # may raise KeyError
        position = TurnoutPosition[jdict.get('position')]

        return cls(turnout_address, position)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, turnout_address: int, position: TurnoutPosition):
        self.__turnout_address = turnout_address
        self.__position = position


    def __eq__(self, other: Any):
        try:
            return self.turnout_address == other.turnout_address and self.position == other.position
        except (AttributeError, TypeError):
            return False


    def __lt__(self, other: Any):
        return self.turnout_address < other.turnout_address


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        jdict = OrderedDict()

        jdict['type'] = self.type_name()

        jdict['addr'] = self.turnout_address
        jdict['position'] = self.position.name

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def is_known(self) -> bool:
        return bool(self.position != TurnoutPosition.UNKNOWN)


    @property
    def is_valid(self) -> bool:
        return bool(self.position != TurnoutPosition.INVALID)


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def turnout_address(self):
        return self.__turnout_address


    @property
    def position(self):
        return self.__position


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return f'{self.__class__.__name__}:{{turnout_address:{self.turnout_address}, position:{self.position.name}}}'
