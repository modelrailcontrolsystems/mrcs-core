"""
Created on 26 Dec 2025

@author: Bruno Beloff (bbeloff@me.com)

A model clock, with start datetime, offset and speed

{
    "speed": 4,
    "offset": 3029029272.269169,
    "start": "2025-12-26T11:01:12.269+00:00"
}
"""

from collections import OrderedDict
from datetime import timedelta

from mrcs_core.data.iso_datetime import ISODatetime
from mrcs_core.data.json import PersistentJSONable


# --------------------------------------------------------------------------------------------------------------------

class Clock(PersistentJSONable):
    """
    classdocs
    """

    START_OF_TIME = 1804        # Pen-y-Darren built by Richard Trevithick

    # ----------------------------------------------------------------------------------------------------------------

    __FILENAME = "clock_conf.json"

    @classmethod
    def persistence_location(cls):
        return cls.conf_dir(), cls.__FILENAME


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict, skeleton=None):
        if not jdict:
            return cls(1, timedelta(), ISODatetime.now())

        speed = int(jdict.get('speed'))
        offset = timedelta(seconds=jdict.get('offset'))
        start = ISODatetime.construct_from_jdict(jdict.get('start'))

        return cls(speed, offset, start)


    @classmethod
    def set(cls, speed: int, year, month, day, hour, minute=0, second=0):
        now = ISODatetime.now()
        model_now = ISODatetime(year, month=month, day=day, hour=hour, minute=minute, second=second)
        offset = now - model_now

        return cls(speed, offset, now)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, speed: int, offset: timedelta, start: ISODatetime):
        super().__init__()

        self.__speed = speed
        self.__offset = offset
        self.__start = start


    def __eq__(self, other):
        try:
            return self.speed == other.speed and self.offset == other.offset and self.start == other.start
        except (AttributeError, TypeError):
            return False


    # ----------------------------------------------------------------------------------------------------------------

    def now(self):
        now = ISODatetime.now()
        true_period = now - self.start
        running_period = true_period * self.speed

        return self.start + running_period - self.offset


    def restart(self):
        now = ISODatetime.now()
        true_period = now - self.start

        self.__offset += true_period
        self.__start = now


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        jdict = OrderedDict()

        jdict['speed'] = self.speed
        jdict['offset'] = self.offset.total_seconds()
        jdict['start'] = self.start

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def speed(self):
        return self.__speed


    @property
    def offset(self):
        return self.__offset


    @property
    def start(self):
        return self.__start


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return f'Clock{{speed:{self.speed}, offset:{self.offset}, start:{self.start}}}'
