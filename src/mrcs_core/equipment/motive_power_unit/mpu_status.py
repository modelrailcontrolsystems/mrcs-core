"""
Created on 4 Jul 2026

@author: Bruno Beloff (bbeloff@me.com)

A DCC motive power unit (MPU) state
The label of the MPUStatus is found from the MPU Inventory

{
    "type": "MPUStatus",
    "label": "EMR Class 08",
    "addr": 3,
    "functions": "+-+",
    "speed_setting": 12,
    "reported_speed": 7,
    "actual_speed": 13.6,
    "direction": true
}
"""

from collections import OrderedDict
from typing import Any, Self

from mrcs_core.data.json import JSONable
from mrcs_core.equipment.motive_power_unit.mpu_enums import MPUDirection
from mrcs_core.equipment.motive_power_unit.mpu_functions import MPUFunctions


# --------------------------------------------------------------------------------------------------------------------

class MPUStatus(JSONable):
    """
    A DCC motive power unit (MPU) state
    """


    @classmethod
    def construct_from_jdict(cls, jdict) -> Self:
        try:
            label = jdict.get('label')
            mpu_address = int(jdict.get('addr'))
            functions = MPUFunctions.construct_from_jdict(jdict.get('functions'))
            speed_setting = jdict.get('speed_setting')
            reported_speed = jdict.get('reported_speed')
            actual_speed = jdict.get('actual_speed')
            direction = MPUDirection[jdict.get('direction')]

        except (TypeError, ValueError):
            raise ValueError(jdict)

        return cls(label, mpu_address, functions, speed_setting, reported_speed, actual_speed, direction)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, label: str, mpu_address: int, functions: MPUFunctions, speed_setting: int | None,
                 reported_speed: int | None, actual_speed: float | None, direction: MPUDirection):
        self._label = label
        self._mpu_address = mpu_address
        self._functions = functions
        self._speed_setting = speed_setting
        self._reported_speed = reported_speed
        self._actual_speed = actual_speed
        self._direction = direction


    def __eq__(self, other: Any):
        try:
            return (self.label == other.label and self.mpu_address == other.mpu_address and
                    self.functions == other.functions and self.speed_setting == other.speed_setting and
                    self.reported_speed == other.reported_speed and self.actual_speed == other.actual_speed and
                    self.direction == other.direction)
        except (AttributeError, TypeError):
            return False


    def __lt__(self, other: Any):
        return self.label < other.label


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        jdict = OrderedDict()

        jdict['type'] = self.type_name()

        jdict['label'] = self.label
        jdict['addr'] = self.mpu_address
        jdict['functions'] = self.functions
        jdict['speed_setting'] = self.speed_setting
        jdict['reported_speed'] = self.reported_speed

        if self.actual_speed is not None:
            jdict['actual_speed'] = self.actual_speed

        jdict['direction'] = self.direction

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def label(self):
        return self._label


    @property
    def mpu_address(self):
        return self._mpu_address


    @property
    def functions(self):
        return self._functions


    @property
    def speed_setting(self):
        return self._speed_setting


    @property
    def reported_speed(self):
        return self._reported_speed


    @property
    def actual_speed(self):
        return self._actual_speed


    @property
    def direction(self):
        return self._direction


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return (f'{self.__class__.__name__}:{{label:{self.label}, mpu_address:{self.mpu_address}, '
                f'functions:{self.functions.as_json()}, speed_setting:{self.speed_setting}, '
                f'reported_speed:{self.reported_speed}, actual_speed:{self.actual_speed}, '
                f'direction:{self.direction}}}')
