"""
Created on 16 Jun 2026

@author: Bruno Beloff (bbeloff@me.com)

An MPU occupant of a block

Classes in support of the Rocco Z21 DCC command station:
https://www.z21.eu/en/products/z21
"""

from collections import OrderedDict

from mrcs_core.data.json import JSONable
from mrcs_core.equipment.block.block_occupant_face import BlockOccupantFace


# --------------------------------------------------------------------------------------------------------------------

class BlockOccupantReport(JSONable):
    """
    An MPU occupant of a block
    """


    @classmethod
    def construct_from_jdict(cls, jdict) -> BlockOccupantReport:
        address = jdict.get('addr')

        # may raise KeyError
        face = BlockOccupantFace[jdict.get('face')]

        return cls(address, face)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, address: int, face: BlockOccupantFace):
        self._address = address
        self._face = face


    def __eq__(self, other):
        try:
            return self.address == other.address and self.face == other.face
        except (AttributeError, TypeError):
            return False


    def __lt__(self, other):
        return self.address < other.address


    # ----------------------------------------------------------------------------------------------------------------

    def has_address(self):
        return self.address > 0


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        jdict = OrderedDict()

        jdict['addr'] = self.address
        jdict['face'] = self.face.name

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def address(self):
        return self._address


    @property
    def face(self):
        return self._face


    # ----------------------------------------------------------------------------------------------------------------

    # noinspection PyUnresolvedReferences
    def __str__(self, *args, **kwargs):
        return f'BlockOccupantReport:{{address:{self.address}, face:{self.face.name}}}'
