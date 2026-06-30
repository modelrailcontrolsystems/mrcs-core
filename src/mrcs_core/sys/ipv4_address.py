"""
Created on 2 Mar 2020

@author: Bruno Beloff (bbeloff@me.com)

"192.168.1.111"
"""
from typing import List


# --------------------------------------------------------------------------------------------------------------------

class IPv4Address(object):
    """
    classdocs
    """


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def is_valid(cls, dot_decimal):
        try:
            octets = [int(octet) for octet in dot_decimal.split('.') if 0 <= int(octet) <= 255]
        except (TypeError, ValueError):
            return False

        if len(octets) != 4:
            return False

        return True


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct(cls, dot_decimal):
        if dot_decimal is None:
            return None

        octets = [int(octet) for octet in dot_decimal.split('.')]

        return cls(octets)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, octets: List[int]):
        """
        Constructor
        """
        self.__octets = octets


    def __eq__(self, other):
        try:
            return self.dot_decimal == other.dot_decimal
        except (AttributeError, TypeError):
            return False


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def dot_decimal(self):
        return '.'.join([str(octet) for octet in self.__octets])


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "IPv4Address:{%s}" % self.dot_decimal
