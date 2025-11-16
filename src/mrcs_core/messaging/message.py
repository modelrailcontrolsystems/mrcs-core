"""
Created on 2 Nov 2025

@author: Bruno Beloff (bbeloff@me.com)

A structured representation of a message

{
    "routing": "TST.001.002.MPU.001.100",
    "body": "hello"
}
"""

import json

from collections import OrderedDict

from mrcs_core.data.json import JSONable, JSONify
from mrcs_core.data.persistence import PersistentObject
from mrcs_core.messaging.routing_key import RoutingKey, PublicationRoutingKey
from mrcs_core.operations.message.message_persistence import MessagePersistence


# --------------------------------------------------------------------------------------------------------------------

class Message(MessagePersistence, PersistentObject, JSONable):
    """
    classdocs
    """

    @staticmethod
    def is_valid(message: Message):
        if not RoutingKey.is_valid(message.routing_key):
            return False

        try:
            JSONify.dumps(message)
        except RuntimeError:
            return False

        return True


    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        routing_key = PublicationRoutingKey.construct_from_jdict(jdict.get('routing'))
        body = jdict.get('body')

        return cls(routing_key, body)


    @classmethod
    def construct_from_callback(cls, routing_key, body_str):
        return cls(routing_key, json.loads(body_str.decode()))


    @classmethod
    def construct_from_db(cls, *fields):
        raise NotImplementedError('use MessageRecord class instead')


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, routing_key: RoutingKey, body):
        super().__init__()

        self.__routing_key = routing_key                # RoutingKey
        self.__body = body                              # JSONable (jdict when constructed from callback)


    def __eq__(self, other):
        try:
            return self.routing_key == other.routing_key and self.body == other.body
        except (AttributeError, TypeError):
            return False


    def __lt__(self, other):
        if self.routing_key < other.routing_key:
            return True

        if self.routing_key > other.routing_key:
            return False

        return self.body < other.body


    # ----------------------------------------------------------------------------------------------------------------

    def save(self):
        return super().insert(self)


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        jdict = OrderedDict()

        jdict['routing'] = self.routing_key
        jdict['body'] = self.body

        return jdict


    def as_db(self):
        return self.routing_key.as_json(), JSONify.dumps(self.body)


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def routing_key(self):
        return self.__routing_key


    @property
    def body(self):
        return self.__body


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return f'Message:{{routing_key:{self.routing_key}, body:{self.body}}}'
