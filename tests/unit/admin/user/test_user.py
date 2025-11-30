"""
Created on 15 Nov 2025

@author: Bruno Beloff (bbeloff@me.com)

python -m unittest -v data/test_equipment_filter.py

https://realpython.com/python-testing/
https://www.jetbrains.com/help/pycharm/creating-tests.html
"""

import json
import os
import unittest

from mrcs_core.admin.user.user import User
from mrcs_core.data.json import JSONify


# --------------------------------------------------------------------------------------------------------------------

class TestUser(unittest.TestCase):
    def test_construct_from_none_jdict(self):
        obj1 = User.construct_from_jdict({})
        self.assertEqual(None, obj1)

    def test_construct_from_jdict(self):
        obj1 = self.__load_user('new_user.json')
        self.assertEqual('User:{uid:None, email:bbeloff@me.com, role:ADMIN, must_set_password:True, '
                         'given_name:Bruno, family_name:Beloff, created:None, latest_login:None}', str(obj1))

    def test_eq(self):
        obj1 = self.__load_user('new_user.json')
        self.assertEqual(True, obj1 == obj1)

    def test_neq(self):
        obj1 = self.__load_user('new_user.json')
        obj2 = self.__load_user('saved_user.json')
        self.assertEqual(False, obj1 == obj2)

    def test_lt(self):
        obj1 = self.__load_user('new_user.json')
        obj2 = self.__load_user('gt_user.json')
        self.assertEqual(True, obj1 < obj2)

    def test_nlt(self):
        obj1 = self.__load_user('new_user.json')
        obj2 = self.__load_user('gt_user.json')
        self.assertEqual(False, obj2 < obj1)

    def test_as_json(self):
        obj1 = self.__load_user('saved_user.json')
        self.assertEqual('{"uid": "c69a665c-11b5-4755-a903-97095f9dc915", "email": "bbeloff@me.com", '
                         '"role": "ADMIN", "must_set_password": true, "given_name": "Bruno", "family_name": "Beloff", '
                         '"created": "2025-11-30T09:36:23.553+00:00", "latest_login": null}',
                         JSONify.dumps(obj1))


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def __load_user(cls, rel_filename):
        abs_filename = os.path.join(os.path.dirname(__file__), 'data', rel_filename)
        with open(abs_filename) as fp:
            jdict = json.load(fp)

        return User.construct_from_jdict(jdict)


if __name__ == "__main_":
    unittest.main()
