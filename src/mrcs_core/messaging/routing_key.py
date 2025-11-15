"""
Created on 1 Nov 2025

@author: Bruno Beloff (bbeloff@me.com)

A structured representation of a message routing key, with source and target

VIS.001.001.MPU.001.*
"""

import re
from abc import ABC

from mrcs_core.data.equipment_identity import EquipmentIdentifier, EquipmentFilter, EquipmentSpecification
from mrcs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class RoutingKey(JSONable, ABC):
    """
    An abstract routing key
    """


    @staticmethod
    def is_valid(routing):
        return re.match(r'[A-Z*]+\.[0-9*\-]+\.[0-9*]+.[A-Z*]+\.[0-9*\-]+\.[0-9*]+', routing)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, source: EquipmentSpecification, target: EquipmentSpecification):
        super().__init__()

        self.__source = source  # EquipmentIdentifier | EquipmentFilter
        self.__target = target  # EquipmentFilter


    def __eq__(self, other):
        try:
            return self.source == other.source and self.target == other.target
        except (AttributeError, TypeError):
            return False


    def __lt__(self, other):
        if self.source < other.source:
            return True

        if self.source > other.source:
            return False

        return self.target < other.target


    # ----------------------------------------------------------------------------------------------------------------

    def matches(self, other):
        try:
            return self.source.matches(other.source) and self.target.matches(other.target)
        except (AttributeError, TypeError):
            return False


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        return '.'.join([self.source.as_json(**kwargs), self.target.as_json(**kwargs)])


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def source(self):
        return self.__source


    @property
    def target(self):
        return self.__target


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return f'{self.__class__.__name__}:{{source:{self.source}, target:{self.target}}}'


# --------------------------------------------------------------------------------------------------------------------

class PublicationRoutingKey(RoutingKey):
    """
    A routing key for a publisher, with a fully-specified source
    """

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        if not cls.is_valid(jdict):
            raise ValueError(jdict)

        pieces = jdict.split('.')

        source = EquipmentIdentifier.construct_from_jdict('.'.join(pieces[:3]))
        target = EquipmentFilter.construct_from_jdict('.'.join(pieces[3:]))

        return cls(source, target)


    @classmethod
    def construct_from_db(cls, field):
        pieces = field.split('.')

        source = EquipmentIdentifier.construct_from_jdict('.'.join(pieces[:3]))
        target = EquipmentFilter.construct_from_jdict('.'.join(pieces[3:]))

        return cls(source, target)


# --------------------------------------------------------------------------------------------------------------------

class SubscriptionRoutingKey(RoutingKey):
    """
    A routing key for a subscriber, with a partially-specified source
    """

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        if not cls.is_valid(jdict):
            raise ValueError(jdict)

        pieces = jdict.split('.')

        source = EquipmentFilter.construct_from_jdict('.'.join(pieces[:3]))
        target = EquipmentFilter.construct_from_jdict('.'.join(pieces[3:]))

        return cls(source, target)
