"""
Created on 9 Jul 2026

@author: Bruno Beloff (bbeloff@me.com)

An enumeration of all the possible Block operation modes
"""

from enum import StrEnum, unique

from mrcs_core.data.json import JSONable
from mrcs_core.data.meta_enum import ABCMetaEnum


# --------------------------------------------------------------------------------------------------------------------

@unique
class BlockOperation(JSONable, StrEnum, metaclass=ABCMetaEnum):
    """
    An enumeration of all the possible Block operation modes
    """

    UP_FAVOURED = 'UP_FAVOURED'
    UP_ONLY = 'UP_ONLY'
    DOWN_FAVOURED = 'DOWN_FAVOURED'
    DOWN_ONLY = 'DOWN_ONLY'
    REVERSIBLE = 'REVERSIBLE'


    # ----------------------------------------------------------------------------------------------------------------

    def may_operate_up(self):
        return self != BlockOperation.DOWN_ONLY


    def may_operate_down(self):
        return self != BlockOperation.UP_ONLY


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        return self.name


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return self.name
