"""
Created on 9 Jul 2026

@author: Bruno Beloff (bbeloff@me.com)

A collection of Blocks, making up one complete layout
"""

from collections import OrderedDict

from mrcs_core.data.json import JSONable
from mrcs_core.equipment.block.block_occupant import BlockOccupant
from mrcs_core.inventory.block.block import Block


# --------------------------------------------------------------------------------------------------------------------

class Layout(JSONable):
    """
    A collection of Blocks, making up one complete layout
    """


    @classmethod
    def construct_from_jdict(cls, jdict) -> Layout:
        label = jdict.get('label')

        blocks = [BlockOccupant.construct_from_jdict(occupant_jdict) for occupant_jdict in
                  jdict.get('blocks', [])]

        return cls(label, *blocks)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, label: str, *blocks: Block):
        self.__label = label
        self.__blocks = blocks


    def __eq__(self, other):
        try:
            return self.label == other.label and self.blocks == other.blocks
        except (AttributeError, TypeError):
            return False


    def __lt__(self, other):
        return self.label < other.label


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        jdict = OrderedDict()

        jdict['label'] = self.label
        jdict['blocks'] = self.blocks

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def label(self):
        return self.__label


    @property
    def blocks(self):
        return sorted(self.__blocks)


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        blocks = '[' + ', '.join([str(block) for block in self.blocks]) + ']'
        return f'Layout:{{label:{self.label}, blocks:{blocks}}}'
