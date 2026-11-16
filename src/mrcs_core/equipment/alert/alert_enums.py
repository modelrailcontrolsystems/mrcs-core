"""
Created on 15 Nov 2026

@author: Bruno Beloff (bbeloff@me.com)

The enumerated types used by alerts
"""

from enum import IntEnum, StrEnum, unique

from mrcs_core.data.json import JSONable
from mrcs_core.data.meta_enum import ABCMetaEnum, MetaEnum


# --------------------------------------------------------------------------------------------------------------------

@unique
class Severity(JSONable, IntEnum, metaclass=ABCMetaEnum):
    """
    An enumeration of all the possible severity levels
    """

    HIGH = 0
    MEDIUM = 1
    LOW = 2


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        return self.name


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return f'{self.name}{{{self.value}}}'


# --------------------------------------------------------------------------------------------------------------------

@unique
class Impact(StrEnum, metaclass=MetaEnum):
    """
    An enumeration of all the possible impact radii
    """

    LOCAL = 'LOCAL'
    GLOBAL = 'GLOBAL'


# --------------------------------------------------------------------------------------------------------------------

@unique
class Subject(StrEnum, metaclass=MetaEnum):
    """
    An enumeration of all the possible sources for an alert
    """

    BLOCK = 'LOCAL'
    MPU = 'MPU'
    SYSTEM = 'SYSTEM'
    TRACK = 'TRACK'
