"""
Created on 18 Jun 2026

@author: Bruno Beloff (bbeloff@me.com)

A DCC motive power unit (MPU) decoder state

            Addr    CV28         CV29          CV135        CV136           Start    Avg     Max
Class 08    0x003   0000 0011   0000 1110      0000 0000    0001 1000        4        1       120
Class 60    0x004   0000 0011   0000 1110      0000 0000    0001 1000        4        1       100

Based on code:
https://github.com/botmonster/z21aio/tree/main
"""

from collections import OrderedDict

from mrcs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class MotivePowerUnitDecoder(JSONable):
    """
    A DCC motive power unit (MPU) decoder state
    """


    @classmethod
    def construct_from_jdict(cls, jdict) -> MotivePowerUnitDecoder | None:
        if not jdict:
            return None

        type_name = jdict.get('type')

        if type_name != cls.__name__:
            raise TypeError(f'required type:{cls.__name__} got:{type_name}')

        address = jdict.get('addr')
        receive_count = jdict.get('received')
        error_count = jdict.get('errors')
        opts = jdict.get('opts')
        speed = jdict.get('speed')
        qos = jdict.get('qos')

        return cls(address, receive_count, error_count, opts, speed, qos)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, address: int, receive_count: int, error_count: int, opts: int, speed: int, qos: int):
        self._address = address
        self._receive_count = receive_count
        self._error_count = error_count
        self._opts = opts
        self._speed = speed
        self._qos = qos


    def __eq__(self, other):
        try:
            return (self.address == other.address and self.receive_count == other.receive_count and
                    self.error_count == other.error_count and self.opts == other.opts and
                    self.speed == other.speed and self.qos == other.qos)
        except (AttributeError, TypeError):
            return False


    def __lt__(self, other):
        if self.address < other.address:
            return True

        if self.address > other.address:
            return False

        return self.receive_count < other.receive_count


    # ----------------------------------------------------------------------------------------------------------------

    # noinspection PyUnresolvedReferences
    def as_json(self, **kwargs):
        jdict = OrderedDict()

        jdict['type'] = self.__class__.__name__

        jdict['addr'] = self.address
        jdict['received'] = self.receive_count
        jdict['errors'] = self.error_count
        jdict['opts'] = self.opts
        jdict['speed'] = self.speed
        jdict['qos'] = self.qos

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def address(self):
        return self._address


    @property
    def receive_count(self):
        return self._receive_count


    @property
    def error_count(self):
        return self._error_count


    @property
    def opts(self):
        return self._opts


    @property
    def speed(self):
        return self._speed


    @property
    def qos(self):
        return self._qos


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return (f'{self.__class__.__name__}:{{address:{self.address}, receive_count:{self.receive_count}, '
                f'error_count:{self.error_count}, opts:0x{self.opts:02x}, speed:{self.speed}, qos:{self.qos}}}')
