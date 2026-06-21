"""
Created on 6 Jun 2026

@author: Bruno Beloff (bbeloff@me.com)

A DCC motive power unit (MPU) state

Based on code:
https://github.com/botmonster/z21aio/tree/main
"""

from collections import OrderedDict

from mrcs_core.data.json import JSONable
from mrcs_core.equipment.motive_power_unit.throttle import DCCThrottleSteps


# --------------------------------------------------------------------------------------------------------------------

class MotivePowerUnitState(JSONable):
    """
    A DCC motive power unit (MPU) state
    """


    @classmethod
    def construct_from_jdict(cls, jdict) -> MotivePowerUnitState | None:
        if not jdict:
            return None

        type_name = jdict.get('type')

        if type_name != cls.__name__:
            raise TypeError(f'required type:{cls.__name__} got:{type_name}')

        # may raise KeyError
        stepping = None if jdict.get('stepping') is None else DCCThrottleSteps[jdict.get('stepping')]

        address = jdict.get('addr')
        functions = [function == '+' for function in jdict.get('functions')]
        is_busy = jdict.get('busy')
        stepping = stepping
        speed_value = jdict.get('speed')
        reverse = jdict.get('reverse')
        double_traction = jdict.get('consist')
        smart_search = jdict.get('smart_search')

        return cls(address, functions, is_busy=is_busy,
                   stepping=stepping, speed_value=speed_value,
                   reverse=reverse, double_traction=double_traction,
                   smart_search=smart_search)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, address: int, functions: list[bool], is_busy: bool | None = None,
                 stepping: DCCThrottleSteps | None = None, speed_value: int | None = None,
                 reverse: bool | None = None, double_traction: bool | None = None,
                 smart_search: bool | None = None):
        self._address = address
        self._functions = functions
        self._is_busy = is_busy
        self._stepping = stepping
        self._speed_value = speed_value
        self._reverse = reverse
        self._double_traction = double_traction
        self._smart_search = smart_search


    def __eq__(self, other):
        try:
            return (self.address == other.address and self.functions == other.functions and
                    self.is_busy == other.is_busy and self.stepping == other.stepping and
                    self.speed_value == other.speed_value and self.reverse == other.reverse and
                    self.double_traction == other.double_traction and self.smart_search == other.smart_search)
        except (AttributeError, TypeError):
            return False


    def __lt__(self, other):
        return self.address < other.address


    # ----------------------------------------------------------------------------------------------------------------

    # noinspection PyUnresolvedReferences
    def as_json(self, **kwargs):
        jdict = OrderedDict()

        jdict['type'] = self.__class__.__name__

        jdict['addr'] = self.address
        jdict['functions'] = ''.join('+' if f else '-' for f in self.functions)
        jdict['busy'] = self.is_busy
        jdict['stepping'] = None if self.stepping is None else self.stepping.name
        jdict['speed'] = self.speed_value
        jdict['reverse'] = self.reverse
        jdict['consist'] = self.double_traction
        jdict['smart_search'] = self.smart_search

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def is_emergency_stop(self) -> bool:
        return self.speed_value == 1


    # noinspection PyUnresolvedReferences
    @property
    def speed_percentage(self):
        if self.stepping is None or self.speed_value is None:
            return None

        return round((self.speed_value / self.stepping.max_speed) * 100.0)


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def address(self):
        return self._address


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
    def speed_value(self):
        return self._speed_value


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
        functions = ''.join('+' if f else '-' for f in self.functions)
        stepping = None if self.stepping is None else self.stepping.name

        return (f'{self.__class__.__name__}:{{address:{self.address}, functions:{functions}, is_busy:{self.is_busy}, '
                f'stepping:{stepping}, speed_value:{self.speed_value}, reverse:{self.reverse}, '
                f'double_traction:{self.double_traction}, smart_search:{self.smart_search}}}')
