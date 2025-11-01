"""
Created on 1 Nov 2025

@author: Bruno Beloff (bbeloff@me.com)

A structured representation of a messaging topic

https://www.rabbitmq.com/tutorials/tutorial-five-python
"""

from mrcs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class RoutingKey(JSONable):
    """
    classdocs
    """

    @staticmethod
    def is_valid(routing):
        pieces = routing.split('.')

        if len(pieces) != 3:
            return False

        for piece in pieces:
            if len(piece) < 1:
                return False

        return True


    @classmethod
    def construct(cls, routing):
        if not routing:
            return None

        if not cls.is_valid(routing):
            raise ValueError(routing)

        pieces = routing.split('.')

        source = pieces[0]
        sector = pieces[1]
        device = pieces[2]

        return cls(source, sector, device)


    @classmethod
    def construct_for_all(cls):
        return cls('*', '*', '*')


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, source, sector, device):
        """
        Constructor
        """
        super().__init__()

        self.__source = source                          # string
        self.__sector = sector                          # string
        self.__device = device                          # string


    def __lt__(self, other):
        if self.source < other.source:
            return True

        if self.source > other.source:
            return False

        if self.sector < other.sector:
            return True

        if self.sector > other.sector:
            return False

        if self.device < other.device:
            return True

        return False


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        return str(self)


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def source(self):
        return self.__source


    @property
    def sector(self):
        return self.__sector


    @property
    def device(self):
        return self.__device


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return f'{self.source}.{self.sector}.{self.device}'
