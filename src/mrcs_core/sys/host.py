"""
Created on 9 Nov 2025

@author: Bruno Beloff (bbeloff@me.com)

Abstractions over the system host, its filesystem and its network connections

https://superuser.com/questions/357159/osx-terminal-showing-incorrect-hostname
"""

import os.path
import socket

from mrcs_core.sys.persistence_manager import FilesystemPersistenceManager


# --------------------------------------------------------------------------------------------------------------------

class Host(FilesystemPersistenceManager):
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
    def mrcs_db_abs_dir(cls, db_mode):
        return os.path.join(cls.mrcs_abs_dir(), cls.__DB_DIR, db_mode)


    @classmethod
    def mrcs_db_abs_file(cls, db_mode, filename):
        return os.path.join(cls.mrcs_db_abs_dir(db_mode), filename)


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def name(cls):
        return socket.gethostname()


