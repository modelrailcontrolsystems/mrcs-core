"""
Created on 2 Jul 2026

@author: Bruno Beloff (bbeloff@me.com)

The current status of a block
The label of the BlockStatus is found from the Block Inventory, which maps BlockReport IDs to BlockStatus labels

{
    "type": "BlockStatus",
    "label": "N01",
    "addr": "5/6",
    "direction": "UP",
    "voltage": "OCCUPIED_WITH_VOLTAGE",
    "occupants": [
        {
            "addr": 4660,
            "face": "FWD"
        },
        {
            "addr": 17767,
            "face": "REV"
        }
    ]
}
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
    def construct_from_jdict(cls, jdict) -> BlockStatus:
        label = jdict.get('label')
        block_address = jdict.get('addr')

        # may raise KeyError
        direction = BlockDirection[jdict.get('direction')]

        # may raise KeyError
        voltage = BlockVoltage[jdict.get('voltage')]

        occupants = [BlockOccupant.construct_from_jdict(occupant_jdict) for occupant_jdict in
                     jdict.get('occupants', [])]

        return cls(label, block_address, direction, voltage, *occupants)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, label: str, block_address: str, direction: BlockDirection, voltage: BlockVoltage,
                 *occupants: BlockOccupant):
        self._label = label
        self._block_address = block_address
        self._direction = direction
        self._voltage = voltage
        self._occupants = occupants


    def __eq__(self, other):
        try:
            return (
                    self.label == other.label and self.block_address == other.block_address and
                    self.direction == other.direction and self.direction == other.direction and
                    self.occupants == other.occupants)
        except (AttributeError, TypeError):
            return False


    def __lt__(self, other):
        return self.label < other.label


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        jdict = OrderedDict()

        jdict['type'] = self.type_name()

        jdict['label'] = self.label
        jdict['addr'] = self.block_address
        jdict['direction'] = self.direction.name
        jdict['voltage'] = self.voltage.name
        jdict['occupants'] = self.occupants

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def label(self):
        return self._label


    @property
    def block_address(self):
        return self._block_address


    @property
    def direction(self):
        return self._direction


    @property
    def voltage(self):
        return self._voltage


    @property
    def occupants(self):
        return sorted(self._occupants)


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        occupants = '[' + ', '.join([str(occupant) for occupant in self.occupants]) + ']'
        return (
            f'BlockStatus:{{label:{self.label}, block_address:{self.block_address}, direction:{self.direction.name}, '
            f'voltage:{self.voltage.name}, occupants:{occupants}}}')
