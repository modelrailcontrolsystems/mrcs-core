"""
Created on 12 Sep 2026

@author: Bruno Beloff (bbeloff@me.com)

python -m unittest -v unit/inventory/layout/test_layout.py

https://realpython.com/python-testing/
https://www.jetbrains.com/help/pycharm/creating-tests.html
"""

import json
import unittest
from collections import OrderedDict
from pathlib import Path

from mrcs_core.data.json import JSONify
from mrcs_core.equipment.block.block_enums import BlockHeading
from mrcs_core.equipment.turnout.turnout_configuration import TurnoutConfiguration
from mrcs_core.equipment.turnout.turnout_status import TurnoutStatus
from mrcs_core.inventory.block.block import Block
from mrcs_core.inventory.block.block_operation import BlockOperation
from mrcs_core.inventory.layout.layout import Layout
from mrcs_core.inventory.layout.location import Location
from mrcs_core.inventory.layout.path import PathEdge
from mrcs_core.inventory.segment.segment import TrackSegment, TurnoutSegment
from mrcs_core.inventory.segment.segment_link import FixedSegmentLink


# --------------------------------------------------------------------------------------------------------------------

class TestLayout(unittest.TestCase):
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


    # Persistence location -------------------------------------------------------------------------------------------

    def test_layout_persistence_location(self):
        self.assertEqual(('layouts', 'layout.json'), Layout.persistence_location(None))
        self.assertEqual(('layouts', 'test_001_layout.json'), Layout.persistence_location('test_001'))


    # Construction & properties --------------------------------------------------------------------------------------

    def test_layout_construct_from_jdict(self):
        layout = Layout.construct_from_jdict(self.__layout_jdict, name='test_001')

        self.assertEqual('test_001', layout.name)
        self.assertEqual('TST001', layout.label)
        self.assertEqual('Test layout 001', layout.description)
        self.assertEqual(4, len(layout.blocks))
        self.assertEqual(('B01', 'B02', 'B03', 'B04'), tuple(b.label for b in layout.blocks))


    def test_layout_construct_from_jdict_none_or_empty(self):
        layout = Layout.construct_from_jdict({})
        self.assertIsNone(layout.name)
        self.assertIsNone(layout.label)
        self.assertIsNone(layout.description)
        self.assertEqual((), layout.blocks)


    def test_layout_block(self):
        layout = Layout.construct_from_jdict(self.__layout_jdict)

        b01 = layout.block('B01')
        self.assertIsNotNone(b01)
        self.assertEqual('B01', b01.label)

        b02 = layout.block('B02')
        self.assertIsNotNone(b02)
        self.assertEqual('B02', b02.label)

        self.assertIsNone(layout.block('B99'))


    def test_layout_segment(self):
        layout = Layout.construct_from_jdict(self.__layout_jdict)

        seg1 = layout.segment(Location('B01', 'S01'))
        self.assertIsNotNone(seg1)
        assert seg1 is not None
        self.assertEqual('S01', seg1.label)
        self.assertIsInstance(seg1, TrackSegment)

        seg2 = layout.segment(Location('B02', 'S02'))
        self.assertIsNotNone(seg2)
        assert seg2 is not None
        self.assertEqual('S02', seg2.label)
        self.assertIsInstance(seg2, TurnoutSegment)

        self.assertIsNone(layout.segment(Location('B99', 'S01')))
        self.assertIsNone(layout.segment(Location('B01', 'S99')))


    def test_layout_block_segment(self):
        layout = Layout.construct_from_jdict(self.__layout_jdict)

        res = layout.block_segment(Location('B02', 'S01'))
        self.assertIsNotNone(res)
        assert res is not None
        block_label, segment = res
        assert segment is not None
        self.assertEqual('B02', block_label)
        self.assertEqual('S01', segment.label)

        self.assertEqual(('B01', None), layout.block_segment(Location('B01', 'S99')))
        self.assertIsNone(layout.block_segment(Location('B99', 'S01')))


    def test_layout_locations(self):
        layout = Layout.construct_from_jdict(self.__layout_jdict)
        locations = layout.locations

        expected = {
            Location('B01', 'S01'),
            Location('B02', 'S01'),
            Location('B02', 'S02'),
            Location('B03', 'S01'),
            Location('B04', 'S01')
        }
        self.assertEqual(expected, set(locations))
        self.assertEqual(5, len(locations))


    # Equality & comparison ------------------------------------------------------------------------------------------

    def test_layout_eq(self):
        layout1 = Layout.construct_from_jdict(self.__layout_jdict, name='test_001')
        layout2 = Layout.construct_from_jdict(self.__layout_jdict, name='test_001')
        self.assertEqual(layout1, layout2)

        blocks = OrderedDict({b.label: b for b in layout1.blocks})

        layout_diff_label = Layout('OTHER', layout1.description, blocks)
        self.assertNotEqual(layout1, layout_diff_label)

        layout_diff_desc = Layout(layout1.label, 'Other description', blocks)
        self.assertNotEqual(layout1, layout_diff_desc)

        layout_diff_blocks = Layout(layout1.label, layout1.description, OrderedDict({'B01': layout1.block('B01')}))
        self.assertNotEqual(layout1, layout_diff_blocks)

        self.assertNotEqual(layout1, None)
        self.assertNotEqual(layout1, 'TST001')


    def test_layout_lt(self):
        layout1 = Layout('TST001', 'Desc', OrderedDict())
        layout2 = Layout('TST002', 'Desc', OrderedDict())

        self.assertTrue(layout1 < layout2)
        self.assertFalse(layout2 < layout1)
        self.assertFalse(layout1 < layout1)


    # String representation & serialization --------------------------------------------------------------------------

    def test_layout_str(self):
        self.maxDiff = None
        layout = Layout.construct_from_jdict(self.__layout_jdict, name='test_001')

        expected = (
            'Layout:{name:test_001, label:TST001, description:Test layout 001, blocks:['
            'Block:{label:B01, address:1/1, operation:REVERSIBLE, segments:['
            'TrackSegment:{label:S01, length:100, up_link:FixedSegmentLink:{next_location:Location:{'
            'block_label:B02, segment_label:S01}}, down_link:None}'
            ']}, '
            'Block:{label:B02, address:1/2, operation:REVERSIBLE, segments:['
            'TrackSegment:{label:S01, length:100, up_link:FixedSegmentLink:{next_location:Location:{'
            'block_label:B02, segment_label:S02}}, down_link:FixedSegmentLink:{next_location:Location:{'
            'block_label:B01, segment_label:S01}}}, '
            'TurnoutSegment:{label:S02, length:50, turnout:TE01, up_link:SwitchedSegmentLink:{'
            'p0_next_location:Location:{block_label:B03, segment_label:S01}, '
            'p1_next_location:Location:{block_label:B04, segment_label:S01}}, down_link:FixedSegmentLink:{'
            'next_location:Location:{block_label:B02, segment_label:S01}}}'
            ']}, '
            'Block:{label:B03, address:1/3, operation:REVERSIBLE, segments:['
            'TrackSegment:{label:S01, length:150, up_link:None, down_link:FixedSegmentLink:{'
            'next_location:Location:{block_label:B02, segment_label:S02}}}'
            ']}, '
            'Block:{label:B04, address:1/4, operation:REVERSIBLE, segments:['
            'TrackSegment:{label:S01, length:200, up_link:None, down_link:FixedSegmentLink:{'
            'next_location:Location:{block_label:B02, segment_label:S02}}}'
            ']}'
            ']}'
        )
        self.assertEqual(expected, str(layout))


    def test_layout_as_json(self):
        layout = Layout.construct_from_jdict(self.__layout_jdict)
        jdict = layout.as_json()

        self.assertEqual('TST001', jdict['label'])
        self.assertEqual('Test layout 001', jdict['description'])
        self.assertEqual(layout.blocks, jdict['blocks'])


    def test_layout_jstr(self):
        layout = Layout.construct_from_jdict(self.__layout_jdict)
        jstr = JSONify.dumps(layout)
        layout_deserialized = Layout.construct_from_jdict(json.loads(jstr))
        self.assertEqual(layout, layout_deserialized)


    # Validation -----------------------------------------------------------------------------------------------------

    def test_layout_validate_valid(self):
        layout = Layout.construct_from_jdict(self.__layout_jdict)
        layout.validate()


    def test_layout_validate_duplicate_block_label(self):
        block1 = Block('B01', '1/1', BlockOperation.REVERSIBLE, OrderedDict())
        block2 = Block('B01', '1/2', BlockOperation.REVERSIBLE, OrderedDict())

        layout = Layout('TEST', 'Desc', OrderedDict({'b1': block1, 'b2': block2}))
        with self.assertRaises(ValueError) as ctx:
            layout.validate()

        self.assertEqual('Duplicate block label: B01.', str(ctx.exception))


    def test_layout_validate_duplicate_segment_label(self):
        seg1 = TrackSegment('S01', 100, None, None)
        seg2 = TrackSegment('S01', 100, None, None)
        block = Block('B01', '1/1', BlockOperation.REVERSIBLE, OrderedDict({'s1': seg1, 's2': seg2}))

        layout = Layout('TEST', 'Desc', OrderedDict({'B01': block}))
        with self.assertRaises(ValueError) as ctx:
            layout.validate()

        self.assertEqual('Duplicate segment label: S01 in block B01.', str(ctx.exception))


    def test_layout_validate_invalid_next_location(self):
        seg = TrackSegment('S01', 100, FixedSegmentLink(Location('B99', 'S01')), None)
        block = Block('B01', '1/1', BlockOperation.REVERSIBLE, OrderedDict({'S01': seg}))

        layout = Layout('TEST', 'Desc', OrderedDict({'B01': block}))
        with self.assertRaises(ValueError) as ctx:
            layout.validate()

        self.assertEqual('Segment S01 in block B01 has an invalid next_location: '
                         'Location:{block_label:B99, segment_label:S01}.', str(ctx.exception))


    def test_layout_validate_missing_reciprocal_link(self):
        seg1 = TrackSegment('S01', 100, FixedSegmentLink(Location('B02', 'S01')), None)
        seg2 = TrackSegment('S01', 100, None, None)

        block1 = Block('B01', '1/1', BlockOperation.REVERSIBLE, OrderedDict({'S01': seg1}))
        block2 = Block('B02', '1/2', BlockOperation.REVERSIBLE, OrderedDict({'S01': seg2}))

        layout = Layout('TEST', 'Desc', OrderedDict({'B01': block1, 'B02': block2}))
        with self.assertRaises(ValueError) as ctx:
            layout.validate()

        self.assertEqual('No reciprocal link for segment label S01 in block B01.', str(ctx.exception))


    # Path calculation -----------------------------------------------------------------------------------------------

    def test_layout_path_up_turnout_p0(self):
        layout = Layout.construct_from_jdict(self.__layout_jdict)
        config = self.__config_p0()

        path = layout.path(config, BlockHeading.UP, Location('B01', 'S01'), Location('B03', 'S01'))

        expected_edges = [
            PathEdge('TrackSegment', 100, Location('B01', 'S01')),
            PathEdge('TrackSegment', 100, Location('B02', 'S01')),
            PathEdge('TurnoutSegment', 50, Location('B02', 'S02')),
            PathEdge('TrackSegment', 150, Location('B03', 'S01'))
        ]
        self.assertEqual(expected_edges, path.edges)
        self.assertEqual(400, path.total_length)


    def test_layout_path_up_turnout_p1(self):
        layout = Layout.construct_from_jdict(self.__layout_jdict)
        config = self.__config_p1()

        path = layout.path(config, BlockHeading.UP, Location('B01', 'S01'), Location('B04', 'S01'))

        expected_edges = [
            PathEdge('TrackSegment', 100, Location('B01', 'S01')),
            PathEdge('TrackSegment', 100, Location('B02', 'S01')),
            PathEdge('TurnoutSegment', 50, Location('B02', 'S02')),
            PathEdge('TrackSegment', 200, Location('B04', 'S01'))
        ]
        self.assertEqual(expected_edges, path.edges)
        self.assertEqual(450, path.total_length)


    def test_layout_path_down_from_p0(self):
        layout = Layout.construct_from_jdict(self.__layout_jdict)
        config = self.__config_p0()

        path = layout.path(config, BlockHeading.DOWN, Location('B03', 'S01'), Location('B01', 'S01'))

        expected_edges = [
            PathEdge('TrackSegment', 150, Location('B03', 'S01')),
            PathEdge('TurnoutSegment', 50, Location('B02', 'S02')),
            PathEdge('TrackSegment', 100, Location('B02', 'S01')),
            PathEdge('TrackSegment', 100, Location('B01', 'S01'))
        ]
        self.assertEqual(expected_edges, path.edges)
        self.assertEqual(400, path.total_length)


    def test_layout_path_down_from_p1(self):
        layout = Layout.construct_from_jdict(self.__layout_jdict)
        config = self.__config_p1()

        path = layout.path(config, BlockHeading.DOWN, Location('B04', 'S01'), Location('B01', 'S01'))

        expected_edges = [
            PathEdge('TrackSegment', 200, Location('B04', 'S01')),
            PathEdge('TurnoutSegment', 50, Location('B02', 'S02')),
            PathEdge('TrackSegment', 100, Location('B02', 'S01')),
            PathEdge('TrackSegment', 100, Location('B01', 'S01'))
        ]
        self.assertEqual(expected_edges, path.edges)
        self.assertEqual(450, path.total_length)


    def test_layout_path_single_segment(self):
        layout = Layout.construct_from_jdict(self.__layout_jdict)
        config = self.__config_p0()

        path = layout.path(config, BlockHeading.UP, Location('B01', 'S01'), Location('B01', 'S01'))

        expected_edges = [
            PathEdge('TrackSegment', 100, Location('B01', 'S01'))
        ]
        self.assertEqual(expected_edges, path.edges)
        self.assertEqual(100, path.total_length)


    def test_layout_path_start_not_found(self):
        layout = Layout.construct_from_jdict(self.__layout_jdict)
        config = self.__config_p0()

        with self.assertRaises(ValueError) as ctx:
            layout.path(config, BlockHeading.UP, Location('B99', 'S01'), Location('B01', 'S01'))

        self.assertEqual('Start location not found:B99/S01.', str(ctx.exception))


    def test_layout_path_end_not_reachable(self):
        layout = Layout.construct_from_jdict(self.__layout_jdict)
        config = self.__config_p0()

        with self.assertRaises(ValueError) as ctx:
            layout.path(config, BlockHeading.UP, Location('B01', 'S01'), Location('B04', 'S01'))

        self.assertEqual('End location B04/S01 is not reachable from location B01/S01 with heading UP - '
                         'turnout configuration may be incorrect.', str(ctx.exception))


    def test_layout_path_malformed_layout_during_traversal(self):
        seg1 = TrackSegment('S01', 100, FixedSegmentLink(Location('B99', 'S01')), None)
        block1 = Block('B01', '1/1', BlockOperation.REVERSIBLE, OrderedDict({'S01': seg1}))
        layout = Layout('TEST', 'Desc', OrderedDict({'B01': block1}))
        config = self.__config_p0()

        with self.assertRaises(ValueError) as ctx:
            layout.path(config, BlockHeading.UP, Location('B01', 'S01'), Location('B02', 'S01'))

        self.assertEqual('Malformed layout - segment not found for next location B99/S01.', str(ctx.exception))


# --------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    unittest.main()
