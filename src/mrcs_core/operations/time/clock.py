"""
Created on 26 Dec 2025

@author: Bruno Beloff (bbeloff@me.com)

A model clock, with true_start datetime, model_start and speed

Note that the clock odes not persist its is_running status - when loaded, it is in the stopped state.

{
    "is_running": false,
    "speed": 4,
    "model_start": "2020-02-04T06:00:00.000+00:00",
    "true_start": "2026-01-01T09:12:08.216+00:00"
}
"""

from collections import OrderedDict

from mrcs_core.data.iso_datetime import ISODatetime
from mrcs_core.data.json import PersistentJSONable


# --------------------------------------------------------------------------------------------------------------------

class Clock(PersistentJSONable):
    """
    classdocs
    """

    START_OF_TIME_YEAR = 1804        # Pen-y-Darren is built by Richard Trevithick

    # ----------------------------------------------------------------------------------------------------------------

    __FILENAME = "clock_conf.json"

    @classmethod
    def persistence_location(cls):
        return cls.conf_dir(), cls.__FILENAME


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict, skeleton=None):
        if not jdict:
            if skeleton:
                now = ISODatetime.now()
                return cls(False, 1, now, now)
            else:
                return None

        speed = int(jdict.get('speed'))
        model_start = ISODatetime.construct_from_jdict(jdict.get('model_start'))
        true_start = ISODatetime.construct_from_jdict(jdict.get('true_start'))

        return cls(False, speed, model_start, true_start)


    @classmethod
    def set(cls, is_running: bool, speed: int, year, month, day, hour, minute=0, second=0):
        model_start = ISODatetime(year, month=month, day=day, hour=hour, minute=minute, second=second)
        true_start = ISODatetime.now() if is_running else None

        return cls(is_running, speed, model_start, true_start)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, is_running: bool, speed: int, model_start: ISODatetime, true_start: ISODatetime | None):
        super().__init__()

        self.__is_running = is_running
        self.__speed = speed
        self.__model_start = model_start
        self.__true_start = true_start


    def __eq__(self, other):
        try:
            return (self.is_running == other.is_running and self.speed == other.speed and
                    self.model_start == other.model_start and self.true_start == other.true_start)
        except (AttributeError, TypeError):
            return False


    # ----------------------------------------------------------------------------------------------------------------

    def now(self):
        if not self.is_running:
            return self.model_start

        true_period = ISODatetime.now() - self.true_start
        model_period = true_period * self.speed

        return self.model_start + model_period


    def start(self):
        self.__true_start = ISODatetime.now()
        self.__is_running = True


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        jdict = OrderedDict()

        jdict['speed'] = self.speed
        jdict['model_start'] = self.model_start
        jdict['true_start'] = self.true_start

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def is_running(self):
        return self.__is_running


    @property
    def speed(self):
        return self.__speed


    @property
    def model_start(self):
        return self.__model_start


    @property
    def true_start(self):
        return self.__true_start


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return (f'Clock{{is_running:{self.is_running}, speed:{self.speed}, model_start:{self.model_start}, '
                f'true_start:{self.true_start}}}')
