"""
Created on 20 Sep 2026

@author: Bruno Beloff (bbeloff@me.com)

An ordered collection of Blocks and Platforms, making up a complete layout

The LayoutNavigator structure separates the business logic - implemented here - from the object lifecycle functions
implemented by the Layout class.
"""

from abc import ABC
from collections import OrderedDict

from mrcs_core.equipment.block.block_enums import BlockHeading
from mrcs_core.equipment.turnout.turnout_configuration import TurnoutConfiguration
from mrcs_core.inventory.block.block import Block
from mrcs_core.inventory.layout.location import Location
from mrcs_core.inventory.layout.path import Path
from mrcs_core.inventory.platform.platform import Platform
from mrcs_core.inventory.platform.platform_label import PlatformLabel
from mrcs_core.inventory.segment.segment import Segment


# --------------------------------------------------------------------------------------------------------------------

class LayoutNavigator(ABC):
    """
    An ordered collection of Blocks and Platforms, making up a complete layout
    """


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, blocks: OrderedDict[str, Block], platforms: OrderedDict[PlatformLabel, Platform]):
        self.__blocks = blocks
        self.__platforms = platforms


    # ----------------------------------------------------------------------------------------------------------------

    def validate(self) -> None:
        # are all block addresses unique?
        addresses = []
        for block in self.blocks:
            if block.address in addresses:
                raise ValueError(f"Duplicate block address {block.address} in {block.label}.")
            addresses.append(block.address)

        # are all turnout labels unique?
        turnout_labels = []
        for block_label, segment in self.block_segments():
            if segment.turnout_label is None:
                continue
            if segment.turnout_label in turnout_labels:
                raise ValueError(f"Duplicate turnout label {segment.turnout_label} in {block_label}.")
            turnout_labels.append(segment.turnout_label)

        # are all segment labels unique within their block?
        for block in self.blocks:
            labels = []
            for segment in block.segments:
                if segment.label in labels:
                    raise ValueError(f"Duplicate segment label {segment.label} in block {block.label}.")
                labels.append(segment.label)

        # does every segment link have a location in the layout?
        for block_label, segment in self.block_segments():
            for next_location in segment.next_locations():
                found = self.block_segment(next_location)
                if found is None:
                    raise ValueError(f'Segment {segment.label} in block {block_label} has an invalid '
                                     f'next_location: {next_location}.')

                next_block_label, next_segment = found
                if block_label == next_block_label and segment.label == next_segment.label:
                    raise ValueError(f'Segment {segment.label} in block {block_label} is pointing to itself.')

        # does every segment have a reciprocal link?
        for block_label, segment in self.block_segments():
            this_location = Location(block_label, segment.label)

            reciprocal = False
            for next_location in segment.next_locations():
                next_segment = self.segment(next_location)
                next_locations = [] if next_segment is None else next_segment.next_locations()

                if this_location in next_locations:
                    reciprocal = True
                    break

            if not reciprocal:
                raise ValueError(f"No reciprocal link for segment label {segment.label} in block {block_label}.")

        # do platform origins exist in the layout?
        for platform in self.platforms:
            if self.segment(platform.origin) is None:
                raise ValueError(f'The platform {platform.label.shortform} has a non-existent origin '
                                 f'{platform.origin.shortform}.')


    def segment_path(self, config: TurnoutConfiguration, heading: BlockHeading, start: Location, end: Location) -> Path:
        path = Path()

        found = self.block_segment(start)
        if found is None:
            raise ValueError(f'Start location not found:{start.shortform}.')

        block_label, segment = found

        while True:
            path.append(config, block_label, segment)

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


    def platform_path(self, config: TurnoutConfiguration, heading: BlockHeading, start: PlatformLabel,
                      end: PlatformLabel) -> Path:
        start_platform = self.platform(start)
        if start_platform is None:
            raise ValueError(f'Start platform not found:{start.shortform}.')

        end_platform = self.platform(end)
        if end_platform is None:
            raise ValueError(f'End platform not found:{end.shortform}.')

        # TODO: length calculation depends on platform offset, platform length and heading

        # start_segment = self.segment(start_platform.origin)
        # end_segment = self.segment(end_platform.origin)

        return self.segment_path(config, heading, start_platform.origin, end_platform.origin)


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

        segment = block.segment(location.segment_label)
        if segment is None:
            return None

        return block.label, segment


    def block_segments(self):
        for block in self.blocks:
            for segment in block.segments:
                yield block.label, segment


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def blocks(self):
        return tuple(self.__blocks.values())


    def block(self, label: str):
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


    @property
    def platforms(self):
        return tuple(self.__platforms.values())


    @property
    def platform_labels(self):
        return tuple(self.__platforms.keys())


    def platform(self, label: PlatformLabel):
        try:
            return self.__platforms[label]
        except KeyError:
            return None
