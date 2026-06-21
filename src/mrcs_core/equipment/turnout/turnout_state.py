"""
Created on 13 Jun 2026

@author: Bruno Beloff (bbeloff@me.com)

A turnout state

Based on code:
https://github.com/botmonster/z21aio/tree/main
"""

from collections import OrderedDict

from mrcs_core.data.json import JSONable
from mrcs_core.equipment.turnout.turnout_position import TurnoutPosition


# --------------------------------------------------------------------------------------------------------------------

class TurnoutState(JSONable):
    """
    A turnout state
    """


    @classmethod
    def construct_from_jdict(cls, jdict) -> TurnoutState | None:
        if not jdict:
            return None

        type_name = jdict.get('type')

        if type_name != cls.__name__:
            raise TypeError(f'required type:{cls.__name__} got:{type_name}')

        address = jdict.get('addr')

        # may raise KeyError
        position = TurnoutPosition[jdict.get('position')]

        return cls(address, position)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, address: int, position: TurnoutPosition):
        self.__address = address
        self.__position = position


    def __eq__(self, other):
        try:
            return self.address == other.address and self.position == other.position
        except (AttributeError, TypeError):
            return False


    def __lt__(self, other):
        return self.address < other.address


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        jdict = OrderedDict()

        jdict['type'] = self.__class__.__name__

        jdict['addr'] = self.address
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
    def address(self):
        return self.__address


    @property
    def position(self):
        return self.__position


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return f'{self.__class__.__name__}:{{address:{self.address}, position:{self.position.name}}}'
