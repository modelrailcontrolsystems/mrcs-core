"""
Created on 5 Jul 2026

@author: Bruno Beloff (bbeloff@me.com)

Motive power unit (MPU) function state

"+-+-----"
"""

from typing import List

from mrcs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class MPUFunctions(JSONable):
    """
    Motive power unit (MPU) function state
    """


    @classmethod
    def construct_from_jdict(cls, jdict) -> MPUFunctions:
        if not jdict:
            raise ValueError('MPUFunctions.construct_from_jdict should not be None')

        return cls([func == '+' for func in jdict])


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, funcs: List[bool]):
        self._funcs = funcs


    def __eq__(self, other):
        try:
            return self.funcs == other.funcs
        except (AttributeError, TypeError):
            return False


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        return ''.join('+' if f else '-' for f in self.funcs)


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def funcs(self):
        return self._funcs


    # ----------------------------------------------------------------------------------------------------------------

    # noinspection PyUnresolvedReferences
    def __str__(self, *args, **kwargs):
        return f'MPUFunctions:{{{self.as_json()}}}'
