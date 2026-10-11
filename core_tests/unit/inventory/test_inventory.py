"""
Created on 11 Oct 2026

@author: Bruno Beloff (bbeloff@me.com)

python -m unittest -v unit/inventory/test_inventory.py

https://realpython.com/python-testing/
https://www.jetbrains.com/help/pycharm/creating-tests.html
"""

import json
import unittest
from collections import OrderedDict
from pathlib import Path

from mrcs_core.data.json import JSONify
from mrcs_core.inventory.configuration_variable.cv_address import CVAddress
from mrcs_core.inventory.configuration_variable.numeric_cv import NumericCV
from mrcs_core.inventory.inventory import Inventory
from mrcs_core.inventory.motive_power_unit.mpu import MPU


# --------------------------------------------------------------------------------------------------------------------

class TestInventory(unittest.TestCase):
    __inventory_filename = Path(__file__).parent / 'data' / 'test_001_inventory.json'
    __inventory_jdict = None


    @classmethod
    def setUpClass(cls):
        with open(cls.__inventory_filename) as fp:
            cls.__inventory_jdict = json.load(fp)


    @classmethod
    def __sample_mpu_1(cls):
        cv1 = NumericCV(CVAddress.ACCELERATION, 5)
        cv2 = NumericCV(CVAddress.DECELERATION, 9)
        cvs = OrderedDict({cv1.cv_address: cv1, cv2.cv_address: cv2})
        return MPU('DB59', 5, 'DB Schenker', '59', '59201', 'Revolution Trains', 145, cvs)


    @classmethod
    def __sample_mpu_2(cls):
        return MPU('GBRF66', 6, 'GB Railfreight', '66', '66701', 'Hornby', 135, OrderedDict())


    # Persistence location -------------------------------------------------------------------------------------------

    def test_inventory_persistence_location(self):
        self.assertEqual(('inventory', 'inventory.json'), Inventory.persistence_location(None))
        self.assertEqual(('inventory', 'test_001_inventory.json'), Inventory.persistence_location('test_001'))


    # Construction & properties --------------------------------------------------------------------------------------

    def test_inventory_construct(self):
        mpu1 = self.__sample_mpu_1()
        mpu2 = self.__sample_mpu_2()
        mpus = OrderedDict({mpu1.label: mpu1, mpu2.label: mpu2})

        inventory = Inventory('INV001', 'Test inventory 001', mpus, name='test_001')
        self.assertEqual('test_001', inventory.name)
        self.assertEqual('INV001', inventory.label)
        self.assertEqual('Test inventory 001', inventory.description)
        self.assertEqual((mpu1, mpu2), inventory.mpus)


    def test_inventory_construct_from_jdict(self):
        inventory = Inventory.construct_from_jdict(self.__inventory_jdict, name='test_001')

        self.assertEqual('test_001', inventory.name)
        self.assertEqual('INV001', inventory.label)
        self.assertEqual('Test inventory 001', inventory.description)
        self.assertEqual(2, len(inventory.mpus))
        self.assertEqual(('DB59', 'GBRF66'), tuple(mpu.label for mpu in inventory.mpus))
        self.assertEqual((self.__sample_mpu_1(), self.__sample_mpu_2()), inventory.mpus)


    def test_inventory_construct_from_jdict_none_or_empty(self):
        inventory = Inventory.construct_from_jdict({})
        self.assertIsNone(inventory.name)
        self.assertIsNone(inventory.label)
        self.assertIsNone(inventory.description)
        self.assertEqual((), inventory.mpus)


    def test_inventory_construct_from_jdict_duplicate_mpu(self):
        jdict = dict(self.__inventory_jdict)
        jdict['mpus'] = [self.__inventory_jdict['mpus'][0], self.__inventory_jdict['mpus'][0]]

        with self.assertRaises(ValueError):
            Inventory.construct_from_jdict(jdict)


    # Equality & comparison ------------------------------------------------------------------------------------------

    def test_inventory_eq(self):
        inventory1 = Inventory.construct_from_jdict(self.__inventory_jdict, name='test_001')
        inventory2 = Inventory.construct_from_jdict(self.__inventory_jdict, name='test_001')
        self.assertEqual(inventory1, inventory2)

        mpus = OrderedDict({mpu.label: mpu for mpu in inventory1.mpus})

        inventory_diff_label = Inventory('OTHER', inventory1.description, mpus)
        self.assertNotEqual(inventory1, inventory_diff_label)

        inventory_diff_desc = Inventory(inventory1.label, 'Other description', mpus)
        self.assertNotEqual(inventory1, inventory_diff_desc)

        mpu1 = inventory1.mpus[0]
        inventory_diff_mpus = Inventory(inventory1.label, inventory1.description, OrderedDict({mpu1.label: mpu1}))
        self.assertNotEqual(inventory1, inventory_diff_mpus)

        inventory_no_mpus = Inventory(inventory1.label, inventory1.description, OrderedDict())
        self.assertNotEqual(inventory1, inventory_no_mpus)

        self.assertNotEqual(inventory1, None)
        self.assertNotEqual(inventory1, 'INV001')


    def test_inventory_lt(self):
        inventory1 = Inventory('INV001', 'Desc', OrderedDict())
        inventory2 = Inventory('INV002', 'Desc', OrderedDict())

        self.assertTrue(inventory1 < inventory2)
        self.assertFalse(inventory2 < inventory1)
        self.assertFalse(inventory1 < inventory1)


    # MPU abstract ---------------------------------------------------------------------------------------------------

    def test_inventory_mpu_abstract(self):
        inventory = Inventory.construct_from_jdict(self.__inventory_jdict)
        abstract = inventory.mpu_abstract()

        self.assertEqual(2, len(abstract))
        self.assertEqual([mpu.mpu_status() for mpu in inventory.mpus], abstract.items)


    # String representation & serialization --------------------------------------------------------------------------

    def test_inventory_str(self):
        self.maxDiff = None
        inventory = Inventory.construct_from_jdict(self.__inventory_jdict, name='test_001')

        expected = ('Inventory:{name:test_001, label:INV001, description:Test inventory 001, mpus:[MPU:{label:DB59, '
                    'address:5, operator:DB Schenker, mpu_class:59, number:59201, vendor:Revolution Trains, '
                    'length:145, cvs:[NumericCV{cv_address:ACCELERATION{3}, value:5}, '
                    'NumericCV{cv_address:DECELERATION{4}, value:9}]}, MPU:{label:GBRF66, address:6, '
                    'operator:GB Railfreight, mpu_class:66, number:66701, vendor:Hornby, length:135, cvs:[]}]}')
        self.assertEqual(expected, str(inventory))


    def test_inventory_as_json(self):
        inventory = Inventory.construct_from_jdict(self.__inventory_jdict)
        jdict = inventory.as_json()

        self.assertEqual('INV001', jdict['label'])
        self.assertEqual('Test inventory 001', jdict['description'])
        self.assertEqual(inventory.mpus, jdict['mpus'])


    def test_inventory_jstr(self):
        inventory = Inventory.construct_from_jdict(self.__inventory_jdict)
        jstr = JSONify.dumps(inventory)
        inventory_deserialized = Inventory.construct_from_jdict(json.loads(jstr))

        self.assertEqual(inventory, inventory_deserialized)
        self.assertEqual(inventory.mpus, inventory_deserialized.mpus)


# --------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    unittest.main()
