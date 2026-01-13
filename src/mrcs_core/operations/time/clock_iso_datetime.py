"""
Created on 2 Jan 2026

@author: Bruno Beloff (bbeloff@me.com)
"""

from mrcs_core.data.iso_datetime import ISODatetime
from mrcs_core.data.json import PersistentJSONable


# --------------------------------------------------------------------------------------------------------------------

class ClockISODatetime(ISODatetime, PersistentJSONable):
    """
    classdocs
    """

    __FILENAME = "model_time.json"

    @classmethod
    def persistence_location(cls):
        return cls.conf_dir(), cls.__FILENAME


    @classmethod
    def construct_from_jdict(cls, iso_string):
        return super().construct_from_jdict(iso_string)


    # ----------------------------------------------------------------------------------------------------------------

    # noinspection PyUnusedLocal
    def __init__(self, year, month=None, day=None, hour=0, minute=0, second=0, microsecond=0, tzinfo=None, *, fold=0):
        super().__init__()
