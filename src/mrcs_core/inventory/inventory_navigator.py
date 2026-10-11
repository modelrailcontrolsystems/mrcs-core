"""
Created on 4 Oct 2026

@author: Bruno Beloff (bbeloff@me.com)

An ordered collection of MPUs

The InventoryNavigator structure separates the business logic - implemented here - from the object lifecycle functions
implemented by the Inventory class.
"""

from abc import ABC
from collections import OrderedDict

from mrcs_core.inventory.motive_power_unit.mpu import MPU
from mrcs_core.inventory.motive_power_unit.mpu_abstract import MPUAbstract


# --------------------------------------------------------------------------------------------------------------------

class InventoryNavigator(ABC):
    """
    An ordered collection of MPUs
    """


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, mpus: OrderedDict[str, MPU]):
        self.__mpus = mpus


    # ----------------------------------------------------------------------------------------------------------------

    def validate(self) -> None:
        pass


    # ----------------------------------------------------------------------------------------------------------------

    def mpu_abstract(self) -> MPUAbstract:
        mpu_statuses = [mpu.mpu_status() for mpu in self.mpus]
        return MPUAbstract(mpu_statuses)


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def mpus(self):
        return tuple(self.__mpus.values())
