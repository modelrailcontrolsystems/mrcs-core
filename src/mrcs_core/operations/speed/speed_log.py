"""
Created on 25 Oct 2026

@author: Bruno Beloff (bbeloff@me.com)

The recording of a single run along a track block

The SpeedLog start() method should be used to record the starting timestamp when the MPU enters the block.
Any reported change in speed that takes place during the run should be recorded with mark(reported_speed).
When the MPU reaches the start of the subsequent block, a final mark(reported_speed) call should be made.
"""

import time
from typing import Any, Self


# --------------------------------------------------------------------------------------------------------------------

class SpeedReport(object):
    """
    The record of a single run along a track block
    """


    @classmethod
    def construct(cls, reported_speed: int) -> Self:
        return cls(time.time(), reported_speed)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, timestamp: float, reported_speed: int):
        self.__timestamp = timestamp  # timestamp
        self.__reported_speed = reported_speed  # MPU speed units


    def __eq__(self, other: Any):
        try:
            return self.timestamp == other.timestamp and self.reported_speed == other.reported_speed
        except (AttributeError, TypeError):
            return False


    def __lt__(self, other: Any):
        return self.timestamp < other.time_offset


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def timestamp(self):
        return round(self.__timestamp, 3)


    @property
    def reported_speed(self):
        return self.__reported_speed


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return f'SpeedReport:{{timestamp:{self.timestamp}, reported_speed:{self.reported_speed}}}'


# --------------------------------------------------------------------------------------------------------------------

class SpeedLog(object):
    """
    The record of a single run along a track block
    """


    @classmethod
    def start(cls) -> Self:
        return cls(SpeedReport.construct(0))  # the first speeed is never used


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, *reports: SpeedReport):
        self.__reports = list(reports)


    def __len__(self):
        return len(self.reports)


    def __eq__(self, other: Any):
        try:
            return self.reports == other.reports
        except (AttributeError, TypeError):
            return False


    # ----------------------------------------------------------------------------------------------------------------

    def mark(self, reported_speed: int) -> None:
        self.reports.append(SpeedReport.construct(reported_speed))


    @property
    def average_reported_speed(self) -> float:
        if len(self) < 2:
            raise ValueError('insufficient data to calculate average reported speed')

        total_elapsed_time = self.elapsed_time
        average_speed = 0

        for i in range(1, len(self.reports), 1):
            elapsed_time = self.reports[i].timestamp - self.reports[i - 1].timestamp
            proportion = elapsed_time / total_elapsed_time
            weighted_speed = self.reports[i].reported_speed * proportion
            average_speed += weighted_speed

        return round(average_speed, 1)


    @property
    def elapsed_time(self) -> float:
        return round(self.reports[-1].timestamp - self.reports[0].timestamp, 3)


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def reports(self):
        return self.__reports


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        reports = '[' + ', '.join(map(str, self.reports)) + ']'
        return f'SpeedLog:{{reports:{reports}}}'
