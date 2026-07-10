"""
Created on 9 Jul 2026

@author: Bruno Beloff (bbeloff@me.com)

An enumeration of all the possible Block operation modes
"""

from enum import StrEnum, unique

from mrcs_core.data.meta_enum import MetaEnum


# --------------------------------------------------------------------------------------------------------------------

@unique
class BlockOperation(StrEnum, metaclass=MetaEnum):
    """
    An enumeration of all the possible Block operation modes
    """

    UP_ONLY = 'UP_ONLY'
    DOWN_ONLY = 'DOWN_ONLY'
    REVERSIBLE = 'REVERSIBLE'


    # ----------------------------------------------------------------------------------------------------------------

    def may_operate_up(self):
        return self != BlockOperation.DOWN_ONLY


    def may_operate_down(self):
        return self != BlockOperation.UP_ONLY
