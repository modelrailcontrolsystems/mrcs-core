"""
Created on 16 Oct 2026

@author: Bruno Beloff (bbeloff@me.com)

python -m unittest -v unit/equipment/test_equipment_enums.py

https://realpython.com/python-testing/
https://www.jetbrains.com/help/pycharm/creating-tests.html
"""

import unittest

from mrcs_core.equipment.equipment_enums import CLK, CLU, CRT, EquipmentType


# --------------------------------------------------------------------------------------------------------------------

class TestEquipmentType(unittest.TestCase):

    def test_keys(self):
        self.assertEqual(['API', 'CLK', 'CRT', 'REC', 'CLU', 'TST',
                          'DCP', 'LGP', 'LVL', 'MPU', 'SCH', 'SIG', 'TEL', 'TRK', 'TRS',
                          'BOS', 'LID', 'VIS'], list(EquipmentType.keys()))


    def test_items(self):
        self.assertEqual(list(EquipmentType), EquipmentType.items())


    def test_values(self):
        # every value is the same as its name
        for member in EquipmentType:
            self.assertEqual(member.name, member.value)


    def test_construct(self):
        self.assertEqual(EquipmentType.BOS, EquipmentType('BOS'))

        with self.assertRaises(ValueError):
            EquipmentType('XXX')


    def test_contains(self):
        self.assertTrue('BOS' in EquipmentType)
        self.assertFalse('XXX' in EquipmentType)
        self.assertFalse('bos' in EquipmentType)


    def test_str(self):
        self.assertEqual('BOS', str(EquipmentType.BOS))


    def test_eq(self):
        self.assertEqual('BOS', EquipmentType.BOS)
        self.assertNotEqual(EquipmentType.BOS, EquipmentType.LID)


    def test_lt(self):
        self.assertTrue(EquipmentType.API < EquipmentType.VIS)
        self.assertFalse(EquipmentType.VIS < EquipmentType.API)
        self.assertFalse(EquipmentType.BOS < EquipmentType.BOS)


    def test_sorted(self):
        # sorted by value, not by declaration order
        self.assertEqual([EquipmentType.BOS, EquipmentType.CLK, EquipmentType.CLU, EquipmentType.CRT],
                         sorted([EquipmentType.CRT, EquipmentType.CLU, EquipmentType.CLK, EquipmentType.BOS]))


# --------------------------------------------------------------------------------------------------------------------

class TestCLU(unittest.TestCase):

    def test_keys(self):
        self.assertEqual(['SUBSCRIBER', 'COMMANDER', 'LAYOUT_MANAGER', 'INVENTORY_MANAGER'], list(CLU.keys()))


    def test_items(self):
        # declaration order, not value order
        self.assertEqual([CLU.SUBSCRIBER, CLU.COMMANDER, CLU.LAYOUT_MANAGER, CLU.INVENTORY_MANAGER], CLU.items())


    def test_values(self):
        self.assertEqual([1, 2, 4, 3], [member.value for member in CLU])


    def test_construct(self):
        self.assertEqual(CLU.INVENTORY_MANAGER, CLU(3))

        with self.assertRaises(ValueError):
            CLU(99)


    def test_contains(self):
        self.assertTrue(4 in CLU)
        self.assertFalse(99 in CLU)
        self.assertFalse('SUBSCRIBER' in CLU)


    def test_str(self):
        self.assertEqual('SUBSCRIBER{1}', str(CLU.SUBSCRIBER))
        self.assertEqual('LAYOUT_MANAGER{4}', str(CLU.LAYOUT_MANAGER))


    def test_int(self):
        self.assertEqual(3, int(CLU.INVENTORY_MANAGER))
        self.assertEqual(CLU.COMMANDER, 2)


    def test_lt(self):
        self.assertTrue(CLU.INVENTORY_MANAGER < CLU.LAYOUT_MANAGER)
        self.assertFalse(CLU.LAYOUT_MANAGER < CLU.INVENTORY_MANAGER)


# --------------------------------------------------------------------------------------------------------------------

class TestCLK(unittest.TestCase):

    def test_keys(self):
        self.assertEqual(['CRON', 'CRONTAB', 'CLOCK_CONF', 'CLOCK_MANAGER'], list(CLK.keys()))


    def test_items(self):
        self.assertEqual([CLK.CRON, CLK.CRONTAB, CLK.CLOCK_CONF, CLK.CLOCK_MANAGER], CLK.items())


    def test_values(self):
        self.assertEqual([1, 2, 3, 4], [member.value for member in CLK])


    def test_construct(self):
        self.assertEqual(CLK.CLOCK_CONF, CLK(3))

        with self.assertRaises(ValueError):
            CLK(99)


    def test_contains(self):
        self.assertTrue(1 in CLK)
        self.assertFalse(99 in CLK)
        self.assertFalse('CRON' in CLK)


    def test_str(self):
        self.assertEqual('CRON{1}', str(CLK.CRON))
        self.assertEqual('CLOCK_MANAGER{4}', str(CLK.CLOCK_MANAGER))


    def test_int(self):
        self.assertEqual(2, int(CLK.CRONTAB))
        self.assertEqual(CLK.CLOCK_MANAGER, 4)


    def test_lt(self):
        self.assertTrue(CLK.CRON < CLK.CLOCK_MANAGER)
        self.assertFalse(CLK.CLOCK_MANAGER < CLK.CRON)


# --------------------------------------------------------------------------------------------------------------------

class TestCRT(unittest.TestCase):

    def test_keys(self):
        self.assertEqual(['ROUTER', 'UNCLASSIFIED', 'COMMON',
                          'SYSTEM', 'TRACK', 'TURNOUT', 'BLOCK', 'SIGNAL', 'MPU'], list(CRT.keys()))


    def test_items(self):
        self.assertEqual([CRT.ROUTER, CRT.UNCLASSIFIED, CRT.COMMON,
                          CRT.SYSTEM, CRT.TRACK, CRT.TURNOUT, CRT.BLOCK, CRT.SIGNAL, CRT.MPU], CRT.items())


    def test_values(self):
        self.assertEqual([1, 2, 3, 4, 5, 6, 7, 8, 9], [member.value for member in CRT])


    def test_construct(self):
        self.assertEqual(CRT.TURNOUT, CRT(6))

        with self.assertRaises(ValueError):
            CRT(99)


    def test_contains(self):
        self.assertTrue(9 in CRT)
        self.assertFalse(99 in CRT)
        self.assertFalse('ROUTER' in CRT)


    def test_str(self):
        self.assertEqual('ROUTER{1}', str(CRT.ROUTER))
        self.assertEqual('MPU{9}', str(CRT.MPU))


    def test_int(self):
        self.assertEqual(7, int(CRT.BLOCK))
        self.assertEqual(CRT.SIGNAL, 8)


    def test_lt(self):
        self.assertTrue(CRT.ROUTER < CRT.MPU)
        self.assertFalse(CRT.MPU < CRT.ROUTER)


# --------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    unittest.main()
