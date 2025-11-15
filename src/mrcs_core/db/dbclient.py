"""
Created on 9 Nov 2025

@author: Bruno Beloff (bbeloff@me.com)

An SQLite database client, guaranteeing one connection per database

https://www.sqlitetutorial.net/sqlite-python/
https://forum.xojo.com/t/sqlite-return-id-of-record-inserted/37896
"""

import os
import sqlite3

from mrcs_core.sys.host import Host
from mrcs_core.sys.logging import Logging


class DBClient(object):
    """
    An SQLite database client
    """

    __clients = {}

    @classmethod
    def instance(cls, db_name):
        if db_name not in cls.__clients:
            cls.__clients[db_name] = DBClient(db_name)
            cls.__clients[db_name].__open()

        return cls.__clients[db_name]


    @classmethod
    def drop(cls, db_name):
        if db_name in list(cls.__clients):
            cls.__clients[db_name].__close()
            del cls.__clients[db_name]


    @classmethod
    def drop_all(cls):
        for db_name in list(cls.__clients):
            cls.drop(db_name)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, db_name):
        self.__db_name = db_name

        self.__connection = None
        self.__cursor = None
        self.__logger = Logging.getLogger()


    # ----------------------------------------------------------------------------------------------------------------

    def execute(self, statement, data=None):    # TODO: {statement, data} is maybe a class?
        if self.connection is None:
            raise RuntimeError('execute: no connection')

        if self.cursor is None:
            raise RuntimeError('execute: no cursor')

        if data:
            self.cursor.execute(statement, data)
        else:
            self.cursor.execute(statement)


    def commit(self):
        self.connection.commit()


    def fetchall(self):
        return self.cursor.fetchall()


    def __open(self):
        filename = '.'.join([self.db_name, 'db'])

        os.makedirs(Host.mrcs_db_abs_dir(), exist_ok=True)
        self.__connection = sqlite3.connect(Host.mrcs_db_abs_file(filename))
        self.__cursor = self.connection.cursor()


    def __close(self):
        if self.connection:
            self.connection.close()
            self.__cursor = None
            self.__connection = None


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def db_name(self):
        return self.__db_name


    @property
    def connection(self):
        return self.__connection


    @property
    def cursor(self):
        return self.__cursor


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return f'Client:{{db_name:{self.db_name}, connection:{self.connection}, cursor:{self.cursor}}}'
