"""
Created on 4 Oct 2026

@author: Bruno Beloff (bbeloff@me.com)

An ordered collection of Blocks and Platforms, making up a complete layout

The LayoutNavigator structure separates the business logic - implemented here - from the object lifecycle functions
implemented by the Layout class.
"""

from abc import ABC
from collections import OrderedDict

from mrcs_core.inventory.motive_power_unit.mpu import MPU
from mrcs_core.inventory.motive_power_unit.mpu_abstract import MPUAbstract


# --------------------------------------------------------------------------------------------------------------------

class InventoryNavigator(ABC):
    """
    An ordered collection of Blocks and Stations, making up a complete layout
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
