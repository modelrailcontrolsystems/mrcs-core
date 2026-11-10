"""
Created on 9 Nov 2026

@author: Bruno Beloff (bbeloff@me.com)

An abstract state machine, managing the state node field
"""

from abc import ABC, abstractclassmethod
from enum import StrEnum

from mrcs_core.sys.logging import Logging


# --------------------------------------------------------------------------------------------------------------------

class StateMachineException(RuntimeError):
    """
    on an attempt to perform an ilegal operation
    """


# --------------------------------------------------------------------------------------------------------------------

class StateMachine[N: StrEnum](ABC):
    """
    an abstract state machine, managing the state node field
    """


    @abstractclassmethod
    def transitions(cls) -> dict[N, set[N]]:
        pass


    @classmethod
    def is_permitted_transition(cls, a: N, b: N) -> bool:
        return b in cls.transitions().get(a, set())  # a node with no entry has no permitted transitions


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, node: N):
        if not isinstance(node, StrEnum):
            raise StateMachineException(f'Node must be a StrEnum member, got {node!r}.')

        self.__node = node
        self.__logger = Logging.getLogger()


    # ----------------------------------------------------------------------------------------------------------------

    def _is(self, a: N) -> bool:
        return self.node == a


    def _go(self, b: N) -> None:
        if not self.is_permitted_transition(self.node, b):
            raise StateMachineException(f'No transition available from {self.node} to {b}.')

        self.logger.info(b)
        self.__node = b


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def node(self):
        return self.__node


    @property
    def logger(self):
        return self.__logger
