"""
Created on 29 Nov 2025

@author: Bruno Beloff (bbeloff@me.com)

python -m unittest -v mrcs-core/tests/unit/admin/user/test_user_persistence.py

https://realpython.com/python-testing/
https://www.jetbrains.com/help/pycharm/creating-tests.html
"""

import json
import os
import unittest

from mrcs_core.db.dbclient import DBClient, DBMode
from setup import Setup

from mrcs_core.admin.user.user import User


# --------------------------------------------------------------------------------------------------------------------

class TestUserPersistence(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        DBClient.set_client_db_mode(DBMode.TEST)
        Setup.dbSetup()

    def test_insert(self):
        obj1 = self.__setup_db()
        records = list(User.find_all())
        obj2 = records[0]

        self.assertEqual(obj2.email, obj1.email)

    def test_find(self):
        obj1 = self.__setup_db()
        obj2 = User.find(obj1.uid)

        self.assertEqual(obj2.email, obj1.email)

    def test_update(self):
        obj1 = self.__setup_db()
        obj2 = User(obj1.uid, obj1.email, obj1.role, obj1.must_set_password, 'Mickey', 'Mouse',
                    obj1.created, obj1.latest_login)
        obj2.save()
        obj3 = User.find(obj1.uid)

        self.assertEqual(obj3.given_name, 'Mickey')
        self.assertEqual(obj3.family_name, 'Mouse')

    def test_delete(self):
        obj1 = self.__setup_db()
        User.delete(obj1.uid)
        obj2 = User.find(obj1.uid)

        self.assertEqual(obj2, None)

    def test_log_in(self):
        obj1 = self.__setup_db()
        success = obj1.log_in(obj1.email, 'password')
        self.assertEqual(success, True)

        success = obj1.log_in(obj1.email, 'junk')
        self.assertEqual(success, False)

    def test_set_password(self):
        obj1 = self.__setup_db()
        obj1.set_password(obj1.uid, 'admin')
        success = obj1.log_in(obj1.email, 'admin')

        self.assertEqual(success, True)

    def test_email(self):
        obj1 = self.__setup_db()
        self.assertEqual(User.email_in_use(obj1.email), True)
        self.assertEqual(User.email_in_use('xbeloff@me.com'), False)


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def __setup_db(cls):
        User.recreate_tables()

        abs_filename = os.path.join(os.path.dirname(__file__), 'data', 'new_user.json')
        with open(abs_filename) as fp:
            jdict = json.load(fp)

        obj1 = User.construct_from_jdict(jdict)
        return obj1.save(password='password')


if __name__ == "__main_":
    unittest.main()
