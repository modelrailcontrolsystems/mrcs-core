"""
Created on 21 Nov 2026

@author: Bruno Beloff (bbeloff@me.com)

The actions accepted by an AlertNode
"""

from enum import StrEnum, unique


# --------------------------------------------------------------------------------------------------------------------

@unique
class AlertAction(StrEnum):
    """
    the actions accepted by an AlertNode
    """

    UNKNOWN = 'UNKNOWN'

    RESOLVE = 'RESOLVE'
    RESOLVE_ALL = 'RESOLVE_ALL'
    LIST_UNRESOLVED = 'LIST_UNRESOLVED'
    LIST_LATEST = 'LIST_LATEST'
    DELETE_RESOLVED = 'DELETE_RESOLVED'
