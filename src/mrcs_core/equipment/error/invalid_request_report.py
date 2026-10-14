"""
Created on 12 Oct 2026

@author: Bruno Beloff (bbeloff@me.com)

A reported invalid request (LAN_X_UNKNOWN_COMMAND)

{
    "type": "InvalidRequestReport",
    "code": 2
}
"""

from collections import OrderedDict
from typing import Any

from mrcs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class InvalidRequestReport(JSONable):
    """
    A reported invalid request (LAN_X_UNKNOWN_COMMAND)
    """


    @classmethod
    def construct_from_jdict(cls, jdict) -> InvalidRequestReport:
        type_name = jdict.get('type')

        if type_name != cls.type_name():
            raise TypeError(f'required type:{cls.type_name()} got:{type_name}')

        code = int(jdict.get('code'))

        return cls(code)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, code: int):
        self.__code = code


    def __eq__(self, other: Any):
        try:
            return self.code == other.code
        except (AttributeError, TypeError):
            return False


    def __lt__(self, other: Any):
        return self.code < other.code


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        jdict = OrderedDict()

        jdict['type'] = self.type_name()
        jdict['code'] = self.code

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def code(self):
        return self.__code


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return f'InvalidRequestReport:{{code:{self.code}}}'
