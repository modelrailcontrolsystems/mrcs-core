"""
Created on 29 Aug 2026

@author: Bruno Beloff (bbeloff@me.com)

python -m unittest -v unit/system/test_server.py

https://realpython.com/python-testing/
https://www.jetbrains.com/help/pycharm/creating-tests.html
"""

import json
import unittest
from pathlib import Path

from mrcs_core.data.json import JSONify
from mrcs_core.sys.server import Server


# --------------------------------------------------------------------------------------------------------------------

class TestServer(unittest.TestCase):
    __filename1 = Path(__file__).parent / 'data' / 'server.json'
    __jdict1 = None


    @classmethod
    def setUpClass(cls):
        with open(cls.__filename1) as fp:
            cls.__jdict1 = json.load(fp)


    def test_server_construct(self):
        obj1 = Server.construct_from_jdict(self.__jdict1)
        self.assertEqual("Server:{name:None, host:127.0.0.1, port:8000, is_secure:False}", str(obj1))
        self.assertEqual('127.0.0.1', obj1.host)
        self.assertEqual(8000, obj1.port)
        self.assertFalse(obj1.is_secure)
        self.assertIsNone(obj1.name)


    def test_server_construct_with_name(self):
        obj1 = Server.construct_from_jdict(self.__jdict1, name='local')
        self.assertEqual("Server:{name:local, host:127.0.0.1, port:8000, is_secure:False}", str(obj1))
        self.assertEqual('local', obj1.name)


    def test_server_construct_none(self):
        self.assertIsNone(Server.construct_from_jdict(None))
        self.assertIsNone(Server.construct_from_jdict({}))


    def test_server_json(self):
        obj1 = Server.construct_from_jdict(self.__jdict1)
        jdict = obj1.as_jdict()
        self.assertEqual(self.__jdict1, jdict)
        self.assertEqual('{"host": "127.0.0.1", "port": 8000, "is_secure": false}', JSONify.dumps(obj1))


    def test_server_authority(self):
        obj1 = Server.construct_from_jdict(self.__jdict1)
        self.assertEqual('127.0.0.1:8000', obj1.authority)

        obj2 = Server('127.0.0.1', 80, False)
        self.assertEqual('127.0.0.1', obj2.authority)


    def test_server_base_url(self):
        obj1 = Server.construct_from_jdict(self.__jdict1)
        self.assertEqual('http://127.0.0.1:8000', obj1.base_url)

        obj2 = Server('127.0.0.1', 443, True)
        self.assertEqual('https://127.0.0.1:443', obj2.base_url)

        obj3 = Server('example.com', 80, True)
        self.assertEqual('https://example.com', obj3.base_url)


    def test_server_url(self):
        obj1 = Server.construct_from_jdict(self.__jdict1)
        self.assertEqual('http://127.0.0.1:8000/', obj1.url())
        self.assertEqual('http://127.0.0.1:8000/api/v1', obj1.url('/api/v1'))

        with self.assertRaises(ValueError):
            obj1.url('invalid_path')


    def test_server_persistence_location(self):
        self.assertEqual(('conf', 'server_conf.json'), Server.persistence_location(None))
        self.assertEqual(('conf', 'local_server_conf.json'), Server.persistence_location('local'))


# --------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    unittest.main()
