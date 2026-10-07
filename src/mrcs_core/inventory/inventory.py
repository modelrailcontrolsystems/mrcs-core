"""
Created on 4 Oct 2026

@author: Bruno Beloff (bbeloff@me.com)

A persistent ordered collection of MPUs (later with other rolling stock)

Business logic is implemented in the abstract superclass InventoryNavigator, with object lifecycle functions
implemented here.
"""

from collections import OrderedDict
from typing import Any

from mrcs_core.data.json import MultiPersistentJSONable
from mrcs_core.inventory.inventory_navigator import InventoryNavigator
from mrcs_core.inventory.motive_power_unit.mpu import MPU


# --------------------------------------------------------------------------------------------------------------------

class Inventory(InventoryNavigator, MultiPersistentJSONable):
    """
    A persistent ordered collection of MPUs
    """

    __FILENAME = "inventory.json"


    @classmethod
    def persistence_location(cls, name):
        filename = cls.__FILENAME if name is None else '_'.join((name, cls.__FILENAME))
        return cls.inventory_dir(), filename


    @classmethod
    def construct_from_jdict(cls, jdict, name=None) -> Inventory:
        label = jdict.get('label')
        description = jdict.get('description')

        mpus = OrderedDict()
        for mpu_jdict in jdict.get('mpus', []):
            mpu = MPU.construct_from_jdict(mpu_jdict)  # TODO: check for duplicate labels
            mpus[mpu.label] = mpu

        return cls(label, description, mpus, name=name)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, label: str, description: str, mpus: OrderedDict[str, MPU], name=None):
        InventoryNavigator.__init__(self, mpus)
        MultiPersistentJSONable.__init__(self, name)

        self.__label = label
        self.__description = description


    def __eq__(self, other: Any):
        try:
            return self.label == other.label and self.description == other.description and self.mpus == other.mpus
        except (AttributeError, TypeError):
            return False


    def __lt__(self, other: Any):
        return self.label < other.label


    # ----------------------------------------------------------------------------------------------------------------


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        jdict = OrderedDict()

        jdict['label'] = self.label
        jdict['description'] = self.description
        jdict['mpus'] = self.mpus

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def label(self):
        return self.__label


    @property
    def description(self):
        return self.__description


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        mpus = '[' + ', '.join([str(mpu) for mpu in self.mpus]) + ']'

        return (f'Inventory:{{name:{self.name}, label:{self.label}, description:{self.description}, '
                f'mpus:{mpus}}}')
