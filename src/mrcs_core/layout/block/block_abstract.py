"""
Created on 27 Sep 2026

@author: Bruno Beloff (bbeloff@me.com)

A compendium of block status objects

The intended use of the BlockAbstract is to populate an empty block database table. To this end, it should provide
BlockStatus objects which have identity, but no information about the configuration of each block.
"""

from typing import Any, List, Self

from mrcs_core.data.json import JSONable
from mrcs_core.equipment.block.block_status import BlockStatus


# --------------------------------------------------------------------------------------------------------------------

class BlockAbstract(JSONable):
    """
    a compendium of block status objects
    """


    @classmethod
    def construct_from_jdict(cls, jdict: Any) -> Self:
        items = [BlockStatus.construct_from_jdict(item) for item in jdict]
        return cls(items)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, items: List[BlockStatus]):
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
        return f'BlockAbstract:{{items:{items}}}'
