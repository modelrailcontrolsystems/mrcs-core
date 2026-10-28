"""
Created on 25 Oct 2026

@author: Bruno Beloff (bbeloff@me.com)

The summary record of a single run along a track block

{
    "start": "2026-10-25T08:55:38.234+00:00",
    "distance": 500,
    "set": 5,
    "ars": 12.1,
    "elapsed": 17.123
}
"""

from collections import OrderedDict
from typing import Any, Self

from mrcs_core.data.iso_datetime import ISODatetime
from mrcs_core.data.json import JSONable
from mrcs_core.equipment.block.block_enums import BlockHeading
from mrcs_core.operations.speed.speed_log import SpeedLog


# --------------------------------------------------------------------------------------------------------------------

class SpeedRun(JSONable):
    """
    The summary record of a single run along a track block
    """


    @classmethod
    def construct(cls, distance: int, direction: BlockHeading, set_speed: int, log: SpeedLog) -> Self:
        test_time = ISODatetime.now()

        return cls(distance, direction, set_speed, log.average_reported_speed, log.elapsed_time, test_time)


    @classmethod
    def construct_from_jdict(cls, jdict) -> Self:
        distance = int(jdict.get('distance'))
        direction = BlockHeading[jdict.get('direction')]
        set_speed = int(jdict.get('set'))
        average_reported_speed = float(jdict.get('ars'))
        elapsed_time = jdict.get('elapsed')
        test_time = ISODatetime.construct_from_jdict(jdict.get('test_time'))

        return cls(distance, direction, set_speed, average_reported_speed, elapsed_time, test_time)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, distance: int, direction: BlockHeading, set_speed: int, average_reported_speed: float,
                 elapsed_time: float, test_time: ISODatetime):
        self.__distance = distance  # mm
        self.__direction = direction
        self.__set_speed = set_speed  # MPU configuration speed units
        self.__average_reported_speed = average_reported_speed  # MPU decoder speed units
        self.__elapsed_time = elapsed_time  # seconds
        self.__test_time = test_time  # ISO datetime


    def __eq__(self, other: Any):
        try:
            return (
                    self.distance == other.distance and self.direction == other.direction and
                    self.set_speed == other.set_speed and
                    self.average_reported_speed == other.average_reported_speed and
                    self.elapsed_time == other.elapsed_time and self.test_time == other.test_time)
        except (AttributeError, TypeError):
            return False


    def __lt__(self, other: Any):
        if self.set_speed < other.set_speed:
            return True

        if self.set_speed > other.set_speed:
            return False

        return self.test_time < other.test_time


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        jdict = OrderedDict()

        jdict['distance'] = self.distance
        jdict['direction'] = self.direction.name
        jdict['set'] = self.set_speed
        jdict['ars'] = self.average_reported_speed
        jdict['elapsed'] = self.elapsed_time
        jdict['test_time'] = self.test_time

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def actual_speed(self) -> float:
        return round((self.distance / 1000) / self.elapsed_time, 3)  # metres per second


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def distance(self):
        return self.__distance


    @property
    def direction(self):
        return self.__direction


    @property
    def set_speed(self):
        return self.__set_speed


    @property
    def average_reported_speed(self):
        return round(self.__average_reported_speed, 1)


    @property
    def elapsed_time(self):
        return round(self.__elapsed_time, 3)


    @property
    def test_time(self):
        return self.__test_time


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return (f'SpeedRun:{{distance:{self.distance}, direction:{self.direction}, set_speed:{self.set_speed}, '
                f'average_reported_speed:{self.average_reported_speed}, elapsed_time:{self.elapsed_time}, '
                f'test_time:{self.test_time}}}')
