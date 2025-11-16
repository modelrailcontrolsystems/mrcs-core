"""
Created on 11 Nov 2025

@author: Bruno Beloff (bbeloff@me.com)

https://stackoverflow.com/questions/70198931/how-to-use-milliseconds-instead-of-microsenconds-in-datetime-python
https://stackoverflow.com/questions/24966806/subclassing-datetime-datetime
https://stackoverflow.com/questions/4770297/convert-utc-datetime-string-to-local-datetime
https://labex.io/tutorials/python-how-to-create-datetime-objects-from-iso-8601-date-strings-417942
"""

import dateutil.tz

from datetime import datetime

from mrcs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class ISODatetime(JSONable, datetime):
    """
    classdocs
    """

    __UTC_ZONE = dateutil.tz.tzutc()
    __LOCAL_ZONE = dateutil.tz.tzlocal()

    __DB_FORMAT = "%Y-%m-%d %H:%M:%S.%f"

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, iso_string):
        if not iso_string:
            return None

        iso = super().fromisoformat(iso_string)

        return iso.astimezone(cls.__LOCAL_ZONE)


    @classmethod
    def construct_from_db(cls, field):
        db_naive = cls.strptime(field, cls.__DB_FORMAT)
        db_utc = db_naive.replace(tzinfo=cls.__UTC_ZONE)

        return db_utc.astimezone(cls.__LOCAL_ZONE)


    @classmethod
    def now(cls, tz=None):
        tzinfo = cls.__LOCAL_ZONE if tz is None else tz

        return super().now().replace(tzinfo=tzinfo)


    # ----------------------------------------------------------------------------------------------------------------

    def __new__(cls, *args, **kwargs):
        return datetime.__new__(cls, *args, **kwargs)


    # ----------------------------------------------------------------------------------------------------------------

    def dbformat(self):
        db_utc = self.astimezone(self.__UTC_ZONE)
        db_utc_millis = db_utc.strftime(self.__DB_FORMAT)[:-3]

        return db_utc_millis


    def isoformat(self, sep='T', timespec='milliseconds'):
        return super().isoformat(sep=sep, timespec=timespec)


    def as_json(self, **kwargs):
        return self.isoformat()


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return f'ISODatetime:{{{self.isoformat()}}}'
