"""
Created on 2 Jul 2026

@author: Bruno Beloff (bbeloff@me.com)

The current status of a block

Classes in support of the Rocco Z21 DCC command station:
https://www.z21.eu/en/products/z21
"""

from collections import OrderedDict

from mrcs_core.data.json import JSONable
from mrcs_core.equipment.block.block_enums import BlockDirection, BlockVoltage
from mrcs_core.equipment.block.block_occupant import BlockOccupant


# --------------------------------------------------------------------------------------------------------------------

class BlockStatus(JSONable):
    """
    The current status of a block
    """


    @classmethod
    def construct_from_jdict(cls, jdict) -> BlockStatus | None:
        if not jdict:
            return None

        id = jdict.get('id')

        # may raise KeyError
        direction = BlockDirection[jdict.get('direction')]

        # may raise KeyError
        voltage = BlockVoltage[jdict.get('voltage')]

        occupants = [BlockOccupant.construct_from_jdict(occupant_jdict) for occupant_jdict in
                     jdict.get('occupants', [])]

        return cls(id, direction, voltage, *occupants)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, id: str, direction: BlockDirection, voltage: BlockVoltage, *occupants: BlockOccupant):
        self._id = id
        self._direction = direction
        self._voltage = voltage
        self._occupants = occupants


    def __eq__(self, other):
        try:
            return (self.id == other.id and self.direction == other.direction and self.direction == other.direction and
                    self.occupants == other.occupants)
        except (AttributeError, TypeError):
            return False


    def __lt__(self, other):
        return self.id < other.id


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        jdict = OrderedDict()

        jdict['type'] = self.type_name()

        jdict['id'] = self.id
        jdict['direction'] = self.direction.name
        jdict['voltage'] = self.voltage.name
        jdict['occupants'] = self.occupants

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def id(self):
        return self._id


    @property
    def direction(self):
        return self._direction


    @property
    def voltage(self):
        return self._voltage


    @property
    def occupants(self):
        return self._occupants


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        occupants = '[' + ', '.join([str(occupant) for occupant in self.occupants]) + ']'
        return (f'BlockStatus:{{id:{self.id}, direction:{self.direction.name}, voltage:{self.voltage.name}, '
                f'occupants:{occupants}}}')
