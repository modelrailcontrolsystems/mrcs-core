"""
Created on 14 Sep 2026

@author: Bruno Beloff (bbeloff@me.com)

python -m unittest -v unit/inventory/layout/test_path.py

https://realpython.com/python-testing/
https://www.jetbrains.com/help/pycharm/creating-tests.html
"""

import json
import unittest

from mrcs_core.data.json import JSONify
from mrcs_core.equipment.turnout.turnout_configuration import TurnoutConfiguration
from mrcs_core.inventory.layout.location import Location
from mrcs_core.inventory.layout.path import Path, PathEdge
from mrcs_core.inventory.segment.segment import TrackSegment
from mrcs_core.inventory.segment.segment_link import FixedSegmentLink


# --------------------------------------------------------------------------------------------------------------------

class TestPath(unittest.TestCase):

    @classmethod
    def __sample_track_segment_1(cls):
        label = 'S01'
        up_link = FixedSegmentLink(Location('BN01', 'S02'))
        down_link = None
        length = 60
        return TrackSegment(label, up_link, down_link, length)


    @classmethod
    def __sample_track_segment_2(cls):
        label = 'S02'
        up_link = FixedSegmentLink(Location('BN01', 'S03'))
        down_link = None
        length = 80
        return TrackSegment(label, up_link, down_link, length)


    @classmethod
    def __sample_turnout_configuration(cls):
        return TurnoutConfiguration({})


    @classmethod
    def __sample_path_edge_1(cls):
        return PathEdge('TrackSegment', 60, Location('BN01', 'S01'))


    @classmethod
    def __sample_path_edge_2(cls):
        return PathEdge('TrackSegment', 80, Location('BN01', 'S02'))


    @classmethod
    def __sample_path_edge_3(cls):
        return PathEdge('TrackSegment', 100, Location('BN02', 'S01'))


    # ----------------------------------------------------------------------------------------------------------------

    def test_path_edge_construct(self):
        obj1 = self.__sample_path_edge_1()
        self.assertEqual('TrackSegment', obj1.segment_type_name)
        self.assertEqual(60, obj1.length)
        self.assertEqual(Location('BN01', 'S01'), obj1.location)


    def test_path_edge_construct_from_segment(self):
        segment = self.__sample_track_segment_1()
        obj1 = PathEdge.construct(self.__sample_turnout_configuration(), 'BN01', segment)

        self.assertEqual('TrackSegment', obj1.segment_type_name)
        self.assertEqual(60, obj1.length)
        self.assertEqual(Location('BN01', 'S01'), obj1.location)


    def test_path_edge_construct_from_jdict(self):
        jdict = {
            'type': 'TrackSegment',
            'length': 60,
            'location': 'BN01/S01'
        }
        obj1 = PathEdge.construct_from_jdict(jdict)

        self.assertEqual('TrackSegment', obj1.segment_type_name)
        self.assertEqual(60, obj1.length)
        self.assertEqual(Location('BN01', 'S01'), obj1.location)


    def test_path_edge_str(self):
        obj1 = self.__sample_path_edge_1()
        self.assertEqual('PathEdge:{segment_type_name:TrackSegment, length:60, '
                         'location:Location:{block_label:BN01, segment_label:S01}}', str(obj1))


    def test_path_edge_as_json(self):
        obj1 = self.__sample_path_edge_1()
        jdict = obj1.as_json()

        self.assertEqual('TrackSegment', jdict['type'])
        self.assertEqual(60, jdict['length'])
        self.assertEqual(Location('BN01', 'S01'), jdict['location'])


    def test_path_edge_jstr(self):
        obj1 = self.__sample_path_edge_1()
        jstr = JSONify.dumps(obj1)
        self.assertEqual('{"type": "TrackSegment", "length": 60, "location": "BN01/S01"}', jstr)


    def test_path_edge_jstr_eq(self):
        obj1 = self.__sample_path_edge_1()
        jstr = JSONify.dumps(obj1)
        obj2 = PathEdge.construct_from_jdict(json.loads(jstr))
        self.assertEqual(obj1, obj2)


    def test_path_edge_eq(self):
        obj1 = self.__sample_path_edge_1()
        obj2 = self.__sample_path_edge_1()
        self.assertEqual(obj1, obj2)


    def test_path_edge_neq(self):
        obj1 = self.__sample_path_edge_1()
        obj2 = self.__sample_path_edge_2()
        obj3 = self.__sample_path_edge_3()

        self.assertNotEqual(obj1, obj2)
        self.assertNotEqual(obj1, obj3)
        self.assertNotEqual(obj1, None)
        self.assertNotEqual(obj1, 'BN01:S01')


    # ----------------------------------------------------------------------------------------------------------------

    def test_path_construct_empty(self):
        obj = Path()
        self.assertEqual([], obj.edges)
        self.assertEqual(0, obj.total_length)


    def test_path_construct_with_edges(self):
        edge1 = self.__sample_path_edge_1()
        edge2 = self.__sample_path_edge_2()
        obj = Path(edge1, edge2)

        self.assertEqual([edge1, edge2], obj.edges)
        self.assertEqual(140, obj.total_length)


    def test_path_construct_from_jdict(self):
        jdict = [
            {'type': 'TrackSegment', 'length': 60, 'location': 'BN01/S01'},
            {'type': 'TrackSegment', 'length': 80, 'location': 'BN01/S02'}
        ]
        obj = Path.construct_from_jdict(jdict)

        self.assertEqual([self.__sample_path_edge_1(), self.__sample_path_edge_2()], obj.edges)
        self.assertEqual(140, obj.total_length)


    def test_path_append(self):
        obj = Path()
        conf = self.__sample_turnout_configuration()
        segment1 = self.__sample_track_segment_1()
        segment2 = self.__sample_track_segment_2()

        obj.append(conf, 'BN01', segment1)
        self.assertEqual([self.__sample_path_edge_1()], obj.edges)
        self.assertEqual(60, obj.total_length)

        obj.append(conf, 'BN01', segment2)
        self.assertEqual([self.__sample_path_edge_1(), self.__sample_path_edge_2()], obj.edges)
        self.assertEqual(140, obj.total_length)


    def test_path_str(self):
        self.maxDiff = None
        obj_empty = Path()
        self.assertEqual('Path:{edges:[]}', str(obj_empty))

        edge1 = self.__sample_path_edge_1()
        edge2 = self.__sample_path_edge_2()
        obj = Path(edge1, edge2)
        self.assertEqual('Path:{edges:[PathEdge:{segment_type_name:TrackSegment, length:60, '
                         'location:Location:{block_label:BN01, segment_label:S01}}, '
                         'PathEdge:{segment_type_name:TrackSegment, length:80, '
                         'location:Location:{block_label:BN01, segment_label:S02}}]}', str(obj))


    def test_path_as_json(self):
        edge1 = self.__sample_path_edge_1()
        edge2 = self.__sample_path_edge_2()
        obj = Path(edge1, edge2)

        self.assertEqual([edge1, edge2], obj.as_json())


    def test_path_jstr(self):
        edge1 = self.__sample_path_edge_1()
        edge2 = self.__sample_path_edge_2()
        obj = Path(edge1, edge2)
        jstr = JSONify.dumps(obj)
        self.assertEqual('[{"type": "TrackSegment", "length": 60, "location": "BN01/S01"}, '
                         '{"type": "TrackSegment", "length": 80, "location": "BN01/S02"}]', jstr)


    def test_path_jstr_eq(self):
        edge1 = self.__sample_path_edge_1()
        edge2 = self.__sample_path_edge_2()
        obj1 = Path(edge1, edge2)
        jstr = JSONify.dumps(obj1)
        obj2 = Path.construct_from_jdict(json.loads(jstr))
        self.assertEqual(obj1, obj2)


    def test_path_eq(self):
        edge1 = self.__sample_path_edge_1()
        edge2 = self.__sample_path_edge_2()
        obj1 = Path(edge1, edge2)
        obj2 = Path(edge1, edge2)
        self.assertEqual(obj1, obj2)


    def test_path_neq(self):
        edge1 = self.__sample_path_edge_1()
        edge2 = self.__sample_path_edge_2()
        edge3 = self.__sample_path_edge_3()

        obj1 = Path(edge1, edge2)
        obj2 = Path(edge1, edge3)
        obj3 = Path(edge1)

        self.assertNotEqual(obj1, obj2)
        self.assertNotEqual(obj1, obj3)
        self.assertNotEqual(obj1, None)
        self.assertNotEqual(obj1, [edge1, edge2])


# --------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    unittest.main()
