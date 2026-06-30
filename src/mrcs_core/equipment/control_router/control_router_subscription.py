"""
Created on 29 Jun 2026

@author: Bruno Beloff (bbeloff@me.com)

Networking configuration of a DCC control router

{
    "flags": [
        "CAN_DETECTOR",
        "TRACK",
        "X_LOCO_INFO_ALL"
    ]
}
"""

import operator
from collections import OrderedDict
from functools import reduce

from mrcs_control.dcc.z21.command.broadcast import Broadcast
from mrcs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class ControlRouterSubscription(JSONable):
    """
    classdocs
    """


    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        # may raise KeyError
        flags = [Broadcast[flag] for flag in jdict.get('flags')]

        return cls(*flags)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, *flags: Broadcast):
        for flag in flags:
            if flag == Broadcast.NONE:
                raise ValueError(f'flag {flag} is not a valid subscription flag')

        self.__flags = set(flags)


    def __eq__(self, other):
        try:
            return self.flags == other.flags
        except (AttributeError, TypeError):
            return False


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        jdict = OrderedDict()

        jdict['flags'] = self.flag_names

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def value(self):
        return reduce(operator.or_, self.flags, Broadcast.NONE.value)


    @property
    def flags(self):
        return self.__flags


    @property
    def flag_names(self):
        return sorted([flag.name for flag in self.flags])


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        flag_names = '[' + ', '.join(self.flag_names) + ']'
        return f'ControlRouterSubscription:{{flags:{flag_names}}}'
