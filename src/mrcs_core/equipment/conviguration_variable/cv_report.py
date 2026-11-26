"""
Created on 7 Oct 2026

@author: Bruno Beloff (bbeloff@me.com)

A reported configuration variable

{
    "type": "CVReport",
    "addr": 1,
    "value": 2
}
"""

from collections import OrderedDict
from typing import Any

from mrcs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class CVReport(JSONable):
    """
    A reported configuration variable
    """


    @classmethod
    def construct_from_jdict(cls, jdict) -> CVReport:
        type_name = jdict.get('type')

        if type_name != cls.type_name():
            raise TypeError(f'required type:{cls.type_name()} got:{type_name}')

        address = int(jdict.get('addr'))
        value = int(jdict.get('value'))

        return cls(address, value)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, address: int, value: int):
        self.__address = address
        self.__value = value


    def __eq__(self, other: Any):
        try:
            return self.address == other.address and self.value == other.value
        except (AttributeError, TypeError):
            return False


    def __lt__(self, other: Any):
        return self.address < other.address


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        jdict = OrderedDict()

        jdict['type'] = self.type_name()

        jdict['addr'] = self.address
        jdict['value'] = self.value

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def address(self):
        return self.__address


    @property
    def value(self):
        return self.__value


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return f'CVReport:{{address:{self.address}, value:{self.value}}}'
