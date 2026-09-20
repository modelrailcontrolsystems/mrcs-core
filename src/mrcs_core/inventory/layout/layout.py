"""
Created on 9 Jul 2026

@author: Bruno Beloff (bbeloff@me.com)

A persistent ordered collection of Blocks and Platforms, making up a complete layout

Business logic is implemented in the abstract superclass LayoutNavigator, with object lifecycle functions
implemented here.
"""

from collections import OrderedDict
from typing import Any

from mrcs_core.data.json import MultiPersistentJSONable
from mrcs_core.inventory.block.block import Block
from mrcs_core.inventory.layout.layout_navigator import LayoutNavigator
from mrcs_core.inventory.platform.platform import Platform
from mrcs_core.inventory.platform.platform_label import PlatformLabel


# --------------------------------------------------------------------------------------------------------------------

class Layout(LayoutNavigator, MultiPersistentJSONable):
    """
    A persistent ordered collection of Blocks and Platforms, making up a complete layout
    """

    __FILENAME = "layout.json"


    @classmethod
    def persistence_location(cls, name):
        filename = cls.__FILENAME if name is None else '_'.join((name, cls.__FILENAME))
        return cls.layouts_dir(), filename


    @classmethod
    def construct_from_jdict(cls, jdict, name=None) -> Layout:
        label = jdict.get('label')
        description = jdict.get('description')

        blocks = OrderedDict()
        for block_jdict in jdict.get('blocks', []):
            block = Block.construct_from_jdict(block_jdict)
            blocks[block.label] = block

        platforms = OrderedDict()
        for platform_jdict in jdict.get('platforms', []):
            platform = Platform.construct_from_jdict(platform_jdict)
            platforms[platform.label] = platform

        return cls(label, description, blocks, platforms, name=name)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, label: str, description: str, blocks: OrderedDict[str, Block],
                 platforms: OrderedDict[PlatformLabel, Platform], name=None):
        LayoutNavigator.__init__(self, blocks, platforms)
        MultiPersistentJSONable.__init__(self, name)

        self.__label = label
        self.__description = description


    def __eq__(self, other: Any):
        try:
            return (self.label == other.label and self.description == other.description and
                    self.blocks == other.blocks and self.platforms == other.platforms)
        except (AttributeError, TypeError):
            return False


    def __lt__(self, other: Any):
        return self.label < other.label


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        jdict = OrderedDict()

        jdict['label'] = self.label
        jdict['description'] = self.description
        jdict['blocks'] = self.blocks
        jdict['platforms'] = self.platforms

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def label(self):
        return self.__label


    @property
    def description(self):
        return self.__description


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        blocks = '[' + ', '.join([str(block) for block in self.blocks]) + ']'
        platforms = '[' + ', '.join([str(platform) for platform in self.platforms]) + ']'

        return (f'Layout:{{name:{self.name}, label:{self.label}, description:{self.description}, '
                f'blocks:{blocks}, platforms:{platforms}}}')
