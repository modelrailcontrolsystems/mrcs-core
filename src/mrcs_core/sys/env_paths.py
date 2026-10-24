"""
Created on 8 Feb 2026

@author: Bruno Beloff (bbeloff@me.com)

Establish PATH and PYTHONPATH for Popen processes launched within an IDE.
MRCS (the relative path from the user home to the MRCS repos) and VENV must be set in an accessible .env file.
SWI_HOME_DIR (the SWI-Prolog home, required by janus_swi) is passed through if set.

Example file:
HOME=/Users/bruno
MRCS=Documents/Development/Python/MRCS/MRCSMacProject
VENV=.venv
SWI_HOME_DIR=/Applications/SWI-Prolog.app/Contents/Resources/swipl

https://dev.to/jakewitcher/using-env-files-for-environment-variables-in-python-applications-55a1
"""

import os
from pathlib import Path
from typing import Self

from dotenv import load_dotenv


# --------------------------------------------------------------------------------------------------------------------

class EnvPaths(object):
    """
    classdocs
    """

    __REPOS = ('mrcs-cli', 'mrcs-api', 'mrcs-control', 'mrcs-core')
    __LIB_REPOS = ('mrcs-core',)

    load_dotenv()

    __HOME = os.getenv('HOME')
    __MRCS = os.getenv('MRCS')
    __VENV = os.getenv('VENV')
    __SWI_HOME_DIR = os.getenv('SWI_HOME_DIR')


    @classmethod
    def mrcs(cls):
        if cls.__HOME is None:
            raise EnvironmentError("HOME environment variable is not set")
        if cls.__MRCS is None:
            raise EnvironmentError("MRCS environment variable is not set")

        return Path(cls.__HOME) / cls.__MRCS


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct(cls) -> Self:
        path = []
        python_path = []

        if cls.__VENV is None:
            raise EnvironmentError("VENV environment variable is not set")

        for repo in cls.__REPOS:
            repo_src = cls.mrcs() / repo / 'src'
            python_path.append(repo_src)

            if repo in cls.__LIB_REPOS:
                continue

            package = repo.replace('-', '_')
            path.append(str(repo_src / package / 'cli'))

        venv_path = cls.mrcs() / cls.__VENV / 'bin'
        path.append(str(venv_path))

        return cls(path, python_path, cls.__SWI_HOME_DIR)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, path, python_path, swi_home_dir=None):
        self.__path = path
        self.__python_path = python_path
        self.__swi_home_dir = swi_home_dir


    # ----------------------------------------------------------------------------------------------------------------

    def as_dict(self):
        env = dict(
            PATH=':'.join(str(path) for path in self.path),
            PYTHONPATH=':'.join(str(path) for path in self.python_path)
        )

        if self.swi_home_dir is not None:
            env['SWI_HOME_DIR'] = self.swi_home_dir

        return env


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def path(self):
        return self.__path


    @property
    def python_path(self):
        return self.__python_path


    @property
    def swi_home_dir(self):
        return self.__swi_home_dir


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return f'EnvPaths:{{path:{self.path}, python_path:{self.python_path}, swi_home_dir:{self.swi_home_dir}}}'
