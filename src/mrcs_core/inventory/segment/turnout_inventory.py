"""
Created on 14 Aug 2026

@author: Bruno Beloff (bbeloff@me.com)

an inventory of turnouts
"""

from typing import Any, List, Self

from mrcs_core.data.json import JSONable
from mrcs_core.equipment.turnout.turnout_status import TurnoutStatus


# --------------------------------------------------------------------------------------------------------------------

class TurnoutInventory(JSONable):
    """
    an inventory of turnouts
    """


    @classmethod
    def construct_from_jdict(cls, jdict: Any) -> Self:
        items = [TurnoutStatus.construct_from_jdict(item) for item in jdict]
        return cls(items)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, items: List[TurnoutStatus]):
        super().__init__()
        self.__items = items


    def __len__(self):
        return len(self.__items)


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        return self.items


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def items(self):
        return sorted(self.__items)


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        items = '[' + ', '.join(str(item) for item in self.items) + ']'
        return f'TurnoutInventory:{{items:{items}}}'
