"""
Created on 3 Oct 2026

@author: Bruno Beloff (bbeloff@me.com)

python -m unittest -v unit/inventory/layout/test_layout_navigator.py

https://realpython.com/python-testing/
https://www.jetbrains.com/help/pycharm/creating-tests.html
"""

import json
import unittest
from collections import OrderedDict
from pathlib import Path as FilePath

from mrcs_core.equipment.block.block_address import BlockAddress
from mrcs_core.equipment.block.block_enums import BlockHeading
from mrcs_core.equipment.turnout.turnout_configuration import TurnoutConfiguration
from mrcs_core.equipment.turnout.turnout_enums import TurnoutPosition
from mrcs_core.equipment.turnout.turnout_status import TurnoutStatus
from mrcs_core.layout.block.block import Block
from mrcs_core.layout.block.block_operation import BlockOperation
from mrcs_core.layout.layout import Layout
from mrcs_core.layout.layout_navigator import LayoutNavigator
from mrcs_core.layout.platform.platform import Platform
from mrcs_core.layout.platform.platform_alignment import PlatformAlignment
from mrcs_core.layout.platform.platform_location import PlatformLocation
from mrcs_core.layout.route import Route, RouteSegment
from mrcs_core.layout.segment.segment_location import SegmentLocation
from mrcs_core.layout.segment.track_segment import TrackSegment
from mrcs_core.layout.segment.turnout_segment import TurnoutSegment
from mrcs_core.layout.segment_link.fixed_segment_link import FixedSegmentLink
from mrcs_core.layout.station.station import Station


# --------------------------------------------------------------------------------------------------------------------

class _DummyLayoutNavigator(LayoutNavigator):
    """
    a concrete LayoutNavigator, without the Layout persistence machinery
    """

    pass


# --------------------------------------------------------------------------------------------------------------------

class TestLayoutNavigator(unittest.TestCase):
    __data_dir = FilePath(__file__).parent / 'data'

    __layout = None
    __turnouts_p0 = None
    __turnouts_p1 = None


    @classmethod
    def setUpClass(cls):
        with open(cls.__data_dir / 'test_001_layout.json') as fp:
            cls.__layout = Layout.construct_from_jdict(json.load(fp), name='test_001')

        cls.__turnouts_p0 = cls.__load_turnout_configuration('turnouts_p0.json')
        cls.__turnouts_p1 = cls.__load_turnout_configuration('turnouts_p1.json')


    @classmethod
    def __load_turnout_configuration(cls, filename):
        with open(cls.__data_dir / filename) as fp:
            turnouts = [TurnoutStatus.construct_from_jdict(jdict) for jdict in json.load(fp)]

        return TurnoutConfiguration.construct_from_turnouts(*turnouts)


    # validate fixtures ----------------------------------------------------------------------------------------------

    @staticmethod
    def __track(label, up=None, down=None, length=100):
        up_link = None if up is None else FixedSegmentLink(SegmentLocation.construct_from_dot_path(up))
        down_link = None if down is None else FixedSegmentLink(SegmentLocation.construct_from_dot_path(down))

        return TrackSegment(label, up_link, down_link, length)


    @staticmethod
    def __block(label, detector, channel, *segments, keys=None):
        keys = [segment.label for segment in segments] if keys is None else keys

        return Block(label, BlockAddress(detector, channel), BlockOperation.REVERSIBLE,
                     OrderedDict(zip(keys, segments)))


    @staticmethod
    def __navigator(*blocks, stations=()):
        return _DummyLayoutNavigator(OrderedDict((block.label, block) for block in blocks),
                                     OrderedDict((station.label, station) for station in stations))


    @classmethod
    def __valid_blocks(cls):
        # B01.S01 <-> B02.S01
        return (cls.__block('B01', 1, 1, cls.__track('S01', up='B02.S01')),
                cls.__block('B02', 1, 2, cls.__track('S01', down='B01.S01')))


    # validate -------------------------------------------------------------------------------------------------------

    def test_validate(self):
        self.__layout.validate()


    def test_validate_minimal(self):
        self.__navigator(*self.__valid_blocks()).validate()


    def test_validate_single_segment(self):
        # a lone segment cannot have a reciprocal link
        self.__navigator(self.__block('B01', 1, 1, self.__track('S01'))).validate()


    def test_validate_empty(self):
        self.__navigator().validate()


    def test_validate_duplicate_block_address(self):
        navigator = self.__navigator(self.__block('B01', 1, 1, self.__track('S01', up='B02.S01')),
                                     self.__block('B02', 1, 1, self.__track('S01', down='B01.S01')))

        with self.assertRaises(ValueError) as ctx:
            navigator.validate()

        self.assertEqual('Duplicate block address 1/1 in B02.', str(ctx.exception))


    def test_validate_duplicate_turnout_address(self):
        navigator = self.__navigator(self.__block('B01', 1, 1, TurnoutSegment('S01', 7, None, None, 50, 70)),
                                     self.__block('B02', 1, 2, TurnoutSegment('S01', 7, None, None, 50, 70)))

        with self.assertRaises(ValueError) as ctx:
            navigator.validate()

        self.assertEqual('Duplicate turnout address 7 in S01.', str(ctx.exception))


    def test_validate_duplicate_segment_label(self):
        navigator = self.__navigator(self.__block('B01', 1, 1, self.__track('S01'), self.__track('S01'),
                                                  keys=['k1', 'k2']))

        with self.assertRaises(ValueError) as ctx:
            navigator.validate()

        self.assertEqual('Duplicate segment label S01 in block B01.', str(ctx.exception))


    def test_validate_invalid_next_location(self):
        navigator = self.__navigator(self.__block('B01', 1, 1, self.__track('S01', up='B99.S01')))

        with self.assertRaises(ValueError) as ctx:
            navigator.validate()

        self.assertEqual('Segment S01 in block B01 has an invalid next_location: '
                         'SegmentLocation:{block_label:B99, segment_label:S01}.', str(ctx.exception))


    def test_validate_self_link(self):
        navigator = self.__navigator(self.__block('B01', 1, 1, self.__track('S01', up='B01.S01')))

        with self.assertRaises(ValueError) as ctx:
            navigator.validate()

        self.assertEqual('Segment S01 in block B01 is pointing to itself.', str(ctx.exception))


    def test_validate_no_reciprocal_link(self):
        navigator = self.__navigator(self.__block('B01', 1, 1, self.__track('S01', up='B02.S01')),
                                     self.__block('B02', 1, 2, self.__track('S01')))

        with self.assertRaises(ValueError) as ctx:
            navigator.validate()

        self.assertEqual('No reciprocal link for segment label S01 in block B01.', str(ctx.exception))


    def test_validate_platform_origin_not_found(self):
        platform = Platform(1, PlatformAlignment.UP_LEFT, SegmentLocation('B99', 'S01'), 20, 120)
        station = Station('Alpha', OrderedDict({1: platform}))
        navigator = self.__navigator(*self.__valid_blocks(), stations=(station,))

        with self.assertRaises(ValueError) as ctx:
            navigator.validate()

        self.assertEqual('Platform 1 in station Alpha has a non-existent origin B99.S01.', str(ctx.exception))


    # segment_route ---------------------------------------------------------------------------------------------------

    def test_segment_route_up_p0(self):
        path = self.__layout.segment_route(self.__turnouts_p0, BlockHeading.UP,
                                           SegmentLocation('B01', 'S01'), SegmentLocation('B03', 'S01'))

        expected = Route(RouteSegment('TrackSegment', 100, SegmentLocation('B01', 'S01')),
                         RouteSegment('TrackSegment', 100, SegmentLocation('B02', 'S01')),
                         RouteSegment('TurnoutSegment', 50, SegmentLocation('B02', 'S02')),
                         RouteSegment('TrackSegment', 150, SegmentLocation('B03', 'S01')))

        self.assertEqual(expected, path)
        self.assertEqual(400, path.total_length)


    def test_segment_route_up_p1(self):
        path = self.__layout.segment_route(self.__turnouts_p1, BlockHeading.UP,
                                           SegmentLocation('B01', 'S01'), SegmentLocation('B04', 'S01'))

        expected = Route(RouteSegment('TrackSegment', 100, SegmentLocation('B01', 'S01')),
                         RouteSegment('TrackSegment', 100, SegmentLocation('B02', 'S01')),
                         RouteSegment('TurnoutSegment', 70, SegmentLocation('B02', 'S02')),
                         RouteSegment('TrackSegment', 200, SegmentLocation('B04', 'S01')))

        self.assertEqual(expected, path)
        self.assertEqual(470, path.total_length)


    def test_segment_route_down(self):
        path = self.__layout.segment_route(self.__turnouts_p0, BlockHeading.DOWN,
                                           SegmentLocation('B03', 'S01'), SegmentLocation('B01', 'S01'))

        self.assertEqual([SegmentLocation('B03', 'S01'), SegmentLocation('B02', 'S02'),
                          SegmentLocation('B02', 'S01'), SegmentLocation('B01', 'S01')],
                         [edge.location for edge in path.edges])
        self.assertEqual(400, path.total_length)


    def test_segment_route_start_is_end(self):
        path = self.__layout.segment_route(self.__turnouts_p0, BlockHeading.UP,
                                           SegmentLocation('B01', 'S01'), SegmentLocation('B01', 'S01'))

        self.assertEqual(Route(RouteSegment('TrackSegment', 100, SegmentLocation('B01', 'S01'))), path)


    def test_segment_route_start_not_found(self):
        with self.assertRaises(ValueError) as ctx:
            self.__layout.segment_route(self.__turnouts_p0, BlockHeading.UP,
                                        SegmentLocation('B99', 'S01'), SegmentLocation('B03', 'S01'))

        self.assertEqual('Start location not found:B99.S01.', str(ctx.exception))


    def test_segment_route_unreachable(self):
        # with the turnout at P1, B03 is not reachable
        with self.assertRaises(ValueError) as ctx:
            self.__layout.segment_route(self.__turnouts_p1, BlockHeading.UP,
                                        SegmentLocation('B01', 'S01'), SegmentLocation('B03', 'S01'))

        self.assertEqual('End location B03.S01 is not reachable from location B01.S01 with heading UP - '
                         'turnout configuration may be incorrect.', str(ctx.exception))


    def test_segment_route_wrong_heading(self):
        with self.assertRaises(ValueError):
            self.__layout.segment_route(self.__turnouts_p0, BlockHeading.DOWN,
                                        SegmentLocation('B01', 'S01'), SegmentLocation('B03', 'S01'))


    def test_segment_route_unassigned_heading(self):
        with self.assertRaises(ValueError):
            self.__layout.segment_route(self.__turnouts_p0, BlockHeading.UNASSIGNED,
                                        SegmentLocation('B01', 'S01'), SegmentLocation('B03', 'S01'))


    def test_segment_route_unknown_turnout_position(self):
        config = TurnoutConfiguration({'S02': TurnoutPosition.UNKNOWN})

        with self.assertRaises(ValueError):
            self.__layout.segment_route(config, BlockHeading.UP,
                                        SegmentLocation('B01', 'S01'), SegmentLocation('B03', 'S01'))


    # platform_route --------------------------------------------------------------------------------------------------

    def test_platform_route(self):
        path = self.__layout.platform_route(self.__turnouts_p0, BlockHeading.DOWN,
                                            PlatformLocation('Alpha', 1), PlatformLocation('Alpha', 1))

        self.assertEqual(Route(RouteSegment('TrackSegment', 150, SegmentLocation('B03', 'S01'))), path)


    def test_platform_route_start_not_found(self):
        with self.assertRaises(ValueError) as ctx:
            self.__layout.platform_route(self.__turnouts_p0, BlockHeading.UP,
                                         PlatformLocation('Beta', 1), PlatformLocation('Alpha', 1))

        self.assertEqual('Start platform not found:Beta.1.', str(ctx.exception))


    def test_platform_route_end_not_found(self):
        with self.assertRaises(ValueError) as ctx:
            self.__layout.platform_route(self.__turnouts_p0, BlockHeading.UP,
                                         PlatformLocation('Alpha', 1), PlatformLocation('Alpha', 9))

        self.assertEqual('End platform not found:Alpha.9.', str(ctx.exception))


    # inventories ----------------------------------------------------------------------------------------------------

    def test_block_abstract(self):
        abstract = self.__layout.block_abstract()

        self.assertEqual(4, len(abstract))
        self.assertEqual(['B01', 'B02', 'B03', 'B04'], [status.label for status in abstract.items])
        self.assertEqual([BlockAddress(1, 1), BlockAddress(1, 2), BlockAddress(1, 3), BlockAddress(1, 4)],
                         [status.address for status in abstract.items])


    def test_turnout_abstract(self):
        abstract = self.__layout.turnout_abstract()

        self.assertEqual(1, len(abstract))
        self.assertEqual(TurnoutStatus('S02', 'B02', 1, TurnoutPosition.UNKNOWN), abstract.items[0])


    # block_report -------------------------------------------------------------------------------------------------

    def test_block_report_all(self):
        report = self.__layout.block_report(None, None)

        self.assertEqual(list(self.__layout.blocks), report)


    def test_block_report_block(self):
        report = self.__layout.block_report('B02', None)

        self.assertEqual([self.__layout.block('B02')], report)


    def test_block_report_block_segment(self):
        report = self.__layout.block_report('B02', 'S02')

        self.assertEqual(1, len(report))
        self.assertEqual('B02', report[0].label)
        self.assertEqual((self.__layout.segment(SegmentLocation('B02', 'S02')),), report[0].segments)


    def test_block_report_block_not_found(self):
        with self.assertRaises(KeyError) as ctx:
            self.__layout.block_report('B99', None)

        self.assertEqual('B99', ctx.exception.args[0])


    def test_block_report_segment_not_found(self):
        with self.assertRaises(KeyError) as ctx:
            self.__layout.block_report('B02', 'S99')

        self.assertEqual('B02.S99', ctx.exception.args[0])


    # station_report ------------------------------------------------------------------------------------------------

    def test_station_report_all(self):
        report = self.__layout.station_report(None, None)

        self.assertEqual(list(self.__layout.stations), report)


    def test_station_report_station(self):
        report = self.__layout.station_report('Alpha', None)

        self.assertEqual([self.__layout.station('Alpha')], report)


    def test_station_report_station_platform(self):
        report = self.__layout.station_report('Alpha', 2)

        self.assertEqual(1, len(report))
        self.assertEqual('Alpha', report[0].label)
        self.assertEqual((self.__layout.platform(PlatformLocation('Alpha', 2)),), report[0].platforms)


    def test_station_report_station_not_found(self):
        with self.assertRaises(KeyError) as ctx:
            self.__layout.station_report('Beta', None)

        self.assertEqual('Beta', ctx.exception.args[0])


    def test_station_report_platform_not_found(self):
        with self.assertRaises(KeyError) as ctx:
            self.__layout.station_report('Alpha', 9)

        self.assertEqual('Alpha.9', ctx.exception.args[0])


    # blocks and segments --------------------------------------------------------------------------------------------

    def test_blocks(self):
        self.assertEqual(['B01', 'B02', 'B03', 'B04'], [block.label for block in self.__layout.blocks])


    def test_block(self):
        self.assertEqual('B02', self.__layout.block('B02').label)
        self.assertIsNone(self.__layout.block('B99'))


    def test_segment(self):
        segment = self.__layout.segment(SegmentLocation('B02', 'S02'))

        self.assertIsInstance(segment, TurnoutSegment)
        self.assertEqual('S02', segment.label)


    def test_segment_not_found(self):
        self.assertIsNone(self.__layout.segment(SegmentLocation('B99', 'S01')))
        self.assertIsNone(self.__layout.segment(SegmentLocation('B02', 'S99')))


    def test_block_segment(self):
        found = self.__layout.block_segment(SegmentLocation('B02', 'S02'))
        assert found is not None

        block_label, segment = found

        self.assertEqual('B02', block_label)
        self.assertEqual('S02', segment.label)


    def test_block_segment_not_found(self):
        self.assertIsNone(self.__layout.block_segment(SegmentLocation('B99', 'S01')))
        self.assertIsNone(self.__layout.block_segment(SegmentLocation('B02', 'S99')))


    def test_block_segments(self):
        self.assertEqual([('B01', 'S01'), ('B02', 'S01'), ('B02', 'S02'), ('B03', 'S01'), ('B04', 'S01')],
                         [(block_label, segment.label) for block_label, segment in self.__layout.block_segments()])


    def test_segment_locations(self):
        self.assertEqual([SegmentLocation('B01', 'S01'), SegmentLocation('B02', 'S01'), SegmentLocation('B02', 'S02'),
                          SegmentLocation('B03', 'S01'), SegmentLocation('B04', 'S01')],
                         sorted(self.__layout.segment_locations))


    def test_segment_count(self):
        self.assertEqual(5, self.__layout.segment_count)
        self.assertEqual(2, self.__navigator(*self.__valid_blocks()).segment_count)
        self.assertEqual(0, self.__navigator().segment_count)


    # stations and platforms -----------------------------------------------------------------------------------------

    def test_stations(self):
        self.assertEqual(['Alpha'], [station.label for station in self.__layout.stations])


    def test_station_labels(self):
        self.assertEqual(('Alpha',), self.__layout.station_labels)


    def test_station(self):
        self.assertEqual('Alpha', self.__layout.station('Alpha').label)
        self.assertIsNone(self.__layout.station('Beta'))


    def test_platform(self):
        platform = self.__layout.platform(PlatformLocation('Alpha', 2))
        assert platform is not None

        self.assertEqual(2, platform.label)
        self.assertEqual(SegmentLocation('B04', 'S01'), platform.origin)


    def test_platform_not_found(self):
        self.assertIsNone(self.__layout.platform(PlatformLocation('Beta', 1)))
        self.assertIsNone(self.__layout.platform(PlatformLocation('Alpha', 9)))


    def test_platform_locations(self):
        self.assertEqual([PlatformLocation('Alpha', 1), PlatformLocation('Alpha', 2)],
                         sorted(self.__layout.platform_locations))


# --------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    unittest.main()
