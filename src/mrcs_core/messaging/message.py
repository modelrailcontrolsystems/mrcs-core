"""
Created on 2 Nov 2025

@author: Bruno Beloff (bbeloff@me.com)

A structured representation of a message

{
    "origin": "12345678",
    "routing": "TST.001.002.MPU.001.100",
    "body": "hello"
}

https://stackoverflow.com/questions/13484726/safe-enough-8-character-short-unique-random-string
"""

import json
import uuid

from collections import OrderedDict

from mrcs_core.data.json import JSONable, JSONify
from mrcs_core.messaging.routing_key import RoutingKey, PublicationRoutingKey


# --------------------------------------------------------------------------------------------------------------------

class Message(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    class Payload(JSONable):
        """
        classdocs
        """

        @classmethod
        def construct_from_jdict(cls, jdict):
            if not jdict:
                return None

            origin = jdict.get('origin')
            body = jdict.get('body')

            return cls(origin, body)


        # ------------------------------------------------------------------------------------------------------------

        def __init__(self, origin, body):
            super().__init__()

            self.__origin = origin
            self.__body = body


        # ------------------------------------------------------------------------------------------------------------

        @property
        def origin(self):
            return self.__origin


        @property
        def body(self):
            return self.__body


        # ------------------------------------------------------------------------------------------------------------

        def as_json(self, **kwargs):
            jdict = OrderedDict()

            jdict['origin'] = self.origin
            jdict['body'] = self.body

            return jdict


        # ------------------------------------------------------------------------------------------------------------

        def __str__(self, *args, **kwargs):
            return f'Message.Payload:{{origin:{self.origin}, body:{self.body}}}'


    # ----------------------------------------------------------------------------------------------------------------

    @staticmethod
    def truncated_uuid4():
        return str(uuid.uuid4())[:13]


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
    def construct_from_callback(cls, routing_key: RoutingKey, payload: bytes):
        payload = Message.Payload.construct_from_jdict(json.loads(payload.decode()))
        return cls(routing_key, payload.body, origin=payload.origin)


    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        origin = jdict.get('origin')
        routing_key = PublicationRoutingKey.construct_from_jdict(jdict.get('routing'))
        body = jdict.get('body')

        return cls(routing_key, body, origin=origin)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, routing_key: RoutingKey, body, origin=None):
        super().__init__()

        self.__origin = origin if origin else self.truncated_uuid4()

        self.__routing_key = routing_key
        self.__body = body                              # JSONable (jdict when constructed from callback)


    def __eq__(self, other):
        try:
            return self.origin == other.origin and self.routing_key == other.routing_key and self.body == other.body
        except (AttributeError, TypeError):
            return False


    def __lt__(self, other):
        if self.routing_key < other.routing_key:
            return True

        if self.routing_key > other.routing_key:
            return False

        return self.body < other.body


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        jdict = OrderedDict()

        jdict['origin'] = self.origin
        jdict['routing'] = self.routing_key
        jdict['body'] = self.body

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def payload(self):
        return Message.Payload(self.origin, self.body)


    @property
    def origin(self):
        return self.__origin


    @property
    def routing_key(self):
        return self.__routing_key


    @property
    def body(self):
        return self.__body


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return f'{self.__class__.__name__}:{{origin:{self.origin}, routing_key:{self.routing_key}, body:{self.body}}}'
