"""
Created on 16 Jun 2026

@author: Bruno Beloff (bbeloff@me.com)

An MPU occupant of a block

Classes in support of the Rocco Z21 DCC command station:
https://www.z21.eu/en/products/z21
"""

from collections import OrderedDict
from typing import Any

from mrcs_core.data.json import JSONable
from mrcs_core.equipment.block.block_enums import BlockOccupantFace


# --------------------------------------------------------------------------------------------------------------------

class BlockOccupant(JSONable):
    """
    An MPU occupant of a block
    """


    @classmethod
    def construct_from_jdict(cls, jdict) -> BlockOccupant:
        mpu_address = jdict.get('addr')

        # may raise KeyError
        face = BlockOccupantFace[jdict.get('face')]

        return cls(mpu_address, face)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, mpu_address: int, face: BlockOccupantFace):
        self._mpu_address = mpu_address
        self._face = face


    def __eq__(self, other: Any):
        try:
            return self.mpu_address == other.mpu_address and self.face == other.face
        except (AttributeError, TypeError):
            return False


    def __lt__(self, other: Any):
        return self.mpu_address < other.mpu_address


    # ----------------------------------------------------------------------------------------------------------------

    def has_mpu_address(self):
        return self.mpu_address > 0


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        jdict = OrderedDict()

        jdict['addr'] = self.mpu_address
        jdict['face'] = self.face.name

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def mpu_address(self):
        return self._mpu_address


    @property
    def face(self):
        return self._face


    # ----------------------------------------------------------------------------------------------------------------

    # noinspection PyUnresolvedReferences
    def __str__(self, *args, **kwargs):
        return f'BlockOccupant:{{mpu_address:{self.mpu_address}, face:{self.face.name}}}'
