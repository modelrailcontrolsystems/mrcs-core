"""
Created on 13 Jun 2026

@author: Bruno Beloff (bbeloff@me.com)

The track state

Based on code:
https://github.com/botmonster/z21aio/tree/main
"""

from collections import OrderedDict

from mrcs_core.data.json import JSONable
from mrcs_core.equipment.track.track_mode import TrackMode


# --------------------------------------------------------------------------------------------------------------------

class TrackState(JSONable):
    """
    The track state
    """


    @classmethod
    def construct_from_jdict(cls, jdict) -> TrackState | None:
        if not jdict:
            return None

        type_name = jdict.get('type')

        if type_name != cls.__name__:
            raise TypeError(f'required type:{cls.__name__} got:{type_name}')

        # may raise KeyError
        mode = TrackMode[jdict.get('mode')]

        return cls(mode)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, mode: TrackMode):
        self.__mode = mode


    def __eq__(self, other):
        try:
            return self.mode == other.mode
        except (AttributeError, TypeError):
            return False


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        jdict = OrderedDict()

        jdict['type'] = self.__class__.__name__
        jdict['mode'] = self.mode.name

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def is_unknown(self) -> bool:
        return bool(self.mode == TrackMode.UNKNOWN)


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def mode(self):
        return self.__mode


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return f'{self.__class__.__name__}:{{mode:{self.mode.name}}}'
