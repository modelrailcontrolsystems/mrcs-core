"""
Created on 6 Jun 2026

@author: Bruno Beloff (bbeloff@me.com)

A motive power unit (MPU) configuration

{
    "type": "MPUConfigurationReport",
    "addr": 3,
    "functions": "+-+",
    "busy": false,
    "stepping": "STEPS_28",
    "speed": 12,
    "reverse": true,
    "consist": false,
    "smart_search": true
}
"""

from collections import OrderedDict
from typing import Any

from mrcs_core.data.json import JSONable
from mrcs_core.equipment.motive_power_unit.mpu_enums import ThrottleSteps
from mrcs_core.equipment.motive_power_unit.mpu_functions import MPUFunctions


# --------------------------------------------------------------------------------------------------------------------

class MPUConfigurationReport(JSONable):
    """
    A motive power unit (MPU) configuration
    """


    @classmethod
    def construct_from_jdict(cls, jdict) -> MPUConfigurationReport:
        type_name = jdict.get('type')

        if type_name != cls.__name__:
            raise TypeError(f'required type:{cls.__name__} got:{type_name}')

        mpu_address = jdict.get('addr')
        functions = MPUFunctions.construct_from_jdict(jdict.get('functions'))
        is_busy = jdict.get('busy')
        stepping = ThrottleSteps[jdict.get('stepping')]
        speed_setting = jdict.get('speed')
        reverse = jdict.get('reverse')
        double_traction = jdict.get('consist')
        smart_search = jdict.get('smart_search')

        return cls(mpu_address, functions, is_busy, stepping, speed_setting, reverse, double_traction, smart_search)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, mpu_address: int, functions: MPUFunctions, is_busy: bool, stepping: ThrottleSteps,
                 speed_setting: int, reverse: bool, double_traction: bool, smart_search: bool):
        self._mpu_address = mpu_address
        self._functions = functions
        self._is_busy = is_busy
        self._stepping = stepping
        self._speed_setting = speed_setting
        self._reverse = reverse
        self._double_traction = double_traction
        self._smart_search = smart_search


    def __eq__(self, other: Any):
        try:
            return (self.mpu_address == other.mpu_address and self.functions == other.functions and
                    self.is_busy == other.is_busy and self.stepping == other.stepping and
                    self.speed_setting == other.speed_setting and self.reverse == other.reverse and
                    self.double_traction == other.double_traction and self.smart_search == other.smart_search)
        except (AttributeError, TypeError):
            return False


    def __lt__(self, other: Any):
        return self.mpu_address < other.mpu_address


    # ----------------------------------------------------------------------------------------------------------------

    # noinspection PyUnresolvedReferences
    def as_json(self, **kwargs):
        jdict = OrderedDict()

        jdict['type'] = self.type_name()

        jdict['addr'] = self.mpu_address
        jdict['functions'] = self.functions
        jdict['busy'] = self.is_busy
        jdict['stepping'] = None if self.stepping is None else self.stepping.name
        jdict['speed'] = self.speed_setting
        jdict['reverse'] = self.reverse
        jdict['consist'] = self.double_traction
        jdict['smart_search'] = self.smart_search

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def is_emergency_stop(self) -> bool:
        return self.speed_setting == 1


    # noinspection PyUnresolvedReferences
    @property
    def speed_setting_percent(self):
        return round((self.speed_setting / self.stepping.max_speed) * 100.0)


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def mpu_address(self):
        return self._mpu_address


    @property
    def functions(self):
        return self._functions


    @property
    def is_busy(self):
        return self._is_busy


    @property
    def stepping(self):
        return self._stepping


    @property
    def speed_setting(self):
        return self._speed_setting


    @property
    def reverse(self):
        return self._reverse


    @property
    def double_traction(self):
        return self._double_traction


    @property
    def smart_search(self):
        return self._smart_search


    # ----------------------------------------------------------------------------------------------------------------

    # noinspection PyUnresolvedReferences
    def __str__(self, *args, **kwargs):
        stepping = None if self.stepping is None else self.stepping.name

        return (f'{self.__class__.__name__}:{{mpu_address:{self.mpu_address}, functions:{self.functions.as_json()}, '
                f'is_busy:{self.is_busy}, stepping:{stepping}, speed_setting:{self.speed_setting}, '
                f'reverse:{self.reverse}, double_traction:{self.double_traction}, smart_search:{self.smart_search}}}')
