"""
Created on 20 Sep 2026

@author: Bruno Beloff (bbeloff@me.com)

python -m unittest -v unit/inventory/layout/test_layout_navigator.py

https://realpython.com/python-testing/
https://www.jetbrains.com/help/pycharm/creating-tests.html
"""

import json
import unittest
from collections import OrderedDict
from pathlib import Path

from mrcs_core.equipment.block.block_enums import BlockHeading
from mrcs_core.equipment.turnout.turnout_configuration import TurnoutConfiguration
from mrcs_core.equipment.turnout.turnout_status import TurnoutStatus
from mrcs_core.inventory.block.block import Block
from mrcs_core.inventory.block.block_operation import BlockOperation
from mrcs_core.inventory.layout.layout_navigator import LayoutNavigator
from mrcs_core.inventory.layout.location import Location
from mrcs_core.inventory.layout.path import PathEdge
from mrcs_core.inventory.platform.platform import Platform
from mrcs_core.inventory.platform.platform_alignment import PlatformAlignment
from mrcs_core.inventory.platform.platform_label import PlatformLabel
from mrcs_core.inventory.segment.segment import TrackSegment, TurnoutSegment
from mrcs_core.inventory.segment.segment_link import FixedSegmentLink


# --------------------------------------------------------------------------------------------------------------------

class _DummyLayoutNavigator(LayoutNavigator):
    pass


# --------------------------------------------------------------------------------------------------------------------

class TestLayoutNavigator(unittest.TestCase):
    __layout_filename = Path(__file__).parent / 'data' / 'test_001_layout.json'
    __layout_jdict = None

    __p0_filename = Path(__file__).parent / 'data' / 'turnouts_p0.json'
    __turnouts_p0_jdict = None

    __p1_filename = Path(__file__).parent / 'data' / 'turnouts_p1.json'
    __turnouts_p1_jdict = None


    @classmethod
    def setUpClass(cls):
        with open(cls.__layout_filename) as fp:
            cls.__layout_jdict = json.load(fp)

        with open(cls.__p0_filename) as fp:
            cls.__turnouts_p0_jdict = json.load(fp)

        with open(cls.__p1_filename) as fp:
            cls.__turnouts_p1_jdict = json.load(fp)


    def __config_p0(self) -> TurnoutConfiguration:
        turnout_statuses = [TurnoutStatus.construct_from_jdict(jdict) for jdict in self.__turnouts_p0_jdict]
        return TurnoutConfiguration.construct_from_turnouts(*turnout_statuses)


    def __config_p1(self) -> TurnoutConfiguration:
        turnout_statuses = [TurnoutStatus.construct_from_jdict(jdict) for jdict in self.__turnouts_p1_jdict]
        return TurnoutConfiguration.construct_from_turnouts(*turnout_statuses)


    @classmethod
    def __sample_platform_1(cls):
        return Platform(PlatformLabel('TST', 1), PlatformAlignment.UP_LEFT, Location('B03', 'S01'), 20, 120)


    @classmethod
    def __sample_platform_2(cls):
        return Platform(PlatformLabel('TST', 2), PlatformAlignment.UP_RIGHT, Location('B04', 'S01'), 30, 140)


    def __navigator(self) -> LayoutNavigator:
        blocks = OrderedDict()
        for block_jdict in self.__layout_jdict.get('blocks', []):
            block = Block.construct_from_jdict(block_jdict)
            blocks[block.label] = block

        platforms = OrderedDict()
        for platform_jdict in self.__layout_jdict.get('platforms', []):
            platform = Platform.construct_from_jdict(platform_jdict)
            platforms[platform.label] = platform

        return _DummyLayoutNavigator(blocks, platforms)


    # Properties & Accessors -----------------------------------------------------------------------------------------

    def test_navigator_blocks(self):
        navigator = self.__navigator()

        self.assertEqual(4, len(navigator.blocks))
        self.assertEqual(('B01', 'B02', 'B03', 'B04'), tuple(b.label for b in navigator.blocks))


    def test_navigator_block(self):
        navigator = self.__navigator()

        b01 = navigator.block('B01')
        self.assertIsNotNone(b01)
        assert b01 is not None
        self.assertEqual('B01', b01.label)

        b02 = navigator.block('B02')
        self.assertIsNotNone(b02)
        assert b02 is not None
        self.assertEqual('B02', b02.label)

        self.assertIsNone(navigator.block('B99'))


    def test_navigator_platforms(self):
        navigator = self.__navigator()

        self.assertEqual(2, len(navigator.platforms))
        self.assertEqual((PlatformLabel('TST', 1), PlatformLabel('TST', 2)),
                         tuple(p.label for p in navigator.platforms))
        self.assertEqual((self.__sample_platform_1(), self.__sample_platform_2()), navigator.platforms)


    def test_navigator_platform(self):
        navigator = self.__navigator()

        p1 = navigator.platform(PlatformLabel('TST', 1))
        self.assertIsNotNone(p1)
        assert p1 is not None
        self.assertEqual(self.__sample_platform_1(), p1)
        self.assertEqual(PlatformAlignment.UP_LEFT, p1.alignment)
        self.assertEqual(Location('B03', 'S01'), p1.origin)

        p2 = navigator.platform(PlatformLabel('TST', 2))
        self.assertIsNotNone(p2)
        assert p2 is not None
        self.assertEqual(self.__sample_platform_2(), p2)

        # an equal-but-distinct label finds the same platform, so PlatformLabel must hash by value
        self.assertEqual(p1, navigator.platform(PlatformLabel('TST', 1)))

        self.assertIsNone(navigator.platform(PlatformLabel('TST', 9)))
        self.assertIsNone(navigator.platform(PlatformLabel('XXX', 1)))


    def test_navigator_locations(self):
        navigator = self.__navigator()
        locations = navigator.locations

        expected = {
            Location('B01', 'S01'),
            Location('B02', 'S01'),
            Location('B02', 'S02'),
            Location('B03', 'S01'),
            Location('B04', 'S01')
        }
        self.assertEqual(expected, set(locations))
        self.assertEqual(5, len(locations))


    # Validation -----------------------------------------------------------------------------------------------------

    def test_navigator_validate_valid(self):
        navigator = self.__navigator()
        navigator.validate()


    def test_navigator_validate_duplicate_block_label(self):
        block1 = Block('B01', '1/1', BlockOperation.REVERSIBLE, OrderedDict())
        block2 = Block('B01', '1/2', BlockOperation.REVERSIBLE, OrderedDict())

        navigator = _DummyLayoutNavigator(OrderedDict({'b1': block1, 'b2': block2}), OrderedDict())
        with self.assertRaises(ValueError) as ctx:
            navigator.validate()

        self.assertEqual('Duplicate block label B01.', str(ctx.exception))


    def test_navigator_validate_duplicate_block_address(self):
        block1 = Block('B01', '1/1', BlockOperation.REVERSIBLE, OrderedDict())
        block2 = Block('B02', '1/1', BlockOperation.REVERSIBLE, OrderedDict())

        navigator = _DummyLayoutNavigator(OrderedDict({'b1': block1, 'b2': block2}), OrderedDict())
        with self.assertRaises(ValueError) as ctx:
            navigator.validate()

        self.assertEqual('Duplicate block address 1/1 in B02.', str(ctx.exception))


    def test_navigator_validate_duplicate_turnout_label(self):
        seg1 = TurnoutSegment('S01', None, None, 50, 70, 'TE01')
        seg2 = TurnoutSegment('S02', None, None, 50, 70, 'TE01')
        block = Block('B01', '1/1', BlockOperation.REVERSIBLE, OrderedDict({'s1': seg1, 's2': seg2}))

        navigator = _DummyLayoutNavigator(OrderedDict({'b1': block}), OrderedDict())
        with self.assertRaises(ValueError) as ctx:
            navigator.validate()

        self.assertEqual('Duplicate turnout label TE01 in B01.', str(ctx.exception))


    def test_navigator_validate_duplicate_segment_label(self):
        seg1 = TrackSegment('S01', None, None, 100)
        seg2 = TrackSegment('S01', None, None, 100)
        block = Block('B01', '1/1', BlockOperation.REVERSIBLE, OrderedDict({'s1': seg1, 's2': seg2}))

        navigator = _DummyLayoutNavigator(OrderedDict({'B01': block}), OrderedDict())
        with self.assertRaises(ValueError) as ctx:
            navigator.validate()

        self.assertEqual('Duplicate segment label S01 in block B01.', str(ctx.exception))


    def test_navigator_validate_invalid_next_location(self):
        seg = TrackSegment('S01', FixedSegmentLink(Location('B99', 'S01')), None, 100)
        block = Block('B01', '1/1', BlockOperation.REVERSIBLE, OrderedDict({'S01': seg}))

        navigator = _DummyLayoutNavigator(OrderedDict({'B01': block}), OrderedDict())
        with self.assertRaises(ValueError) as ctx:
            navigator.validate()

        self.assertEqual('Segment S01 in block B01 has an invalid next_location: '
                         'Location:{block_label:B99, segment_label:S01}.', str(ctx.exception))


    def test_navigator_validate_segment_pointing_to_itself(self):
        seg = TrackSegment('S01', FixedSegmentLink(Location('B01', 'S01')), None, 100)
        block = Block('B01', '1/1', BlockOperation.REVERSIBLE, OrderedDict({'S01': seg}))

        navigator = _DummyLayoutNavigator(OrderedDict({'B01': block}), OrderedDict())
        with self.assertRaises(ValueError) as ctx:
            navigator.validate()

        self.assertEqual('Segment S01 in block B01 is pointing to itself.', str(ctx.exception))


    def test_navigator_validate_missing_reciprocal_link(self):
        seg1 = TrackSegment('S01', FixedSegmentLink(Location('B02', 'S01')), None, 100)
        seg2 = TrackSegment('S01', None, None, 100)

        block1 = Block('B01', '1/1', BlockOperation.REVERSIBLE, OrderedDict({'S01': seg1}))
        block2 = Block('B02', '1/2', BlockOperation.REVERSIBLE, OrderedDict({'S01': seg2}))

        navigator = _DummyLayoutNavigator(OrderedDict({'B01': block1, 'B02': block2}), OrderedDict())
        with self.assertRaises(ValueError) as ctx:
            navigator.validate()

        self.assertEqual('No reciprocal link for segment label S01 in block B01.', str(ctx.exception))


    # Path calculation -----------------------------------------------------------------------------------------------

    def test_navigator_path_up_turnout_p0(self):
        navigator = self.__navigator()
        config = self.__config_p0()

        path = navigator.path(config, BlockHeading.UP, Location('B01', 'S01'), Location('B03', 'S01'))

        expected_edges = [
            PathEdge('TrackSegment', 100, Location('B01', 'S01')),
            PathEdge('TrackSegment', 100, Location('B02', 'S01')),
            PathEdge('TurnoutSegment', 50, Location('B02', 'S02')),
            PathEdge('TrackSegment', 150, Location('B03', 'S01'))
        ]
        self.assertEqual(expected_edges, path.edges)
        self.assertEqual(400, path.total_length)


    def test_navigator_path_up_turnout_p1(self):
        navigator = self.__navigator()
        config = self.__config_p1()

        path = navigator.path(config, BlockHeading.UP, Location('B01', 'S01'), Location('B04', 'S01'))

        expected_edges = [
            PathEdge('TrackSegment', 100, Location('B01', 'S01')),
            PathEdge('TrackSegment', 100, Location('B02', 'S01')),
            PathEdge('TurnoutSegment', 70, Location('B02', 'S02')),
            PathEdge('TrackSegment', 200, Location('B04', 'S01'))
        ]
        self.assertEqual(expected_edges, path.edges)
        self.assertEqual(470, path.total_length)


    def test_navigator_path_down_from_p0(self):
        navigator = self.__navigator()
        config = self.__config_p0()

        path = navigator.path(config, BlockHeading.DOWN, Location('B03', 'S01'), Location('B01', 'S01'))

        expected_edges = [
            PathEdge('TrackSegment', 150, Location('B03', 'S01')),
            PathEdge('TurnoutSegment', 50, Location('B02', 'S02')),
            PathEdge('TrackSegment', 100, Location('B02', 'S01')),
            PathEdge('TrackSegment', 100, Location('B01', 'S01'))
        ]
        self.assertEqual(expected_edges, path.edges)
        self.assertEqual(400, path.total_length)


    def test_navigator_path_down_from_p1(self):
        navigator = self.__navigator()
        config = self.__config_p1()

        path = navigator.path(config, BlockHeading.DOWN, Location('B04', 'S01'), Location('B01', 'S01'))

        expected_edges = [
            PathEdge('TrackSegment', 200, Location('B04', 'S01')),
            PathEdge('TurnoutSegment', 70, Location('B02', 'S02')),
            PathEdge('TrackSegment', 100, Location('B02', 'S01')),
            PathEdge('TrackSegment', 100, Location('B01', 'S01'))
        ]
        self.assertEqual(expected_edges, path.edges)
        self.assertEqual(470, path.total_length)


    def test_navigator_path_single_segment(self):
        navigator = self.__navigator()
        config = self.__config_p0()

        path = navigator.path(config, BlockHeading.UP, Location('B01', 'S01'), Location('B01', 'S01'))

        expected_edges = [
            PathEdge('TrackSegment', 100, Location('B01', 'S01'))
        ]
        self.assertEqual(expected_edges, path.edges)
        self.assertEqual(100, path.total_length)


    def test_navigator_path_start_not_found(self):
        navigator = self.__navigator()
        config = self.__config_p0()

        with self.assertRaises(ValueError) as ctx:
            navigator.path(config, BlockHeading.UP, Location('B99', 'S01'), Location('B01', 'S01'))

        self.assertEqual('Start location not found:B99/S01.', str(ctx.exception))


    def test_navigator_path_end_not_reachable(self):
        navigator = self.__navigator()
        config = self.__config_p0()

        with self.assertRaises(ValueError) as ctx:
            navigator.path(config, BlockHeading.UP, Location('B01', 'S01'), Location('B04', 'S01'))

        self.assertEqual('End location B04/S01 is not reachable from location B01/S01 with heading UP - '
                         'turnout configuration may be incorrect.', str(ctx.exception))


    def test_navigator_path_malformed_layout_during_traversal(self):
        seg1 = TrackSegment('S01', FixedSegmentLink(Location('B99', 'S01')), None, 100)
        block1 = Block('B01', '1/1', BlockOperation.REVERSIBLE, OrderedDict({'S01': seg1}))
        navigator = _DummyLayoutNavigator(OrderedDict({'B01': block1}), OrderedDict())
        config = self.__config_p0()

        with self.assertRaises(ValueError) as ctx:
            navigator.path(config, BlockHeading.UP, Location('B01', 'S01'), Location('B02', 'S01'))

        self.assertEqual('Malformed layout - segment not found for next location B99/S01.', str(ctx.exception))


# --------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    unittest.main()
