"""
Created on 7 Oct 2026

@author: Bruno Beloff (bbeloff@me.com)

A reported configuration variable

{
    "type": "CVReport",
    "addr": 1,
    "value": 2
}"""

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

        cv_address = int(jdict.get('addr'))
        value = int(jdict.get('value'))

        return cls(cv_address, value)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, cv_address: int, value: int):
        self.__cv_address = cv_address
        self.__value = value


    def __eq__(self, other: Any):
        try:
            return self.cv_address == other.cv_address and self.value == other.value
        except (AttributeError, TypeError):
            return False


    def __lt__(self, other: Any):
        return self.cv_address < other.cv_address


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        jdict = OrderedDict()

        jdict['type'] = self.type_name()

        jdict['addr'] = self.cv_address
        jdict['value'] = self.value

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def cv_address(self):
        return self.__cv_address


    @property
    def value(self):
        return self.__value


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return f'{self.__class__.__name__}:{{cv_address:{self.cv_address}, value:{self.value}}}'
