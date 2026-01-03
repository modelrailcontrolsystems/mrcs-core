"""
Created on 31 Dec 2025

@author: Bruno Beloff (bbeloff@me.com)

Message-based Cron - this class represents a cron job to be performed
Note that the cron components work in model time, not true time.

{
    "target": "SCH.*.001",
    "event_id": "abc",
    "on": "2025-12-31T06:00:00.000"
}
"""

from collections import OrderedDict

from mrcs_core.data.equipment_identity import EquipmentIdentifier
from mrcs_core.data.iso_datetime import ISODatetime
from mrcs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class Cronjob(JSONable):
    """
    represents a cron job to be performed
    """

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        target = EquipmentIdentifier.construct_from_jdict(jdict.get('target'))
        event_id = jdict.get('event_id')
        on_datetime = ISODatetime.construct_from_jdict(jdict.get('on'))

        return cls(target, event_id, on_datetime)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, target: EquipmentIdentifier | None, event_id: str, on_datetime: ISODatetime):
        super().__init__()

        self.__target = target              # the target of the cron event (may be the source of the crontab message)
        self.__event_id = event_id          # the ID of the event to be performed
        self.__on_datetime = on_datetime    # the model datetime when the event should be performed


    def __eq__(self, other):
        try:
            return (self.target == other.target and self.event_id == other.event_id and
                    self.on_datetime == other.on_datetime)
        except (AttributeError, TypeError):
            return False


    def __lt__(self, other):
        if self.on_datetime < other.on_datetime:
            return True

        if self.on_datetime > other.on_datetime:
            return False

        if self.target < other.target:
            return True

        if self.target > other.target:
            return False

        return self.event_id < other.event_id


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        jdict = OrderedDict()

        if self.target:
            jdict['target'] = self.target

        jdict['event_id'] = self.event_id
        jdict['on'] = self.on_datetime

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def target(self):
        return self.__target


    @property
    def event_id(self):
        return self.__event_id


    @property
    def on_datetime(self):
        return self.__on_datetime


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return f'Cronjob:{{target:{self.target}, event_id:{self.event_id}, on_datetime:{self.on_datetime}}}'
