"""
Created on 6 Jul 2026

@author: Bruno Beloff (bbeloff@me.com)

The current status of a turnout
The label of the TurnoutStatus is found from the Turnout Inventory,
which maps TurnoutStatus addresses to TurnoutStatus labels

{
    "type": "TurnoutStatus",
    "label": "TE01",
    "block_label": "BN01",
    "addr": 3,
    "position": "P1"
}
"""

from collections import OrderedDict

from mrcs_core.data.json import JSONable
from mrcs_core.equipment.turnout.turnout_enums import TurnoutPosition


# --------------------------------------------------------------------------------------------------------------------

class TurnoutStatus(JSONable):
    """
    The current status of a turnout
    """


    @classmethod
    def construct_from_jdict(cls, jdict) -> TurnoutStatus:
        label = jdict.get('label')
        block_label = jdict.get('block_label')

        address = jdict.get('addr')

        # may raise KeyError
        position = TurnoutPosition[jdict.get('position')]

        return cls(label, block_label, address, position)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, label: str, block_label: str, address: int, position: TurnoutPosition):
        self.__label = label
        self.__block_label = block_label
        self.__address = address
        self.__position = position


    def __eq__(self, other):
        try:
            return (self.label == other.label and self.block_label == other.block_label and
                    self.address == other.address and self.position == other.position)
        except (AttributeError, TypeError):
            return False


    def __lt__(self, other):
        return self.label < other.label


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def has_known_position(self) -> bool:
        return bool(self.position != TurnoutPosition.UNKNOWN)


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        jdict = OrderedDict()

        jdict['type'] = self.type_name()

        jdict['label'] = self.label
        jdict['block_label'] = self.block_label
        jdict['addr'] = self.address
        jdict['position'] = self.position.name

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def label(self):
        return self.__label


    @property
    def block_label(self):
        return self.__block_label


    @property
    def address(self):
        return self.__address


    @property
    def position(self):
        return self.__position


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return (f'TurnoutStatus:{{label:{self.label}, block_label:{self.block_label}, address:{self.address}, '
                f'position:{self.position.name}}}')
