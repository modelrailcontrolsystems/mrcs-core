"""
Created on 2 Jul 2026

@author: Bruno Beloff (bbeloff@me.com)

A unique identifier for a block, as defined by its detector
Note that that (detector_address, channel) for a PK, the reporter_id field is purely for validation.

Based on the Roco 10808 detector:
https://www.roco.cc/ren/products/control/accessories/10808-z21-detector.html

Based on code:
https://github.com/botmonster/z21aio/tree/main
"""

from collections import OrderedDict
from typing import Any

from mrcs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class BlockID(JSONable):
    """
    A unique identifier for a block, as defined by its detector
    """


    @classmethod
    def construct_from_jdict(cls, jdict) -> BlockID:
        detector_address = jdict.get('addr')
        channel = jdict.get('channel')
        reporter_id = jdict.get('rid')

        return cls(detector_address, channel, reporter_id)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, detector_address: int, channel: int, reporter_id: int):
        self._detector_address = detector_address
        self._channel = channel
        self._reporter_id = reporter_id


    def __eq__(self, other: Any):
        try:
            return (self.detector_address == other.detector_address and self.channel == other.channel and
                    self.reporter_id == other.reporter_id)
        except (AttributeError, TypeError):
            return False


    def __lt__(self, other: Any):
        if self.detector_address < other.detector_address:
            return True

        if self.detector_address > other.detector_address:
            return False

        return self.channel < other.channel


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        jdict = OrderedDict()

        jdict['addr'] = self.detector_address
        jdict['channel'] = self.channel
        jdict['rid'] = self.reporter_id

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def block_address(self):
        return f'{self.detector_address}/{self.channel}'


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def detector_address(self):
        return self._detector_address


    @property
    def channel(self):
        return self._channel


    @property
    def reporter_id(self):
        return self._reporter_id


    # ----------------------------------------------------------------------------------------------------------------

    # noinspection PyUnresolvedReferences
    def __str__(self, *args, **kwargs):
        return (f'BlockID:{{detector_address:{self.detector_address}, channel:{self.channel}, '
                f'reporter_id:0x{self.reporter_id:04x}}}')
