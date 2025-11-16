"""
Created on 9 Nov 2025

@author: Bruno Beloff (bbeloff@me.com)

A structured representation of a message

{
    "routing": "TST.001.002.MPU.001.100",
    "body": "hello"
}

https://www.geeksforgeeks.org/python/python-sqlite-working-with-date-and-datetime/
https://stackoverflow.com/questions/17574784/sqlite-current-timestamp-with-milliseconds
https://forum.xojo.com/t/sqlite-return-id-of-record-inserted/37896/3
"""

import json
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
        routing_key = PublicationRoutingKey.construct_from_jdict(jdict.get('routing'))
        body = jdict.get('body')

        return cls(uid, rec, routing_key, body)


    @classmethod
    def construct_from_db(cls, uid_field, rec_field, routing_key_field, body_field):
        uid = int(uid_field)
        rec = ISODatetime.construct_from_db(rec_field)
        routing_key = PublicationRoutingKey.construct_from_db(routing_key_field)
        body = json.loads(body_field)

        return cls(uid, rec, routing_key, body)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, uid: int, rec: ISODatetime, routing_key: RoutingKey, body):
        """
        Constructor
        """
        super().__init__(routing_key, body)

        self.__uid = uid
        self.__rec = rec


    def __eq__(self, other):
        try:
            return (self.uid == other.uid and self.rec == other.rec and
                    self.routing_key == other.routing_key and self.body == other.body)
        except (AttributeError, TypeError):
            return False


    def __lt__(self, other):
        return self.uid < other.uid


    # ----------------------------------------------------------------------------------------------------------------

    def save(self):
        raise NotImplementedError('use Message class instead')


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        jdict = OrderedDict()

        jdict['uid'] = self.uid
        jdict['rec'] = self.rec
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
        return f'MessageRecord:{{uid:{self.uid}, rec:{self.rec}, routing_key:{self.routing_key}, body:{self.body}}}'
