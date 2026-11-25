"""
Created on 19 Nov 2026

@author: Bruno Beloff (bbeloff@me.com)

A command that may be received by an operational node
"""

from abc import ABC, abstractmethod
from enum import StrEnum
from typing import Any, OrderedDict, Self

from mrcs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class CommandException(RuntimeError):
    """
    on a failure to construct or parse a command
    """


# --------------------------------------------------------------------------------------------------------------------

class NodeCommand[A: StrEnum](JSONable, ABC):
    """
    a command that may be received by an operational node
    """


    @classmethod
    @abstractmethod
    def action_class(cls) -> type[A]:
        pass


    @classmethod
    def construct_from_jdict(cls, jdict) -> Self:
        type_name = jdict.get('type')

        if type_name != cls.type_name():
            raise TypeError(f'required type:{cls.type_name()} got:{type_name}')

        action = cls.action_class()(jdict.get('action'))  # may raise KeyError
        response_required = bool(jdict.get('response_required', False))
        kwargs = jdict.get('kwargs', {})

        return cls(action, response_required=response_required, **kwargs)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, action: A, response_required: bool = True, **kwargs):
        if not isinstance(action, StrEnum):
            raise CommandException(f'action must be a StrEnum member, got {action!r}.')

        self.__action = action
        self.__response_required = response_required
        self.__kwargs = kwargs


    def __eq__(self, other: Any) -> bool:
        try:
            return (self.action == other.action and self.response_required == other.response_required and
                    self.kwargs == other.kwargs)
        except (AttributeError, TypeError):
            return False


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        jdict = OrderedDict()

        jdict['type'] = self.type_name()

        jdict['action'] = self.action
        jdict['response_required'] = self.response_required
        jdict['kwargs'] = self.kwargs

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def action(self):
        return self.__action


    @property
    def response_required(self):
        return self.__response_required


    @property
    def kwargs(self):
        return self.__kwargs


    def kwarg(self, key):
        return self.kwargs[key]  # may raise KeyError


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        kwargs = '{' + ', '.join(f'{key}: {value}' for key, value in self.kwargs.items()) + '}'

        return (f'{self.__class__.__name__}:{{action:{self.action}, response_required:{self.response_required}, '
                f'kwargs:{kwargs}}}')
