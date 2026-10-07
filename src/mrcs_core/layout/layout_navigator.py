"""
Created on 20 Sep 2026

@author: Bruno Beloff (bbeloff@me.com)

An ordered collection of Blocks and Platforms, making up a complete layout

The LayoutNavigator structure separates the business logic - implemented here - from the object lifecycle functions
implemented by the Layout class.
"""

from abc import ABC
from collections import OrderedDict

from mrcs_core.data.dot import Dot
from mrcs_core.equipment.block.block_enums import BlockHeading
from mrcs_core.equipment.turnout.turnout_configuration import TurnoutConfiguration
from mrcs_core.layout.block.block import Block
from mrcs_core.layout.block.block_abstract import BlockAbstract
from mrcs_core.layout.platform.platform import Platform
from mrcs_core.layout.platform.platform_location import PlatformLocation
from mrcs_core.layout.route import Route
from mrcs_core.layout.segment.segment import Segment
from mrcs_core.layout.segment.segment_location import SegmentLocation
from mrcs_core.layout.segment.turnout_abstract import TurnoutAbstract
from mrcs_core.layout.segment.turnout_segment import TurnoutSegment
from mrcs_core.layout.station.station import Station


# --------------------------------------------------------------------------------------------------------------------

class LayoutNavigator(ABC):
    """
    An ordered collection of Blocks and Stations, making up a complete layout
    """


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, blocks: OrderedDict[str, Block], stations: OrderedDict[str, Station]):
        self.__blocks = blocks
        self.__stations = stations


    # ----------------------------------------------------------------------------------------------------------------

    def validate(self) -> None:
        # are all block addresses unique?
        addresses = []
        for block in self.blocks:
            if block.address in addresses:
                raise ValueError(f"Duplicate block address {block.address.shortform} in {block.label}.")
            addresses.append(block.address)

        # are all turnout addresses unique?
        addresses = []
        for block_label, segment in self.block_segments():
            if segment.address is None:
                continue
            if segment.address in addresses:
                raise ValueError(f"Duplicate turnout address {segment.address} in {segment.label}.")
            addresses.append(segment.address)

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
            this_location = SegmentLocation(block_label, segment.label)

            reciprocal = False
            for next_location in segment.next_locations():
                next_segment = self.segment(next_location)
                next_locations = [] if next_segment is None else next_segment.next_locations()

                if this_location in next_locations:
                    reciprocal = True
                    break

            if not reciprocal and self.segment_count > 1:
                raise ValueError(f"No reciprocal link for segment label {segment.label} in block {block_label}.")

        # do platform origins exist in the layout?
        for station in self.stations:
            for platform in station.platforms:
                if self.segment(platform.origin) is None:
                    raise ValueError(f'Platform {platform.label} in station {station.label} has a non-existent origin '
                                     f'{platform.origin.dot_path}.')


    # ----------------------------------------------------------------------------------------------------------------

    def segment_route(self, config: TurnoutConfiguration, heading: BlockHeading, start: SegmentLocation,
                      end: SegmentLocation) -> Route:
        path = Route()

        found = self.block_segment(start)
        if found is None:
            raise ValueError(f'Start location not found:{start.dot_path}.')

        block_label, segment = found

        while True:
            path.append(config, block_label, segment)

            if SegmentLocation(block_label, segment.label) == end:
                return path

            next_location = segment.next_location(config, heading)
            if next_location is None:
                raise ValueError(f'End location {end.dot_path} is not reachable from location {start.dot_path} '
                                 f'with heading {heading.name} - turnout configuration may be incorrect.')

            found = self.block_segment(next_location)
            if found is None:
                raise ValueError(f'Malformed layout - segment not found for next location {next_location.dot_path}.')

            block_label, segment = found


    def platform_route(self, config: TurnoutConfiguration, heading: BlockHeading, start: PlatformLocation,
                       end: PlatformLocation) -> Route:
        start_platform = self.platform(start)
        if start_platform is None:
            raise ValueError(f'Start platform not found:{start.dot_path}.')

        end_platform = self.platform(end)
        if end_platform is None:
            raise ValueError(f'End platform not found:{end.dot_path}.')

        # TODO: length calculation depends on station offset, station length and heading

        # start_segment = self.segment(start_station.origin)
        # end_segment = self.segment(end_station.origin)

        return self.segment_route(config, heading, start_platform.origin, end_platform.origin)


    # ----------------------------------------------------------------------------------------------------------------

    def block_abstract(self) -> BlockAbstract:
        block_statuses = [block.status() for block in self.blocks]

        return BlockAbstract(block_statuses)


    def turnout_abstract(self) -> TurnoutAbstract:
        turnout_statuses = [segment.status(block_label) for block_label, segment in self.block_segments() if
                            isinstance(segment, TurnoutSegment)]

        return TurnoutAbstract(turnout_statuses)


    # ----------------------------------------------------------------------------------------------------------------

    def block_report(self, block_label: str | None, segment_label: str | None) -> list[Block]:
        if block_label is None:
            return [block.segment_report(None) for block in self.blocks]

        block = self.__blocks[block_label]  # may raise KeyError(block_label)

        try:
            return [block.segment_report(segment_label)]
        except KeyError as exc:
            raise KeyError(Dot.path(block_label, exc.args[0]))


    def station_report(self, station_label: str | None, platform_label: int | None) -> list[Station]:
        if station_label is None:
            return [station.platform_report(None) for station in self.stations]

        station = self.__stations[station_label]  # may raise KeyError

        try:
            return [station.platform_report(platform_label)]
        except KeyError as exc:
            raise KeyError(Dot.path(station_label, exc.args[0]))


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def blocks(self):
        return tuple(self.__blocks.values())


    def block(self, label: str):
        try:
            return self.__blocks[label]
        except KeyError:
            return None


    # ----------------------------------------------------------------------------------------------------------------

    def segment(self, location: SegmentLocation) -> Segment | None:
        block = self.block(location.block_label)
        if block is None:
            return None

        return block.segment(location.segment_label)


    def block_segment(self, location: SegmentLocation) -> tuple[str, Segment] | None:
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


    @property
    def segment_locations(self):
        locations = set()

        for block in self.blocks:
            for segment in block.segments:
                locations.add(SegmentLocation(block.label, segment.label))

        return list(locations)


    @property
    def segment_count(self):
        count = 0

        for block in self.blocks:
            count += len(block.segments)

        return count


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def stations(self):
        return tuple(self.__stations.values())


    @property
    def station_labels(self):
        return tuple(self.__stations.keys())


    def station(self, label: str):
        try:
            return self.__stations[label]
        except KeyError:
            return None


    # ----------------------------------------------------------------------------------------------------------------

    def platform(self, location: PlatformLocation) -> Platform | None:
        station = self.station(location.station_label)
        if station is None:
            return None

        return station.platform(location.platform_label)


    @property
    def platform_locations(self):
        locations = set()

        for station in self.stations:
            for platform in station.platforms:
                locations.add(PlatformLocation(station.label, platform.label))

        return list(locations)
