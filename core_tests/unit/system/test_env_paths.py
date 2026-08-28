"""
Created on 28 Aug 2026

@author: Bruno Beloff (bbeloff@me.com)

python -m unittest -v unit/system/test_env_paths.py

https://realpython.com/python-testing/
https://www.jetbrains.com/help/pycharm/creating-tests.html
"""

import unittest

from mrcs_core.sys.env_paths import EnvPaths


# --------------------------------------------------------------------------------------------------------------------

class TestEnvPaths(unittest.IsolatedAsyncioTestCase):

    def test_construct(self):
        mrcs = EnvPaths.mrcs()
        obj1 = EnvPaths.construct()
        self.assertEqual(
            f"EnvPaths:{{path:['{mrcs}/mrcs-cli/src/mrcs_cli/cli', "
            f"'{mrcs}/mrcs-api/src/mrcs_api/cli', "
            f"'{mrcs}/mrcs-control/src/mrcs_control/cli', "
            f"'{mrcs}/.venv14/bin'], "
            f"python_path:[{repr(mrcs / 'mrcs-cli/src')}, "
            f"{repr(mrcs / 'mrcs-api/src')}, "
            f"{repr(mrcs / 'mrcs-control/src')}, "
            f"{repr(mrcs / 'mrcs-core/src')}]}}",
            str(obj1))


    def test_as_dict(self):
        mrcs = EnvPaths.mrcs()
        obj1 = EnvPaths.construct()
        self.assertEqual(
            f"{{'PATH': '{mrcs}/mrcs-cli/src/mrcs_cli/cli:"
            f"{mrcs}/mrcs-api/src/mrcs_api/cli:"
            f"{mrcs}/mrcs-control/src/mrcs_control/cli:"
            f"{mrcs}/.venv14/bin', "
            f"'PYTHONPATH': '{mrcs}/mrcs-cli/src:"
            f"{mrcs}/mrcs-api/src:"
            f"{mrcs}/mrcs-control/src:"
            f"{mrcs}/mrcs-core/src'}}",
            str(obj1.as_dict()))
