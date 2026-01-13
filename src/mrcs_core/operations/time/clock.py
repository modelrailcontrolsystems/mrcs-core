"""
Created on 26 Dec 2025

@author: Bruno Beloff (bbeloff@me.com)

A model clock
If a configuration is not present, then the model clock follows the system clock.

{
    "is_running": true,
    "speed": 4,
    "model_start": "1930-01-03T06:00:00.000+00:00",
    "true_start": "2026-01-03T12:27:51.002+00:00",
    "true_stop": null
}
"""

from collections import OrderedDict

from mrcs_core.data.json import PersistentJSONable
from mrcs_core.operations.time.clock_iso_datetime import ClockISODatetime
from mrcs_core.sys.host import Host


# TODO: implement conf save with messaging
# --------------------------------------------------------------------------------------------------------------------

class Clock(PersistentJSONable):
    """
    a model clock
    """

    START_OF_TIME_YEAR = 1804        # Pen-y-Darren is built by Richard Trevithick

    # ----------------------------------------------------------------------------------------------------------------

    __FILENAME = "clock_conf.json"

    @classmethod
    def persistence_location(cls):
        return cls.conf_dir(), cls.__FILENAME


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return cls(True, 1, None, None, None)

        is_running = jdict.get('is_running')
        speed = int(jdict.get('speed'))
        model_start = ClockISODatetime.construct_from_jdict(jdict.get('model_start'))
        true_start = ClockISODatetime.construct_from_jdict(jdict.get('true_start'))
        true_stop = ClockISODatetime.construct_from_jdict(jdict.get('true_stop'))

        return cls(is_running, speed, model_start, true_start, true_stop)


    @classmethod
    def set(cls, is_running: bool, speed: int, year, month, day, hour, minute=0, second=0):
        model_start = ClockISODatetime(year, month=month, day=day, hour=hour, minute=minute, second=second)
        true_start = ClockISODatetime.now()
        true_stop = None if is_running else ClockISODatetime.now()

        return cls(is_running, speed, model_start, true_start, true_stop)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, is_running: bool, speed: int, model_start: ClockISODatetime | None,
                 true_start: ClockISODatetime | None, true_stop: ClockISODatetime | None):
        super().__init__()

        self.__is_running = is_running
        self.__speed = speed

        self.__model_start = model_start
        self.__true_start = true_start
        self.__true_stop = true_stop


    def __eq__(self, other):
        try:
            return (self.is_running == other.is_running and self.speed == other.speed and
                    self.model_start == other.model_start and self.true_start == other.true_start and
                    self.true_stop == other.true_stop)
        except (AttributeError, TypeError):
            return False


    # ----------------------------------------------------------------------------------------------------------------

    def now(self):
        if self.model_start is None:
            return ClockISODatetime.now()

        now = ClockISODatetime.now() if self.is_running else self.true_stop

        true_period = now - self.true_start
        model_period = true_period * self.speed

        return self.model_start + model_period


    def run(self):
        if not self.exists(Host):
            raise RuntimeError('run - no clock configuration exists')

        if self.is_running:
            return

        self.__true_start = ClockISODatetime.now()
        self.__true_stop = None
        self.__is_running = True


    def pause(self):
        if not self.exists(Host):
            raise RuntimeError('pause - no clock configuration exists')

        if not self.is_running:
            return

        self.__true_stop = ClockISODatetime.now()
        self.__is_running = False


    def resume(self):
        if not self.exists(Host):
            raise RuntimeError('resume - no clock configuration exists')

        if self.is_running:
            return

        paused_period = ClockISODatetime.now() - self.true_stop

        self.__true_start = self.true_start + paused_period
        self.__true_stop = None
        self.__is_running = True


    def reload(self, stored: ClockISODatetime):
        now = ClockISODatetime.now()

        if self.model_start is None:
            self.__model_start = stored
            self.__true_start = now

        else:
            model_period = stored - self.model_start
            true_period = model_period / self.speed
            self.__true_start = now - true_period

        self.__true_stop = None
        self.__is_running = True


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        jdict = OrderedDict()

        jdict['is_running'] = self.is_running
        jdict['speed'] = self.speed

        jdict['model_start'] = self.model_start
        jdict['true_start'] = self.true_start
        jdict['true_stop'] = self.true_stop

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def is_running(self):
        return self.__is_running


    @property
    def speed(self):
        return self.__speed


    @property
    def tick_interval(self):
        return 1.0 / self.speed


    @property
    def model_start(self):
        return self.__model_start


    @property
    def true_start(self):
        return self.__true_start


    @property
    def true_stop(self):
        return self.__true_stop


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return (f'Clock{{is_running:{self.is_running}, speed:{self.speed}, model_start:{self.model_start}, '
                f'true_start:{self.true_start}, true_stop:{self.true_stop}}}')
