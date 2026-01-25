"""
Created on 9 Nov 2025

@author: Bruno Beloff (bbeloff@me.com)

A structured representation of a message
Note that recorder components follow system time, not model time.

{
    "routing": "TST.001.002.MPU.001.100",
    "body": "hello"
}

https://www.geeksforgeeks.org/python/python-sqlite-working-with-date-and-datetime/
https://stackoverflow.com/questions/17574784/sqlite-current-timestamp-with-milliseconds
https://forum.xojo.com/t/sqlite-return-id-of-record-inserted/37896/3
"""

from collections import OrderedDict

from mrcs_core.data.iso_datetime import ISODatetime
from mrcs_core.messaging.message import Message
from mrcs_core.messaging.routing_key import RoutingKey, PublicationRoutingKey


# --------------------------------------------------------------------------------------------------------------------

class MessageRecord(Message):
    """
    classdocs
    """

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        uid = jdict.get('uid')
        rec = ISODatetime.construct_from_jdict(jdict.get('rec'))
        origin = jdict.get('origin')
        routing_key = PublicationRoutingKey.construct_from_jdict(jdict.get('routing'))
        body = jdict.get('body')

        return cls(uid, rec, routing_key, body, origin)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, uid: int, rec: ISODatetime, routing_key: RoutingKey, body, origin):
        super().__init__(routing_key, body, origin=origin)

        self.__uid = uid
        self.__rec = rec


    def __eq__(self, other):
        try:
            return (self.uid == other.uid and self.rec == other.rec and self.origin == other.origin and
                    self.routing_key == other.routing_key and self.body == other.body)
        except (AttributeError, TypeError):
            return False


    def __lt__(self, other):
        return self.uid < other.uid


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        jdict = OrderedDict()

        jdict['uid'] = self.uid
        jdict['rec'] = self.rec
        jdict['origin'] = self.origin
        jdict['routing'] = self.routing_key
        jdict['body'] = self.body

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def uid(self):
        return self.__uid


    @property
    def rec(self):
        return self.__rec


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return (f'{self.__class__.__name__}:{{uid:{self.uid}, rec:{self.rec}, origin:{self.origin}, '
                f'routing_key:{self.routing_key}, body:{self.body}}}')
