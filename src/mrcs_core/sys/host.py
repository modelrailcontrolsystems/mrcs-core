"""
Created on 9 Nov 2025

@author: Bruno Beloff (bbeloff@me.com)

An SQLite database client

https://docs.python.org/3/howto/enum.html
"""
import os.path


class Host(object):
    """
    An abstraction over the host system
    """

    __MRCS_DIR = 'MRCS'
    __DB_DIR = 'db'

    @classmethod
    def home_abs_dir(cls):
        return os.path.expanduser('~')


    @classmethod
    def mrcs_abs_dir(cls):
        return os.path.join(cls.home_abs_dir(), cls.__MRCS_DIR)


    @classmethod
    def mrcs_db_abs_dir(cls):
        return os.path.join(cls.mrcs_abs_dir(), cls.__DB_DIR)


    @classmethod
    def mrcs_db_abs_file(cls, filename):
        return os.path.join(cls.mrcs_db_abs_dir(), filename)


