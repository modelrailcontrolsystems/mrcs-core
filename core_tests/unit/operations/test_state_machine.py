"""
Created on 10 Nov 2026

@author: Bruno Beloff (bbeloff@me.com)

python -m unittest -v unit/operations/test_state_machine.py

https://realpython.com/python-testing/
https://www.jetbrains.com/help/pycharm/creating-tests.html
"""

import unittest
from enum import StrEnum
from typing import Any, cast

from mrcs_core.operations.state_machine import StateMachine, StateMachineException


# --------------------------------------------------------------------------------------------------------------------

class SampleNode(StrEnum):
    STANDBY = 'STANDBY'
    RUNNING = 'RUNNING'
    STOPPING = 'STOPPING'
    STOPPED = 'STOPPED'


class OtherNode(StrEnum):
    OTHER = 'OTHER'


class SampleStateMachine(StateMachine[SampleNode]):
    @classmethod
    def transitions(cls) -> dict[SampleNode, set[SampleNode]]:
        return {
            SampleNode.STANDBY: {SampleNode.RUNNING},
            SampleNode.RUNNING: {SampleNode.STOPPING, SampleNode.STANDBY},
            SampleNode.STOPPING: {SampleNode.STOPPED},
            SampleNode.STOPPED: set(),
        }


    # public wrappers for the protected methods under test
    def is_node(self, a: SampleNode) -> bool:
        return self._is(a)


    def go(self, b: SampleNode) -> None:
        self._go(b)


# --------------------------------------------------------------------------------------------------------------------

class TestStateMachine(unittest.TestCase):
    # some tests deliberately misuse the API - cast(Any, ...) stops the type checker rejecting them


    def test_construct(self):
        obj1 = SampleStateMachine(SampleNode.STANDBY)
        self.assertEqual(SampleNode.STANDBY, obj1.node)


    def test_construct_not_enum(self):
        with self.assertRaises(StateMachineException):
            SampleStateMachine(cast(Any, 'STANDBY'))


    def test_construct_abstract(self):
        with self.assertRaises(TypeError):
            cast(Any, StateMachine)(SampleNode.STANDBY)


    def test_exception_is_runtime_error(self):
        self.assertTrue(issubclass(StateMachineException, RuntimeError))


    # ----------------------------------------------------------------------------------------------------------------

    def test_is_permitted_transition(self):
        self.assertTrue(SampleStateMachine.is_permitted_transition(SampleNode.STANDBY, SampleNode.RUNNING))


    def test_is_permitted_transition_not_permitted(self):
        self.assertFalse(SampleStateMachine.is_permitted_transition(SampleNode.STANDBY, SampleNode.STOPPED))


    def test_is_permitted_transition_to_self(self):
        self.assertFalse(SampleStateMachine.is_permitted_transition(SampleNode.STANDBY, SampleNode.STANDBY))


    def test_is_permitted_transition_from_terminal(self):
        for node in SampleNode:
            self.assertFalse(SampleStateMachine.is_permitted_transition(SampleNode.STOPPED, node))


    # ----------------------------------------------------------------------------------------------------------------

    def test_is(self):
        obj1 = SampleStateMachine(SampleNode.RUNNING)
        self.assertTrue(obj1.is_node(SampleNode.RUNNING))
        self.assertFalse(obj1.is_node(SampleNode.STANDBY))


    # ----------------------------------------------------------------------------------------------------------------

    def test_go(self):
        obj1 = SampleStateMachine(SampleNode.STANDBY)
        obj1.go(SampleNode.RUNNING)
        self.assertEqual(SampleNode.RUNNING, obj1.node)


    def test_go_sequence(self):
        obj1 = SampleStateMachine(SampleNode.STANDBY)

        for node in [SampleNode.RUNNING, SampleNode.STOPPING, SampleNode.STOPPED]:
            obj1.go(node)
            self.assertEqual(node, obj1.node)


    def test_go_and_back(self):
        obj1 = SampleStateMachine(SampleNode.STANDBY)
        obj1.go(SampleNode.RUNNING)
        obj1.go(SampleNode.STANDBY)
        self.assertEqual(SampleNode.STANDBY, obj1.node)


    def test_go_not_permitted(self):
        obj1 = SampleStateMachine(SampleNode.STANDBY)

        with self.assertRaises(StateMachineException):
            obj1.go(SampleNode.STOPPED)


    def test_go_not_permitted_node_unchanged(self):
        obj1 = SampleStateMachine(SampleNode.STANDBY)

        try:
            obj1.go(SampleNode.STOPPED)
        except StateMachineException:
            pass

        self.assertEqual(SampleNode.STANDBY, obj1.node)


    def test_node_is_read_only(self):
        obj1 = SampleStateMachine(SampleNode.STANDBY)

        with self.assertRaises(AttributeError):
            setattr(obj1, 'node', SampleNode.STOPPED)


    def test_go_from_terminal(self):
        obj1 = SampleStateMachine(SampleNode.STOPPED)

        with self.assertRaises(StateMachineException):
            obj1.go(SampleNode.STANDBY)


    # ----------------------------------------------------------------------------------------------------------------

    def test_is_permitted_transition_unknown_node(self):
        self.assertFalse(SampleStateMachine.is_permitted_transition(cast(Any, OtherNode.OTHER), SampleNode.RUNNING))


    def test_go_from_unknown_node(self):
        obj1 = SampleStateMachine(cast(Any, OtherNode.OTHER))

        with self.assertRaises(StateMachineException):
            obj1.go(SampleNode.RUNNING)


# --------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    unittest.main()
