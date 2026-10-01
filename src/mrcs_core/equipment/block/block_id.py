"""
Created on 2 Jul 2026

@author: Bruno Beloff (bbeloff@me.com)

A unique identifier for a block, as defined by its detector
Note that BlockAddress (detector, channel) is a PK, the reporter_id field is purely for validation.

Based on the Roco 10808 detector:
https://www.roco.cc/ren/products/control/accessories/10808-z21-detector.html

Based on code:
https://github.com/botmonster/z21aio/tree/main
"""

from collections import OrderedDict
from typing import Any

from mrcs_core.data.json import JSONable
from mrcs_core.equipment.block.block_address import BlockAddress


# --------------------------------------------------------------------------------------------------------------------

class BlockID(JSONable):
    """
    A unique identifier for a block, as defined by its detector
    """


    @classmethod
    def construct_from_jdict(cls, jdict) -> BlockID:
        address = BlockAddress.construct_from_jdict(jdict.get('addr'))
        reporter_id = jdict.get('rid')

        return cls(address, reporter_id)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, address: BlockAddress, reporter_id: int):
        self._address = address
        self._reporter_id = reporter_id


    def __eq__(self, other: Any):
        try:
            return self.address == other.address and self.reporter_id == other.reporter_id
        except (AttributeError, TypeError):
            return False


    def __lt__(self, other: Any):
        if self.address < other.address:
            return True

        if self.address > other.address:
            return False

        return self.reporter_id < other.reporter_id


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        jdict = OrderedDict()

        jdict['addr'] = self.address
        jdict['rid'] = self.reporter_id

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def address(self):
        return self._address


    @property
    def reporter_id(self):
        return self._reporter_id


    # ----------------------------------------------------------------------------------------------------------------

    # noinspection PyUnresolvedReferences
    def __str__(self, *args, **kwargs):
        return f'BlockID:{{address:{self.address}, reporter_id:0x{self.reporter_id:04x}}}'
