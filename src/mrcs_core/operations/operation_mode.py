"""
Created on 16 Nov 2025

@author: Bruno Beloff (bbeloff@me.com)

A gathering-together of service operation modes

https://stackoverflow.com/questions/37678418/python-enums-with-complex-types
"""

from enum import unique, Enum

from mrcs_core.db.dbclient import DBMode
from mrcs_core.messaging.broker import Broker


# --------------------------------------------------------------------------------------------------------------------

class OperationService(object):
    """
    A gathering-together of service operation modes
    """

    def __init__(self, db_mode: DBMode, broker_exchange: Broker.Exchange):
        self.__db_mode = db_mode
        self.__broker_exchange = broker_exchange


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def db_mode(self):
        return self.__db_mode


    @property
    def broker_exchange(self):
        return self.__broker_exchange


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return f'OperationService:{{db_mode:{self.db_mode}, broker_exchange:{self.broker_exchange}}}'


# --------------------------------------------------------------------------------------------------------------------

@unique
class OperationMode(Enum):
    """
    An enumeration of all the possible operation modes
    """

    TEST = OperationService(DBMode.TEST, Broker.Exchange.TEST)
    LIVE = OperationService(DBMode.LIVE, Broker.Exchange.OPERATIONS)

    @classmethod
    def keys(cls):
        return cls.__members__.keys()

