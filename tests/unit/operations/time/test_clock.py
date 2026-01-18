"""
Created on 26 Dec 2025

@author: Bruno Beloff (bbeloff@me.com)

python -m unittest -v operations/test_clock.py

https://realpython.com/python-testing/
https://www.jetbrains.com/help/pycharm/creating-tests.html
https://stackoverflow.com/questions/8047736/how-to-load-data-from-a-file-for-a-unit-test-in-python
"""

import json
import time
import unittest

from datetime import timedelta

from mrcs_core.data.iso_datetime import ISODatetime
from mrcs_core.data.json import JSONify
from mrcs_core.operations.time.clock import Clock
from mrcs_core.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

class TestClockConf(unittest.TestCase):

    def test_construct(self):
        now = ISODatetime.now()
        obj1 = Clock.set(True, 4, 2020, 2, 4, 6)
        self.assertEqual(obj1.speed, 4)
        self.assertGreaterEqual(obj1.true_start - now, timedelta())
        self.assertLess(obj1.true_start - now, timedelta(milliseconds=0.1))


    def test_json(self):
        obj1 = Clock.set(False, 4, 2020, 2, 4, 6)
        jstr = JSONify.dumps(obj1, indent=4)
        obj2 = Clock.construct_from_jdict(json.loads(jstr))
        self.assertEqual(obj1, obj2)

        time.sleep(1)
        self.assertEqual(obj1, obj2)


    def test_stopped_time(self):
        obj1 = Clock.set(False, 4, 2020, 2, 4, 6)
        obj1.save(Host)
        t1 = obj1.now()

        time.sleep(1)
        t2 = obj1.now()
        self.assertEqual(t2 - t1, timedelta())


    def test_run_time(self):
        obj1 = Clock.set(False, 4, 2020, 2, 4, 6)
        obj1.save(Host)
        t1 = obj1.now()

        obj1.run()

        time.sleep(1)
        t2 = obj1.now()
        self.assertGreater(t2 - t1, timedelta(seconds=4))
        self.assertLess(t2 - t1, timedelta(seconds=4.1))

        time.sleep(1)
        t3 = obj1.now()
        self.assertGreaterEqual(t3 - t1, timedelta(seconds=8))
        self.assertLess(t3 - t1, timedelta(seconds=8.1))


    def test_running_time(self):
        obj1 = Clock.set(True, 4, 2020, 2, 4, 6)
        obj1.save(Host)
        t1 = obj1.now()

        time.sleep(1)
        t2 = obj1.now()
        self.assertGreater(t2 - t1, timedelta(seconds=4))
        self.assertLess(t2 - t1, timedelta(seconds=4.1))

        time.sleep(1)
        t3 = obj1.now()
        self.assertGreaterEqual(t3 - t1, timedelta(seconds=8))
        self.assertLess(t3 - t1, timedelta(seconds=8.1))


    def test_pause(self):
        obj1 = Clock.set(True, 1, 2020, 2, 4, 6)
        obj1.save(Host)
        t1 = obj1.now()

        time.sleep(1)
        t2 = obj1.now()
        self.assertGreater(t2 - t1, timedelta(seconds=1))
        self.assertLess(t2 - t1, timedelta(seconds=1.1))

        obj1.pause()
        time.sleep(1)
        t2 = obj1.now()
        self.assertGreater(t2 - t1, timedelta(seconds=1))
        self.assertLess(t2 - t1, timedelta(seconds=1.1))


    def test_resume(self):
        obj1 = Clock.set(True, 1, 2020, 2, 4, 6)
        obj1.save(Host)
        t1 = obj1.now()

        time.sleep(1)
        t2 = obj1.now()
        self.assertGreater(t2 - t1, timedelta(seconds=1))
        self.assertLess(t2 - t1, timedelta(seconds=1.1))

        obj1.pause()
        time.sleep(1)
        t2 = obj1.now()
        self.assertGreater(t2 - t1, timedelta(seconds=1))
        self.assertLess(t2 - t1, timedelta(seconds=1.1))

        obj1.resume()
        time.sleep(1)
        t2 = obj1.now()
        self.assertGreater(t2 - t1, timedelta(seconds=2))
        self.assertLess(t2 - t1, timedelta(seconds=2.1))


    def test_reload(self):
        obj1 = Clock.set(True, 1, 2020, 2, 4, 6)
        obj1.save(Host)
        t1 = obj1.now()

        time.sleep(1)
        t2 = obj1.now()
        self.assertGreater(t2 - t1, timedelta(seconds=1))
        self.assertLess(t2 - t1, timedelta(seconds=1.1))

        now = obj1.now()

        time.sleep(1)
        obj1.reload(now)
        t2 = obj1.now()
        self.assertGreater(t2 - t1, timedelta(seconds=1))
        self.assertLess(t2 - t1, timedelta(seconds=1.1))


if __name__ == "__main_":
    unittest.main()
