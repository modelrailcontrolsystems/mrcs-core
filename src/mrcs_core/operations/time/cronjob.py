"""
Created on 31 Dec 2025

@author: Bruno Beloff (bbeloff@me.com)

Message-based Cron - this class represents a cron job to be performed

{
    "source": "SCH.*.001",
    "event_id": "abc",
    "on": "2025-12-31T06:00:00.000"
}
"""

from collections import OrderedDict

from mrcs_core.data.equipment_identity import EquipmentIdentifier
from mrcs_core.data.iso_datetime import ISODatetime
from mrcs_core.data.json import JSONable


# TODO: needs to handle the case where the job is going to be sent in a message, so does not need source
# --------------------------------------------------------------------------------------------------------------------

class Cronjob(JSONable):
    """
    represents a cron job to be performed
    """

    # @classmethod
    # def construct_from_callback(cls, routing_key: RoutingKey, body_str: bytes):
    #     return cls(routing_key, json.loads(body_str.decode()))


    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        source = EquipmentIdentifier.construct_from_jdict(jdict.get('source'))
        event_id = jdict.get('event_id')
        on_datetime = ISODatetime.construct_from_jdict(jdict.get('on'))

        return cls(source, event_id, on_datetime)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, source: EquipmentIdentifier, event_id: str, on_datetime: ISODatetime):
        super().__init__()

        self.__source = source                  # the equipment requesting the job
        self.__event_id = event_id              # the ID of the event to be performed
        self.__on_datetime = on_datetime        # the model datetime when the event should be performed


    def __eq__(self, other):
        try:
            return (self.source == other.source and self.event_id == other.event_id and
                    self.on_datetime == other.on_datetime)
        except (AttributeError, TypeError):
            return False


    def __lt__(self, other):
        if self.on_datetime < other.on_datetime:
            return True

        if self.on_datetime > other.on_datetime:
            return False

        if self.source < other.source:
            return True

        if self.source > other.source:
            return False

        return self.event_id < other.event_id


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        jdict = OrderedDict()

        jdict['source'] = self.source
        jdict['event_id'] = self.event_id
        jdict['on'] = self.on_datetime

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def source(self):
        return self.__source


    @property
    def event_id(self):
        return self.__event_id


    @property
    def on_datetime(self):
        return self.__on_datetime


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return f'Cronjob:{{source:{self.source}, event_id:{self.event_id}, on_datetime:{self.on_datetime}}}'
