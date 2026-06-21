"""
Created on 11 Jun 2026

@author: Bruno Beloff (bbeloff@me.com)

python -m unittest -v dcc/z21/entities/test_control_router.py

https://realpython.com/python-testing/
https://www.jetbrains.com/help/pycharm/creating-tests.html
"""

import json
import unittest

from mrcs_core.data.json import JSONify
from mrcs_core.equipment.track.track_mode import TrackMode
from mrcs_core.equipment.track.track_state import TrackState


# --------------------------------------------------------------------------------------------------------------------

class TestTrackState(unittest.TestCase):

    def test_track(self):
        mode = TrackMode.POWER_ON
        obj1 = TrackState(mode)
        self.assertEqual(mode, obj1.mode)


    def test_track_str(self):
        mode = TrackMode.POWER_ON
        obj1 = TrackState(mode)
        self.assertEqual('TrackState:{mode:POWER_ON}', str(obj1))


    def test_turnout_is_valid(self):
        mode = TrackMode.UNKNOWN
        obj1 = TrackState(mode)
        self.assertEqual(True, obj1.is_unknown)


    def test_turnout_jstr(self):
        mode = TrackMode.SHORT_CIRCUIT
        obj1 = TrackState(mode)
        jstr = JSONify.dumps(obj1)
        self.assertEqual('{"type": "TrackState", "mode": "SHORT_CIRCUIT"}', jstr)


    def test_turnout_jstr_eq(self):
        mode = TrackMode.POWER_OFF
        obj1 = TrackState(mode)
        jstr = JSONify.dumps(obj1)
        obj2 = TrackState.construct_from_jdict(json.loads(jstr))
        self.assertEqual(obj1, obj2)
