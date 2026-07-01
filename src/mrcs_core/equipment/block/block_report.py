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
from mrcs_core.equipment.block.block_occupant_report import BlockOccupantReport
from mrcs_core.equipment.block.block_status import BlockStatus


# --------------------------------------------------------------------------------------------------------------------

class BlockReport(JSONable, ABC):
    """
    An abstract block report
    """


    @classmethod
    def construct_from_jdict(cls, jdict) -> BlockStatusReport | BlockOccupancyReport | None:
        if not jdict:
            return None

        return BlockStatusReport.construct_from_jdict(jdict) if 'status' in jdict else \
            BlockOccupancyReport.construct_from_jdict(jdict)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, network_id: int, reporter_address: int, reporter_input: int):
        self._network_id = network_id
        self._reporter_address = reporter_address
        self._reporter_input = reporter_input


    def __lt__(self, other):
        if self.reporter_address < other.reporter_address:
            return True

        if self.reporter_address > other.reporter_address:
            return False

        return self.reporter_input < other.reporter_input


    # ----------------------------------------------------------------------------------------------------------------

    @property
    @abstractmethod
    def is_occupancy(self):
        pass


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def network_id(self):
        return self._network_id


    @property
    def reporter_address(self):
        return self._reporter_address


    @property
    def reporter_input(self):
        return self._reporter_input


# --------------------------------------------------------------------------------------------------------------------

class BlockStatusReport(BlockReport):
    """
    A block report, including status
    """


    @classmethod
    def construct_from_jdict(cls, jdict) -> BlockStatusReport | None:
        if not jdict:
            return None

        type_name = jdict.get('type')

        if type_name != cls.__name__:
            raise TypeError(f'required type:{cls.__name__} got:{type_name}')

        network_id = jdict.get('nid')
        reporter_address = jdict.get('reporter')
        reporter_input = jdict.get('input')

        # may raise KeyError
        status = BlockStatus[jdict.get('status')]

        return cls(network_id, reporter_address, reporter_input, status)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, network_id: int, reporter_address: int, reporter_input: int, status: BlockStatus):
        super().__init__(network_id, reporter_address, reporter_input)
        self._status = status


    def __eq__(self, other):
        try:
            return (self.network_id == other.network_id and self.reporter_address == other.reporter_address and
                    self.reporter_input == other.reporter_input and self.status == other.status)
        except (AttributeError, TypeError):
            return False


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        jdict = OrderedDict()

        jdict['type'] = self.type_name()

        jdict['nid'] = self.network_id
        jdict['reporter'] = self.reporter_address
        jdict['input'] = self.reporter_input
        jdict['status'] = self.status.name

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def is_occupancy(self):
        return False


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def status(self):
        return self._status


    # ----------------------------------------------------------------------------------------------------------------

    # noinspection PyUnresolvedReferences
    def __str__(self, *args, **kwargs):
        return (f'{self.__class__.__name__}:{{network_id:0x{self.network_id:04x}, '
                f'reporter_address:{self.reporter_address}, reporter_input:{self.reporter_input}, '
                f'status:{self.status.name}}}')


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

        network_id = jdict.get('nid')
        reporter_address = jdict.get('reporter')
        reporter_input = jdict.get('input')

        occupant_group = jdict.get('group')
        occupants = [BlockOccupantReport.construct_from_jdict(occupant) for occupant in jdict.get('occupants', [])]

        return cls(network_id, reporter_address, reporter_input, occupant_group, occupants)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, network_id: int, reporter_address: int, reporter_input: int, occupant_group: int | None,
                 occupants: list[BlockOccupantReport]):
        super().__init__(network_id, reporter_address, reporter_input)

        self._occupant_group = occupant_group
        self._occupants = occupants


    def __eq__(self, other):
        try:
            return (self.network_id == other.network_id and self.reporter_address == other.reporter_address and
                    self.reporter_input == other.reporter_input and self.occupant_group == other.occupant_group and
                    self.occupants == other.occupants)
        except (AttributeError, TypeError):
            return False


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        jdict = OrderedDict()

        jdict['type'] = self.type_name()

        jdict['nid'] = self.network_id
        jdict['reporter'] = self.reporter_address
        jdict['input'] = self.reporter_input
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

        return (f'{self.__class__.__name__}:{{network_id:0x{self.network_id:04x}, '
                f'reporter_address:{self.reporter_address}, reporter_input:{self.reporter_input}, '
                f'occupant_group:{self.occupant_group}, occupants:{occupants}}}')
