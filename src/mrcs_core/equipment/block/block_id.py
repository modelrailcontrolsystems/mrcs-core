"""
Created on 2 Jul 2026

@author: Bruno Beloff (bbeloff@me.com)

A unique identifier for a block, as defined by its detector
Note that that (address, channel) for a PK, the reporter_id field is purely for validation.

Based on the Roco 10808 detector:
https://www.roco.cc/ren/products/control/accessories/10808-z21-detector.html

Based on code:
https://github.com/botmonster/z21aio/tree/main
"""

from collections import OrderedDict

from mrcs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class BlockID(JSONable):
    """
    A unique identifier for a block, as defined by its detector
    """


    @classmethod
    def construct_from_jdict(cls, jdict) -> BlockID:
        address = jdict.get('addr')
        channel = jdict.get('channel')
        reporter_id = jdict.get('rid')

        return cls(address, channel, reporter_id)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, address: int, channel: int, reporter_id: int):
        self._address = address
        self._channel = channel
        self._reporter_id = reporter_id


    def __eq__(self, other):
        try:
            return (self.address == other.address and self.channel == other.channel and
                    self.reporter_id == other.reporter_id)
        except (AttributeError, TypeError):
            return False


    def __lt__(self, other):
        if self.address < other.address:
            return True

        if self.address > other.address:
            return False

        return self.channel < other.channel


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        jdict = OrderedDict()

        jdict['addr'] = self.address
        jdict['channel'] = self.channel
        jdict['rid'] = self.reporter_id

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def block_address(self):
        return f'{self.address}/{self.channel}'


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def address(self):
        return self._address


    @property
    def channel(self):
        return self._channel


    @property
    def reporter_id(self):
        return self._reporter_id


    # ----------------------------------------------------------------------------------------------------------------

    # noinspection PyUnresolvedReferences
    def __str__(self, *args, **kwargs):
        return f'BlockID:{{address:{self.address}, channel:{self.channel}, reporter_id:0x{self.reporter_id:04x}}}'
