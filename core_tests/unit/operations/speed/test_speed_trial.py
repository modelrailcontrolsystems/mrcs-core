"""
Created on 25 Oct 2025

@author: Bruno Beloff (bbeloff@me.com)

python -m unittest -v unit/operations/speed/test_speed_trial.py

https://realpython.com/python-testing/
https://www.jetbrains.com/help/pycharm/creating-tests.html
https://stackoverflow.com/questions/8047736/how-to-load-data-from-a-file-for-a-unit-test-in-python
"""

import json
import os
import unittest
from pathlib import Path

from mrcs_core.data.csv import CSV
from mrcs_core.data.iso_datetime import ISODatetime
from mrcs_core.data.json import JSONify
from mrcs_core.equipment.block.block_enums import BlockHeading
from mrcs_core.operations.speed.speed_run import SpeedRun
from mrcs_core.operations.speed.speed_trial import SpeedTrial
from mrcs_core.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

class TestSpeedTrial(unittest.TestCase):

    @classmethod
    def __test_dir(cls):
        return os.path.join(Host.mrcs_abs_dir(), Host.test_dir())


    @classmethod
    def __test_abs_filename(cls):
        return os.path.join(cls.__test_dir(), 'test_TEST00_BS05.csv')


    @classmethod
    def __test_ref_filename(cls):
        return Path(__file__).parent / 'data' / 'test_TEST00_BS05.csv'


    @classmethod
    def setUpClass(cls):
        try:
            os.mkdir(cls.__test_dir())
        except FileExistsError:
            pass


    @classmethod
    def tearDownClass(cls):
        try:
            os.remove(cls.__test_abs_filename())
        except FileNotFoundError:
            pass


    @classmethod
    def __sample_run_1(cls):
        now = ISODatetime.construct_from_jdict('2026-10-25T08:55:38.234Z')
        return SpeedRun(500, BlockHeading.UP, 5, 12.125, 17.123, now)


    @classmethod
    def __sample_run_2(cls):
        now = ISODatetime.construct_from_jdict('2026-10-25T08:56:38.234Z')
        return SpeedRun(500, BlockHeading.UP, 15, 17.125, 10.123, now)


    @classmethod
    def __sample_run_3(cls):
        now = ISODatetime.construct_from_jdict('2026-10-25T08:56:38.234Z')
        return SpeedRun(500, BlockHeading.UP, 25, 27.125, 5.123, now)


    @classmethod
    def __sample_trial_1(cls):
        runs = [cls.__sample_run_1(), cls.__sample_run_2()]
        return SpeedTrial('TEST00', 'BS05', *runs)


    # ----------------------------------------------------------------------------------------------------------------

    def test_construct(self):
        obj1 = self.__sample_trial_1()
        self.assertEqual('SpeedTrial:{name:TEST00_BS05, mpu_label:TEST00, block_label:BS05, runs:['
                         'SpeedRun:{distance:500, direction:UP{1}, set_speed:5, average_reported_speed:12.1, '
                         'elapsed_time:17.123, test_time:ISODatetime:{2026-10-25T08:55:38.234+00:00}}, '
                         'SpeedRun:{distance:500, direction:UP{1}, set_speed:15, average_reported_speed:17.1, '
                         'elapsed_time:10.123, test_time:ISODatetime:{2026-10-25T08:56:38.234+00:00}}]}',
                         str(obj1))


    def test_add_run(self):
        obj1 = SpeedTrial('TEST00', 'BS05')
        obj1.add_run(self.__sample_run_3())
        self.assertEqual('SpeedTrial:{name:TEST00_BS05, mpu_label:TEST00, block_label:BS05, runs:['
                         'SpeedRun:{distance:500, direction:UP{1}, set_speed:25, average_reported_speed:27.1, '
                         'elapsed_time:5.123, test_time:ISODatetime:{2026-10-25T08:56:38.234+00:00}}]}',
                         str(obj1))


    def test_json(self):
        obj1 = self.__sample_trial_1()
        jstr = JSONify.dumps(obj1)
        self.assertEqual('{"mpu_label": "TEST00", "block_label": "BS05", "runs": ['
                         '{"distance": 500, "direction": "UP", "set": 5, "ars": 12.1, "elapsed": 17.123, '
                         '"test_time": "2026-10-25T08:55:38.234+00:00"}, '
                         '{"distance": 500, "direction": "UP", "set": 15, "ars": 17.1, "elapsed": 10.123, '
                         '"test_time": "2026-10-25T08:56:38.234+00:00"}]}',
                         jstr)


    def test_json_eq(self):
        obj1 = self.__sample_trial_1()
        jstr = JSONify.dumps(obj1)
        obj2 = SpeedTrial.construct_from_jdict(json.loads(jstr))
        self.assertTrue(obj1 == obj2)


    def test_persistence(self):
        obj1 = self.__sample_trial_1()
        obj1.save(Host)
        obj2 = SpeedTrial.load(Host, obj1.name)
        self.assertTrue(obj1 == obj2)


    def test_csv(self):
        abs_ref_filename = self.__test_ref_filename()
        abs_new_filename = self.__test_abs_filename()
        obj1 = self.__sample_trial_1()
        jdict = JSONify.as_jdict(obj1.runs)
        CSV.write(jdict, filename=abs_new_filename)

        f = open(abs_ref_filename)
        ref = f.readlines()
        f.close()

        f = open(abs_new_filename)
        new = f.readlines()
        f.close()

        self.assertEqual(ref, new)


# --------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    unittest.main()
