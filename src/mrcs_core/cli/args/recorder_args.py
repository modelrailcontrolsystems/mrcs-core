"""
Created on 17 Nov 2025

@author: Bruno Beloff (bbeloff@me.com)

https://realpython.com/command-line-interfaces-python-argparse/
"""

import argparse

from mrcs_core import version
from mrcs_core.operations.operation_mode import OperationMode


# --------------------------------------------------------------------------------------------------------------------

class RecorderArgs(object):
    """unix command line handler"""

    def __init__(self, description):
        """
        Constructor
        """
        self.__parser = argparse.ArgumentParser(description=description)

        self.__parser.add_argument("-m", "--mode", action="store", type=str,
                                   choices=OperationMode.keys(), required=True,
                                   help='operate in given mode')

        self.__parser.add_argument("-c", "--clean", action="store_true",
                                   help='discard existing messages')

        self.__parser.add_argument("-s", "--subscribe", action="store_true",
                                   help='subscribe to future messages')

        self.__parser.add_argument("-v", "--verbose", action="store_true",
                                   help='report narrative to stderr')

        self.__parser.add_argument("--version", action="version",
                                   version=f'{self.__parser.prog} {version()}')

        self.__args = self.__parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def mode(self) -> OperationMode:
        return OperationMode[self.__args.mode]


    @property
    def clean(self):
        return self.__args.clean


    @property
    def subscribe(self):
        return self.__args.subscribe


    @property
    def verbose(self):
        return self.__args.verbose


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return (f'RecorderArgs:{{mode:{self.mode}, clean:{self.clean}, subscribe:{self.subscribe}, '
                f'verbose:{self.verbose}}}')
