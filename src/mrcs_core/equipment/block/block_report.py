"""
Created on 6 Jun 2026

@author: Bruno Beloff (bbeloff@me.com)

Block occupany detector reports

Based on the Roco 10808 detector:
https://www.roco.cc/ren/products/control/accessories/10808-z21-detector.html


Based on code:
https://github.com/botmonster/z21aio/tree/main
"""

from abc import ABC, abstractmethod
from collections import OrderedDict

from mrcs_core.data.json import JSONable
from mrcs_core.equipment.block.block_enums import BlockVoltage
from mrcs_core.equipment.block.block_id import BlockID
from mrcs_core.equipment.block.block_occupant import BlockOccupant


# --------------------------------------------------------------------------------------------------------------------

class BlockReport(JSONable, ABC):
    """
    An abstract block report
    """


    @classmethod
    def construct_from_jdict(cls, jdict) -> BlockVoltageReport | BlockOccupancyReport | None:
        if not jdict:
            return None

        type_name = jdict.get('type')

        if type_name == 'BlockVoltageReport':
            return BlockVoltageReport.construct_from_jdict(jdict)

        if type_name == 'BlockOccupancyReport':
            return BlockOccupancyReport.construct_from_jdict(jdict)

        raise TypeError(f'unsupported type:{type_name}')


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, block_id: BlockID):
        self._block_id = block_id


    def __lt__(self, other):
        return self.block_id < other.block_id


    # ----------------------------------------------------------------------------------------------------------------

    @property
    @abstractmethod
    def is_occupancy(self):
        pass


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def block_id(self):
        return self._block_id


# --------------------------------------------------------------------------------------------------------------------

class BlockVoltageReport(BlockReport):
    """
    A block report, including voltage
    """


    @classmethod
    def construct_from_jdict(cls, jdict) -> BlockVoltageReport | None:
        if not jdict:
            return None

        type_name = jdict.get('type')

        if type_name != cls.__name__:
            raise TypeError(f'required type:{cls.__name__} got:{type_name}')

        block_id = BlockID.construct_from_jdict(jdict.get('id'))

        if block_id is None:
            raise ValueError(f'missing BlockID in:{jdict}')

        # may raise KeyError
        voltage = BlockVoltage[jdict.get('voltage')]

        return cls(block_id, voltage)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, block_id: BlockID, voltage: BlockVoltage):
        super().__init__(block_id)
        self._voltage = voltage


    def __eq__(self, other):
        try:
            return self.block_id == other.block_id and self.voltage == other.voltage
        except (AttributeError, TypeError):
            return False


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        jdict = OrderedDict()

        jdict['type'] = self.type_name()

        jdict['id'] = self.block_id
        jdict['voltage'] = self.voltage.name

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def is_occupancy(self):
        return False


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def voltage(self):
        return self._voltage


    # ----------------------------------------------------------------------------------------------------------------

    # noinspection PyUnresolvedReferences
    def __str__(self, *args, **kwargs):
        return f'{self.__class__.__name__}:{{block_id:{self.block_id}, voltage:{self.voltage.name}}}'


# --------------------------------------------------------------------------------------------------------------------

class BlockOccupancyReport(BlockReport):
    """
    A block report, including occupancy
    """


    @classmethod
    def construct_from_jdict(cls, jdict) -> BlockOccupancyReport | None:
        if not jdict:
            return None

        type_name = jdict.get('type')

        if type_name != cls.__name__:
            raise TypeError(f'required type:{cls.__name__} got:{type_name}')

        block_id = BlockID.construct_from_jdict(jdict.get('id'))

        if block_id is None:
            raise ValueError(f'missing BlockID in:{jdict}')

        occupant_group = jdict.get('group')
        occupants = [BlockOccupant.construct_from_jdict(occupant) for occupant in jdict.get('occupants', [])]

        return cls(block_id, occupant_group, occupants)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, block_id: BlockID, occupant_group: int | None, occupants: list[BlockOccupant]):
        super().__init__(block_id)

        self._occupant_group = occupant_group
        self._occupants = occupants


    def __eq__(self, other):
        try:
            return (self.block_id == other.block_id and
                    self.occupant_group == other.occupant_group and self.occupants == other.occupants)
        except (AttributeError, TypeError):
            return False


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        jdict = OrderedDict()

        jdict['type'] = self.type_name()

        jdict['id'] = self.block_id
        jdict['group'] = self.occupant_group
        jdict['occupants'] = self.occupants

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def is_occupancy(self):
        return True


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def occupant_group(self):
        return self._occupant_group


    @property
    def occupants(self):
        return self._occupants


    # ----------------------------------------------------------------------------------------------------------------

    # noinspection PyUnresolvedReferences
    def __str__(self, *args, **kwargs):
        occupants = '[' + ', '.join([str(occupant) for occupant in self.occupants]) + ']'

        return (f'{self.__class__.__name__}:{{block_id:{self.block_id}, '
                f'occupant_group:{self.occupant_group}, occupants:{occupants}}}')
