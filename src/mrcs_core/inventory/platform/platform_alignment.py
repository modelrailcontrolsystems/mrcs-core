"""
Created on 19 Sep 2026

@author: Bruno Beloff (bbeloff@me.com)

An enumeration of all the possible platform alignments

https://docs.python.org/3/howto/enum.html
"""

from enum import StrEnum, unique

from mrcs_core.data.meta_enum import MetaEnum


# --------------------------------------------------------------------------------------------------------------------

@unique
class PlatformAlignment(StrEnum, metaclass=MetaEnum):
    """
    An enumeration of all the possible platform alignments
    """

    UP_LEFT = 'LEFT'
    UP_RIGHT = 'RIGHT'
