"""
Created on 20 Jan 2021

@author: Bruno Beloff (bbeloff@me.com)

https://realpython.com/python-logging/
https://stackoverflow.com/questions/35325042/python-logging-disable-logging-from-imported-modules
"""

import logging
import sys


# --------------------------------------------------------------------------------------------------------------------

class LoggingSpecification(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, name, level):
        self.__name = name                              # string
        self.__level = level                            # int or string


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def name(self):
        return self.__name


    @property
    def level(self):
        return self.__level


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return f'LoggingSpecification:{{name:{self.name}, level:{self.level}}}'


# --------------------------------------------------------------------------------------------------------------------

class Logging(object):
    """
    classdocs
    """

    __NAME = None
    __LEVEL = logging.NOTSET

    __MULTI_FORMAT = '%(name)s: %(message)s'

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def config(cls, name, verbose=False, level=logging.ERROR, stream=sys.stderr):       # for CLU
        cls.__NAME = name
        cls.__LEVEL = logging.INFO if verbose else level

        logging.basicConfig(format=cls.__MULTI_FORMAT, level=logging.CRITICAL, stream=stream)


    @classmethod
    def replicate(cls, specification: LoggingSpecification, stream=sys.stderr):         # for child process
        cls.__NAME = specification.name
        cls.__LEVEL = specification.level

        logging.basicConfig(format=cls.__MULTI_FORMAT, level=logging.CRITICAL, stream=stream)


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def getLogger(cls, name=None):
        logger_name = cls.__NAME if cls.__NAME else name

        logger = logging.getLogger(name=logger_name)
        logger.setLevel(cls.__LEVEL)

        return logger


    @classmethod
    def debugging_on(cls):
        return cls.__LEVEL == logging.DEBUG


    @classmethod
    def specification(cls):
        return LoggingSpecification(cls.__NAME, cls.__LEVEL)


    @classmethod
    def level(cls):
        return cls.__LEVEL
