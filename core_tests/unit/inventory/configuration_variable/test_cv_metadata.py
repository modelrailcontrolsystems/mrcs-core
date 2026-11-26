"""
Created on 26 Nov 2026

@author: Bruno Beloff (bbeloff@me.com)

python -m unittest -v unit/inventory/configuration_variable/test_cv_metadata.py

https://realpython.com/python-testing/
https://www.jetbrains.com/help/pycharm/creating-tests.html
"""

import unittest

from mrcs_core.inventory.configuration_variable.cv_address import CVAddress
from mrcs_core.inventory.configuration_variable.cv_metadata import CVMetadata
from mrcs_core.inventory.manufacturer.manufacturer import Manufacturer


# --------------------------------------------------------------------------------------------------------------------

class TestCVMetaData(unittest.TestCase):

    def test_cv_metadata_find_numeric(self):
        obj1 = CVMetadata.find(CVAddress.SHORT_ADDRESS)
        self.assertEqual('CVMetadata:{cv_type_name:NumericCV, may_read:ALL{0}, may_write:ALL{0}}', str(obj1))


    def test_cv_metadata_find_manufacturer(self):
        obj1 = CVMetadata.find(CVAddress.MANUFACTURER_ID)
        self.assertEqual('CVMetadata:{cv_type_name:ManufacturerCV, may_read:ALL{0}, may_write:None}', str(obj1))


    def test_cv_metadata_find_consist(self):
        obj1 = CVMetadata.find(CVAddress.CONSIST_ADDRESS)
        self.assertEqual('CVMetadata:{cv_type_name:ConsistCV, may_read:ALL{0}, may_write:ALL{0}}', str(obj1))


    def test_cv_metadata_find_railcom(self):
        obj1 = CVMetadata.find(CVAddress.RAILCOM)
        self.assertEqual('CVMetadata:{cv_type_name:RailcomCV, may_read:ALL{0}, may_write:ALL{0}}', str(obj1))


    def test_cv_metadata_find_configuration(self):
        obj1 = CVMetadata.find(CVAddress.CONFIGURATION)
        self.assertEqual('CVMetadata:{cv_type_name:ConfigurationCV, may_read:ALL{0}, may_write:ALL{0}}', str(obj1))


    def test_cv_metadata_find_esu(self):
        obj1 = CVMetadata.find(CVAddress.ESU_CONTROL_VOLTAGE)
        self.assertEqual('CVMetadata:{cv_type_name:NumericCV, may_read:ELECTRONIC_SOLUTIONS_ULM_GMBH{151}, '
                         'may_write:ELECTRONIC_SOLUTIONS_ULM_GMBH{151}}', str(obj1))


    def test_cv_metadata_find_zimo(self):
        obj1 = CVMetadata.find(CVAddress.ZIMO_MASTER_VOLUME)
        self.assertEqual('CVMetadata:{cv_type_name:NumericCV, may_read:ZIMO_ELEKTRONIK{145}, '
                         'may_write:ZIMO_ELEKTRONIK{145}}', str(obj1))


    # ----------------------------------------------------------------------------------------------------------------

    def test_cv_may_be_read_by_all_none(self):
        obj1 = CVMetadata.find(CVAddress.SHORT_ADDRESS)
        may_read = obj1.may_be_read_from(None)
        self.assertTrue(may_read)


    def test_cv_may_be_read_by_all_zimo(self):
        obj1 = CVMetadata.find(CVAddress.SHORT_ADDRESS)
        may_read = obj1.may_be_read_from(Manufacturer.ZIMO_ELEKTRONIK)
        self.assertTrue(may_read)


    def test_cv_may_be_read_by_zimo_none(self):
        obj1 = CVMetadata.find(CVAddress.ZIMO_MASTER_VOLUME)
        may_read = obj1.may_be_read_from(None)
        self.assertFalse(may_read)


    def test_cv_may_be_read_by_zimo_esu(self):
        obj1 = CVMetadata.find(CVAddress.ZIMO_MASTER_VOLUME)
        may_read = obj1.may_be_read_from(Manufacturer.ELECTRONIC_SOLUTIONS_ULM_GMBH)
        self.assertFalse(may_read)


    def test_cv_may_be_read_by_zimo_zimo(self):
        obj1 = CVMetadata.find(CVAddress.ZIMO_MASTER_VOLUME)
        may_read = obj1.may_be_read_from(Manufacturer.ZIMO_ELEKTRONIK)
        self.assertTrue(may_read)


    def test_cv_may_be_written_by_all_none(self):
        obj1 = CVMetadata.find(CVAddress.SHORT_ADDRESS)
        may_read = obj1.may_be_written_to(None)
        self.assertTrue(may_read)


    def test_cv_may_be_written_by_all_zimo(self):
        obj1 = CVMetadata.find(CVAddress.SHORT_ADDRESS)
        may_read = obj1.may_be_written_to(Manufacturer.ZIMO_ELEKTRONIK)
        self.assertTrue(may_read)


    def test_cv_may_be_written_by_zimo_none(self):
        obj1 = CVMetadata.find(CVAddress.ZIMO_MASTER_VOLUME)
        may_read = obj1.may_be_written_to(None)
        self.assertFalse(may_read)


    def test_cv_may_be_written_by_zimo_esu(self):
        obj1 = CVMetadata.find(CVAddress.ZIMO_MASTER_VOLUME)
        may_read = obj1.may_be_written_to(Manufacturer.ELECTRONIC_SOLUTIONS_ULM_GMBH)
        self.assertFalse(may_read)


    def test_cv_may_be_written_by_zimo_zimo(self):
        obj1 = CVMetadata.find(CVAddress.ZIMO_MASTER_VOLUME)
        may_read = obj1.may_be_written_to(Manufacturer.ZIMO_ELEKTRONIK)
        self.assertTrue(may_read)


    def test_cv_may_be_written_by_none_none(self):
        obj1 = CVMetadata.find(CVAddress.MANUFACTURER_ID)
        may_read = obj1.may_be_written_to(None)
        self.assertFalse(may_read)


    def test_cv_may_be_written_by_none_esu(self):
        obj1 = CVMetadata.find(CVAddress.MANUFACTURER_ID)
        may_read = obj1.may_be_written_to(Manufacturer.ELECTRONIC_SOLUTIONS_ULM_GMBH)
        self.assertFalse(may_read)


    def test_cv_may_be_written_by_none_zimo(self):
        obj1 = CVMetadata.find(CVAddress.MANUFACTURER_ID)
        may_read = obj1.may_be_written_to(Manufacturer.ZIMO_ELEKTRONIK)
        self.assertFalse(may_read)


# --------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    unittest.main()
