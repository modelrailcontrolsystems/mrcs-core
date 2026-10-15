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
        # TODO: implement validate() - unique addresses
        pass


    # ----------------------------------------------------------------------------------------------------------------

    def mpu_abstract(self) -> MPUAbstract:
        mpu_statuses = [mpu.mpu_status() for mpu in self.mpus]
        return MPUAbstract(mpu_statuses)


    def mpu_report(self, mpu_label: str | None) -> list[MPU]:
        if mpu_label is None:
            return list(self.mpus)

        mpu = self.__mpus[mpu_label]  # may raise KeyError

        try:
            return [mpu]
        except KeyError:
            raise KeyError(mpu_label)


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def mpus(self):
        return tuple(self.__mpus.values())


    def mpu(self, label: str):
        try:
            return self.__mpus[label]
        except KeyError:
            return None
