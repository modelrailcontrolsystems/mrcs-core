"""
Created on 8 Feb 2026

@author: Bruno Beloff (bbeloff@me.com)

Establish PATH and PYTHONPATH for Popen processes launched within an IDE.
MRCS (the relative path from the user home to the MRCS repos) and VENV must be set in an accessible .env file.

Example file:
HOME=/Users/bruno
MRCS=Documents/Development/Python/MRCS/MRCSMacProject
VENV=.venv14


https://dev.to/jakewitcher/using-env-files-for-environment-variables-in-python-applications-55a1
"""

import os

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


    @classmethod
    def mrcs(cls):
        return os.path.join(cls.__HOME, cls.__MRCS)


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct(cls):
        path = []
        python_path = []

        for repo in cls.__REPOS:
            repo_src = os.path.join(cls.mrcs(), repo, 'src')
            python_path.append(repo_src)

            if repo in cls.__LIB_REPOS:
                continue

            package = repo.replace('-', '_')
            path.append(os.path.join(repo_src, package, 'cli'))

        venv_path = os.path.join(cls.mrcs(), cls.__VENV, 'bin')
        path.append(venv_path)

        return cls(path, python_path)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, path, python_path):
        self.__path = path
        self.__python_path = python_path


    # ----------------------------------------------------------------------------------------------------------------

    def as_dict(self):
        return dict(PATH=':'.join(self.path), PYTHONPATH=':'.join(self.python_path))


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def path(self):
        return self.__path


    @property
    def python_path(self):
        return self.__python_path


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return f'EnvPaths:{{path:{self.path}, python_path:{self.python_path}}}'
