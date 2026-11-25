"""
Created on 21 Nov 2026

@author: Bruno Beloff (bbeloff@me.com)

An ACK / NACK + data in response to a NodeCommand

The receiver must understand how to unpack the payload - this class simply assumes that the payload is JSONable.
"""

from abc import ABC, abstractmethod
from collections import OrderedDict
from enum import StrEnum
from typing import Any, Self

from mrcs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class NodeResponse[A: StrEnum](JSONable, ABC):
    """
    an ACK / NACK in response to a ResolutionCommand
    """


    @classmethod
    @abstractmethod
    def action_class(cls) -> type[A]:
        pass


    @classmethod
    def construct_error(cls, action: A, error: Exception):
        error_str = None if error is None else f'{error.__class__.__name__}: {str(error)}'
        return cls(action, error=error_str)


    @classmethod
    def construct_from_jdict(cls, jdict) -> Self:
        type_name = jdict.get('type')

        if type_name != cls.type_name():
            raise TypeError(f'required type:{cls.type_name()} got:{type_name}')

        action = cls.action_class()(jdict.get('action'))  # may raise KeyError
        error = jdict.get('error')
        payload = jdict.get('payload')

        return cls(action, error=error, payload=payload)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, action: A, error: str | None = None, payload: Any = None):
        self.__action = action
        self.__error = error
        self.__payload = payload  # JSONable (jdict when constructed from callback)


    def __eq__(self, other: Any) -> bool:
        try:
            return self.action == other.action and self.error == other.error and self.payload == other.payload
        except (AttributeError, TypeError):
            return False


    # ----------------------------------------------------------------------------------------------------------------

    def is_ACK(self):
        return self.error is None


    def is_NACK(self):
        return self.error is not None


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        jdict = OrderedDict()

        jdict['type'] = self.type_name()

        jdict['action'] = self.action

        if self.error is not None:
            jdict['error'] = self.error

        if self.payload is not None:
            jdict['payload'] = self.payload

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def action(self):
        return self.__action


    @property
    def error(self):
        return self.__error


    @property
    def payload(self):
        return self.__payload


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return f'{self.__class__.__name__}:{{action:{self.action}, error:{self.error}, payload:{self.payload}}}'
