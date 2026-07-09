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
    "speed": 7,
    "reverse": true
}
"""

from collections import OrderedDict

from mrcs_core.data.json import JSONable
from mrcs_core.equipment.motive_power_unit.mpu_functions import MPUFunctions


# --------------------------------------------------------------------------------------------------------------------

class MPUStatus(JSONable):
    """
    A DCC motive power unit (MPU) state
    """


    @classmethod
    def construct_from_jdict(cls, jdict) -> MPUStatus:
        label = jdict.get('label')
        mpu_address = jdict.get('addr')
        functions = MPUFunctions.construct_from_jdict(jdict.get('functions'))
        speed_setting = jdict.get('speed_setting')
        speed = jdict.get('speed')
        reverse = jdict.get('reverse')

        return cls(label, mpu_address, functions, speed_setting, speed, reverse)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, label: str, mpu_address: int, functions: MPUFunctions, speed_setting: int, speed: int,
                 reverse: bool):
        self._label = label
        self._mpu_address = mpu_address
        self._functions = functions
        self._speed_setting = speed_setting
        self._speed = speed
        self._reverse = reverse


    def __eq__(self, other):
        try:
            return (self.label == other.label and self.mpu_address == other.mpu_address and
                    self.functions == other.functions and self.speed_setting == other.speed_setting and
                    self.speed == other.speed and self.reverse == other.reverse)
        except (AttributeError, TypeError):
            return False


    def __lt__(self, other):
        return self.label < other.label


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        jdict = OrderedDict()

        jdict['type'] = self.type_name()

        jdict['label'] = self.label
        jdict['addr'] = self.mpu_address
        jdict['functions'] = self.functions
        jdict['speed_setting'] = self.speed_setting
        jdict['speed'] = self.speed
        jdict['reverse'] = self.reverse

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
    def speed(self):
        return self._speed


    @property
    def reverse(self):
        return self._reverse


    # ----------------------------------------------------------------------------------------------------------------

    # noinspection PyUnresolvedReferences
    def __str__(self, *args, **kwargs):
        return (f'{self.type_name()}:{{label:{self.label}, mpu_address:{self.mpu_address}, '
                f'functions:{self.functions.as_json()}, speed_setting:{self.speed_setting}, speed:{self.speed}, '
                f'reverse:{self.reverse}}}')
