"""
Created on 9 Jul 2026

@author: Bruno Beloff (bbeloff@me.com)

An ordered collection of Blocks, making up one complete layout
"""

from collections import OrderedDict
from typing import Any

from mrcs_core.data.json import MultiPersistentJSONable
from mrcs_core.equipment.block.block_enums import BlockHeading
from mrcs_core.equipment.turnout.turnout_configuration import TurnoutConfiguration
from mrcs_core.inventory.block.block import Block
from mrcs_core.inventory.layout.location import Location
from mrcs_core.inventory.layout.path import Path
from mrcs_core.inventory.segment.segment import Segment


# --------------------------------------------------------------------------------------------------------------------

class Layout(MultiPersistentJSONable):
    """
    An ordered collection of Blocks, making up one complete layout
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

        return cls(label, description, blocks, name=name)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, label: str, description: str, blocks: OrderedDict[str, Block], name=None):
        super().__init__(name)

        self.__label = label
        self.__description = description
        self.__blocks = blocks


    def __eq__(self, other: Any):
        try:
            return self.label == other.label and self.description == other.description and self.blocks == other.blocks
        except (AttributeError, TypeError):
            return False


    def __lt__(self, other: Any):
        return self.label < other.label


    # ----------------------------------------------------------------------------------------------------------------

    def validate(self) -> None:
        # are all block labels unique?
        labels = []
        for block in self.blocks:
            if block.label in labels:
                raise ValueError(f"Duplicate block label: {block.label}.")
            labels.append(block.label)

        # are all segment labels unique within their block?
        for block in self.blocks:
            labels = []
            for segment in block.segments:
                if segment.label in labels:
                    raise ValueError(f"Duplicate segment label: {segment.label} in block {block.label}.")
                labels.append(segment.label)

        # does every segment link have a location in the layout?
        for block in self.blocks:
            for segment in block.segments:
                for next_location in segment.next_locations():
                    if self.segment(next_location) is None:
                        raise ValueError(f'Segment {segment.label} in block {block.label} has an invalid '
                                         f'next_location: {next_location}.')

        # does every segment have a reciprocal link?
        for block in self.blocks:
            for segment in block.segments:
                this_location = Location(block.label, segment.label)

                reciprocal = False
                for next_location in segment.next_locations():
                    next_segment = self.segment(next_location)
                    next_locations = [] if next_segment is None else next_segment.next_locations()

                    if this_location in next_locations:
                        reciprocal = True
                        break

                if not reciprocal:
                    raise ValueError(f"No reciprocal link for segment label {segment.label} in block {block.label}.")


    def path(self, config: TurnoutConfiguration, heading: BlockHeading, start: Location, end: Location) -> Path:
        path = Path()

        found = self.block_segment(start)
        if found is None:
            raise ValueError(f'Start location not found:{start.shortform}.')

        block_label, segment = found

        while True:
            path.append(block_label, segment)

            if Location(block_label, segment.label) == end:
                return path

            next_location = segment.next_location(config, heading)
            if next_location is None:
                raise ValueError(f'End location {end.shortform} is not reachable from location {start.shortform} '
                                 f'with heading {heading.name} - turnout configuration may be incorrect.')

            found = self.block_segment(next_location)
            if found is None:
                raise ValueError(f'Malformed layout - segment not found for next location {next_location.shortform}.')

            block_label, segment = found


    # ----------------------------------------------------------------------------------------------------------------

    def segment(self, location: Location) -> Segment | None:
        block = self.block(location.block_label)
        if block is None:
            return None

        return block.segment(location.segment_label)


    def block_segment(self, location: Location) -> tuple[str, Segment] | None:
        block = self.block(location.block_label)
        if block is None:
            return None

        return block.label, block.segment(location.segment_label)


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        jdict = OrderedDict()

        jdict['label'] = self.label
        jdict['description'] = self.description
        jdict['blocks'] = self.blocks

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def label(self):
        return self.__label


    @property
    def description(self):
        return self.__description


    @property
    def blocks(self):
        return tuple(self.__blocks.values())


    def block(self, label):
        try:
            return self.__blocks[label]
        except KeyError:
            return None


    @property
    def locations(self):
        locations = set()

        for block in self.blocks:
            for segment in block.segments:
                locations.add(Location(block.label, segment.label))

        return list(locations)


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        blocks = '[' + ', '.join([str(block) for block in self.blocks]) + ']'
        return f'Layout:{{name:{self.name}, label:{self.label}, description:{self.description}, blocks:{blocks}}}'
