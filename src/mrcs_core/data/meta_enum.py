"""
Created on 22 Nov 2025

@author: Bruno Beloff (bbeloff@me.com)

https://stackoverflow.com/questions/63335753/how-to-check-if-string-exists-in-enum-of-strings
"""

from enum import EnumMeta


# --------------------------------------------------------------------------------------------------------------------

class MetaEnum(EnumMeta):
    def __contains__(cls, item):
        try:
            cls(item)
        except ValueError:
            return False
        return True


    def keys(cls):
        return cls.__members__.keys()
