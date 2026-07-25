"""
Created on 9 Jul 2026

@author: Bruno Beloff (bbeloff@me.com)

A component of a Layout, monitored by a block detector
Blocks contain track segments and turnouts.
A Block may have a fixed direction, or may be reversible.
"""

from collections import OrderedDict

from mypy.types import Any

from mrcs_core.data.json import JSONable
from mrcs_core.equipment.block.block_occupant import BlockOccupant
from mrcs_core.inventory.block.block_operation import BlockOperation


# --------------------------------------------------------------------------------------------------------------------

class Block(JSONable):
    """
    A component of a layout, monitored by a block detector
    """


    @classmethod
    def construct_from_jdict(cls, jdict) -> Block:
        label = jdict.get('label')
        operation = BlockOperation(jdict.get('operation'))
        next_up_block = jdict.get('next_up_block')  # TODO: this may depend on turnout status
        next_down_block = jdict.get('next_down_block')  # TODO: this may depend on turnout status

        segments = [BlockOccupant.construct_from_jdict(occupant_jdict) for occupant_jdict in jdict.get('segments', [])]

        return cls(label, operation, next_up_block, next_down_block, *segments)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, label: str, operation: BlockOperation, next_up_block: str | None, next_down_block: str | None,
                 *segments: BlockOccupant):
        self.__label = label
        self.__operation = operation
        self.__next_up_block = next_up_block
        self.__next_down_block = next_down_block
        self.__segments = segments


    def __eq__(self, other: Any):
        try:
            return self.label == other.label and self.segments == other.segments
        except (AttributeError, TypeError):
            return False


    def __lt__(self, other: Any):
        return self.label < other.label  # TODO: ordering is by linked list chain


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        jdict = OrderedDict()

        jdict['label'] = self.label
        jdict['operation'] = self.operation.name
        jdict['next_up_block'] = self.next_up_block
        jdict['next_down_block'] = self.next_down_block
        jdict['segments'] = self.segments

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def label(self):
        return self.__label


    @property
    def operation(self):
        return self.__operation


    @property
    def next_up_block(self):
        return self.__next_up_block


    @property
    def next_down_block(self):
        return self.__next_down_block


    @property
    def segments(self):
        return sorted(self.__segments)


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        segments = '[' + ', '.join([str(block) for block in self.segments]) + ']'

        return (f'Block:{{label:{self.label}, operation:{self.operation.name}, next_up_block:{self.next_up_block}, '
                f'next_down_block:{self.next_down_block}, segments:{segments}}}')
