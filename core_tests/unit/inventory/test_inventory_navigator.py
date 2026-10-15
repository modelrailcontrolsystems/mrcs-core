"""
Created on 11 Oct 2026

@author: Bruno Beloff (bbeloff@me.com)

python -m unittest -v unit/inventory/test_inventory_navigator.py

https://realpython.com/python-testing/
https://www.jetbrains.com/help/pycharm/creating-tests.html
"""

import json
import unittest
from collections import OrderedDict
from pathlib import Path as FilePath

from mrcs_core.equipment.motive_power_unit.mpu_enums import MPUDirection
from mrcs_core.equipment.motive_power_unit.mpu_functions import MPUFunctions
from mrcs_core.equipment.motive_power_unit.mpu_status import MPUStatus
from mrcs_core.inventory.inventory import Inventory
from mrcs_core.inventory.inventory_navigator import InventoryNavigator
from mrcs_core.inventory.motive_power_unit.mpu import MPU


# --------------------------------------------------------------------------------------------------------------------

class _DummyInventoryNavigator(InventoryNavigator):
    """
    a concrete InventoryNavigator, without the Inventory persistence machinery
    """

    pass


# --------------------------------------------------------------------------------------------------------------------

class TestInventoryNavigator(unittest.TestCase):
    __data_dir = FilePath(__file__).parent / 'data'

    __inventory = None


    @classmethod
    def setUpClass(cls):
        with open(cls.__data_dir / 'test_001_inventory.json') as fp:
            cls.__inventory = Inventory.construct_from_jdict(json.load(fp), name='test_001')


    # fixtures -------------------------------------------------------------------------------------------------------

    @staticmethod
    def __mpu(label, address):
        return MPU(label, address, 'Operator', '00', '00000', 'Vendor', 100, OrderedDict())


    @staticmethod
    def __navigator(*mpus):
        return _DummyInventoryNavigator(OrderedDict((mpu.label, mpu) for mpu in mpus))


    @staticmethod
    def __status(label, address):
        return MPUStatus(label, address, MPUFunctions([]), None, None, MPUDirection.UNKNOWN)


    # validate -------------------------------------------------------------------------------------------------------

    def test_validate(self):
        self.__inventory.validate()


    def test_validate_minimal(self):
        self.__navigator(self.__mpu('M01', 1)).validate()


    def test_validate_empty(self):
        self.__navigator().validate()


    def test_validate_duplicate_address(self):
        # the second MPU with a given address is the one reported
        navigator = self.__navigator(self.__mpu('M01', 1), self.__mpu('M02', 2), self.__mpu('M03', 1))

        with self.assertRaises(ValueError) as context:
            navigator.validate()

        self.assertEqual("Duplicate MPU address 1 in M03.", str(context.exception))


    # mpus -----------------------------------------------------------------------------------------------------------

    def test_mpus(self):
        self.assertEqual(('DB59', 'GBRF66'), tuple(mpu.label for mpu in self.__inventory.mpus))


    def test_mpus_ordered(self):
        # insertion order is preserved, not sorted
        mpu1 = self.__mpu('M02', 2)
        mpu2 = self.__mpu('M01', 1)

        self.assertEqual((mpu1, mpu2), self.__navigator(mpu1, mpu2).mpus)


    def test_mpus_empty(self):
        self.assertEqual((), self.__navigator().mpus)


    # mpu_abstract ---------------------------------------------------------------------------------------------------

    def test_mpu_abstract(self):
        abstract = self.__inventory.mpu_abstract()

        self.assertEqual(2, len(abstract))
        self.assertEqual(['DB59', 'GBRF66'], [status.label for status in abstract.items])
        self.assertEqual([5, 6], [status.mpu_address for status in abstract.items])


    def test_mpu_abstract_status(self):
        abstract = self.__navigator(self.__mpu('M01', 1), self.__mpu('M02', 2)).mpu_abstract()

        self.assertEqual([self.__status('M01', 1), self.__status('M02', 2)], abstract.items)


    def test_mpu_abstract_empty(self):
        abstract = self.__navigator().mpu_abstract()

        self.assertEqual(0, len(abstract))
        self.assertEqual([], abstract.items)


# --------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    unittest.main()
