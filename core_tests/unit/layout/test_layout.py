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
from mrcs_core.equipment.block.block_address import BlockAddress
from mrcs_core.layout.block.block import Block
from mrcs_core.layout.block.block_operation import BlockOperation
from mrcs_core.layout.layout import Layout
from mrcs_core.layout.platform.platform import Platform
from mrcs_core.layout.platform.platform_alignment import PlatformAlignment
from mrcs_core.layout.platform.platform_location import PlatformLocation
from mrcs_core.layout.segment.segment_location import SegmentLocation
from mrcs_core.layout.station.station import Station


# --------------------------------------------------------------------------------------------------------------------

class TestLayout(unittest.TestCase):
    __layout_filename = Path(__file__).parent / 'data' / 'test_001_layout.json'
    __layout_jdict = None


    @classmethod
    def setUpClass(cls):
        with open(cls.__layout_filename) as fp:
            cls.__layout_jdict = json.load(fp)


    @classmethod
    def __sample_platform_1(cls):
        return Platform(1, PlatformAlignment.UP_LEFT, SegmentLocation('B03', 'S01'), 20, 120)


    @classmethod
    def __sample_platform_2(cls):
        return Platform(2, PlatformAlignment.UP_RIGHT, SegmentLocation('B04', 'S01'), 30, 140)


    @classmethod
    def __sample_station_1(cls):
        p1 = Platform(1, PlatformAlignment.UP_RIGHT, SegmentLocation('BS01', 'SG01'), 0, 100)
        p2 = Platform(2, PlatformAlignment.UP_RIGHT, SegmentLocation('BN01', 'SG01'), 0, 100)
        return Station('Alpha', OrderedDict({1: p1, 2: p2}))


    # Persistence location -------------------------------------------------------------------------------------------

    def test_layout_persistence_location(self):
        self.assertEqual(('layouts', 'layout.json'), Layout.persistence_location(None))
        self.assertEqual(('layouts', 'test_001_layout.json'), Layout.persistence_location('test_001'))


    # Construction & properties --------------------------------------------------------------------------------------

    def test_layout_construct(self):
        block1 = Block('B01', BlockAddress(1, 1), BlockOperation.REVERSIBLE, OrderedDict())
        blocks = OrderedDict({'B01': block1})
        station1 = self.__sample_station_1()
        stations = OrderedDict({station1.label: station1})

        layout = Layout('TST001', 'Test layout 001', blocks, stations, name='test_001')
        self.assertEqual('test_001', layout.name)
        self.assertEqual('TST001', layout.label)
        self.assertEqual('Test layout 001', layout.description)
        self.assertEqual((block1,), layout.blocks)
        self.assertEqual((station1,), layout.stations)


    def test_layout_construct_from_jdict(self):
        layout = Layout.construct_from_jdict(self.__layout_jdict, name='test_001')

        self.assertEqual('test_001', layout.name)
        self.assertEqual('TST001', layout.label)
        self.assertEqual('Test layout 001', layout.description)
        self.assertEqual(4, len(layout.blocks))
        self.assertEqual(('B01', 'B02', 'B03', 'B04'), tuple(b.label for b in layout.blocks))

        self.assertEqual(1, len(layout.stations))


    def test_layout_construct_from_jdict_none_or_empty(self):
        layout = Layout.construct_from_jdict({})
        self.assertIsNone(layout.name)
        self.assertIsNone(layout.label)
        self.assertIsNone(layout.description)
        self.assertEqual((), layout.blocks)
        self.assertEqual((), layout.stations)


    def test_layout_construct_from_jdict_no_platforms(self):
        jdict = {key: value for key, value in self.__layout_jdict.items() if key != 'stations'}
        layout = Layout.construct_from_jdict(jdict)

        self.assertEqual(4, len(layout.blocks))
        self.assertEqual((), layout.stations)
        self.assertIsNone(layout.platform(PlatformLocation('TST', 1)))


    # Equality & comparison ------------------------------------------------------------------------------------------

    def test_layout_eq(self):
        layout1 = Layout.construct_from_jdict(self.__layout_jdict, name='test_001')
        layout2 = Layout.construct_from_jdict(self.__layout_jdict, name='test_001')
        self.assertEqual(layout1, layout2)

        blocks = OrderedDict({b.label: b for b in layout1.blocks})
        stations = OrderedDict({s.label: s for s in layout1.stations})

        layout_diff_label = Layout('OTHER', layout1.description, blocks, stations)
        self.assertNotEqual(layout1, layout_diff_label)

        layout_diff_desc = Layout(layout1.label, 'Other description', blocks, stations)
        self.assertNotEqual(layout1, layout_diff_desc)

        layout_diff_blocks = Layout(layout1.label, layout1.description,
                                    OrderedDict({'B01': layout1.block('B01')}), stations)
        self.assertNotEqual(layout1, layout_diff_blocks)

        layout_no_platforms = Layout(layout1.label, layout1.description, blocks, OrderedDict())
        self.assertNotEqual(layout1, layout_no_platforms)

        self.assertNotEqual(layout1, None)
        self.assertNotEqual(layout1, 'TST001')


    def test_layout_lt(self):
        layout1 = Layout('TST001', 'Desc', OrderedDict(), OrderedDict())
        layout2 = Layout('TST002', 'Desc', OrderedDict(), OrderedDict())

        self.assertTrue(layout1 < layout2)
        self.assertFalse(layout2 < layout1)
        self.assertFalse(layout1 < layout1)


    # String representation & serialization --------------------------------------------------------------------------

    def test_layout_str(self):
        self.maxDiff = None
        layout = Layout.construct_from_jdict(self.__layout_jdict, name='test_001')

        expected = ('Layout:{name:test_001, label:TST001, description:Test layout 001, blocks:[Block:{label:B01, '
                    'address:BlockAddress:{detector:1, channel:1}, operation:REVERSIBLE, '
                    'segments:[TrackSegment:{label:S01, up_link:FixedSegmentLink:{next_location:'
                    'SegmentLocation:{block_label:B02, segment_label:S01}}, down_link:None, length:100}]}, '
                    'Block:{label:B02, address:BlockAddress:{detector:1, channel:2}, operation:REVERSIBLE, '
                    'segments:[TrackSegment:{label:S01, up_link:FixedSegmentLink:{next_location:SegmentLocation:'
                    '{block_label:B02, segment_label:S02}}, down_link:FixedSegmentLink:{next_location:'
                    'SegmentLocation:{block_label:B01, segment_label:S01}}, length:100}, '
                    'TurnoutSegment:{label:S02, address:1, up_link:SwitchedSegmentLink:{p0_next_location:'
                    'SegmentLocation:{block_label:B03, segment_label:S01}, p1_next_location:SegmentLocation:'
                    '{block_label:B04, segment_label:S01}}, down_link:FixedSegmentLink:{next_location:SegmentLocation:'
                    '{block_label:B02, segment_label:S01}}, p0_length:50, p1_length:70}]}, Block:{label:B03, '
                    'address:BlockAddress:{detector:1, channel:3}, operation:REVERSIBLE, segments:[TrackSegment:'
                    '{label:S01, up_link:None, down_link:FixedSegmentLink:{next_location:SegmentLocation:'
                    '{block_label:B02, segment_label:S02}}, length:150}]}, Block:{label:B04, address:'
                    'BlockAddress:{detector:1, channel:4}, operation:REVERSIBLE, segments:[TrackSegment:'
                    '{label:S01, up_link:None, down_link:FixedSegmentLink:{next_location:SegmentLocation:'
                    '{block_label:B02, segment_label:S02}}, length:200}]}], stations:[Station:{label:Alpha, '
                    'platforms:[Platform:{label:1, alignment:UP_LEFT, origin:SegmentLocation:{block_label:B03, '
                    'segment_label:S01}, offset:20, length:120}, Platform:{label:2, alignment:UP_RIGHT, '
                    'origin:SegmentLocation:{block_label:B04, segment_label:S01}, offset:30, length:140}]}]}')
        self.assertEqual(expected, str(layout))


    def test_layout_as_json(self):
        layout = Layout.construct_from_jdict(self.__layout_jdict)
        jdict = layout.as_json()

        self.assertEqual('TST001', jdict['label'])
        self.assertEqual('Test layout 001', jdict['description'])
        self.assertEqual(layout.blocks, jdict['blocks'])
        self.assertEqual(layout.stations, jdict['stations'])


    def test_layout_jstr(self):
        layout = Layout.construct_from_jdict(self.__layout_jdict)
        jstr = JSONify.dumps(layout)
        layout_deserialized = Layout.construct_from_jdict(json.loads(jstr))

        self.assertEqual(layout, layout_deserialized)
        self.assertEqual(layout.stations, layout_deserialized.stations)


# --------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    unittest.main()
