"""
Created on 2 Nov 2025

@author: Bruno Beloff (bbeloff@me.com)

A structured representation of a message

{
    "routing": "src1.sec1.dev1",
    "body": "hello"
}
"""

from collections import OrderedDict

from mrcs_core.data.json import JSONable, JSONify
from mrcs_core.messaging.routing_key import RoutingKey


# --------------------------------------------------------------------------------------------------------------------

class Message(JSONable):
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

        routing_key = RoutingKey.construct_from_jdict(jdict.get('routing'))
        body = jdict.get('body')

        return cls(routing_key, body)


    @classmethod
    def construct(cls, routing, body):
        routing_key = RoutingKey.construct(routing)

        return cls(routing_key, body)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, routing_key: RoutingKey, body):
        """
        Constructor
        """
        super().__init__()

        self.__routing_key = routing_key                # RoutingKey
        self.__body = body                              # JSONable


    def __eq__(self, other):
        return self.routing_key == other.routing_key and self.body == other.body


    def __lt__(self, other):
        if self.routing_key < other.routing_key:
            return True

        if self.routing_key > other.routing_key:
            return False

        if self.body < other.body:
            return True

        return False


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        jdict = OrderedDict()

        jdict['routing'] = self.routing_key
        jdict['body'] = self.body

        return jdict


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
