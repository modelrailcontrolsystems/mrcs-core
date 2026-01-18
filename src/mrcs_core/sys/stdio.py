"""
Created on 27 May 2017

@author: Bruno Beloff (bbeloff@me.com)

A stdio abstraction

WARNING: macOS (darwin) users must install the gnureadline package

https://stackoverflow.com/questions/11130156/suppress-stdout-stderr-print-from-python-functions
"""

import sys
import termios

from contextlib import contextmanager, redirect_stderr, redirect_stdout
from getpass import getpass
from os import devnull


# --------------------------------------------------------------------------------------------------------------------

class StdIO(object):
    """
    classdocs
    """

    @staticmethod
    def prompt(request, default=None):
        try:
            termios.tcflush(sys.stdin, termios.TCIOFLUSH)  # flush stdin
        except termios.error:
            pass

        prompt_str = f'{request} ({default}): ' if default else f'{request}: '
        line = input(prompt_str).strip()

        return line.strip() if line else default


    @staticmethod
    def password(request):
        try:
            termios.tcflush(sys.stdin, termios.TCIOFLUSH)  # flush stdin
        except termios.error:
            pass

        return getpass(f'{request}: ').strip()


    @staticmethod
    @contextmanager
    def suppress_stdout_stderr():
        with open(devnull, 'w') as f_null:
            with redirect_stderr(f_null) as err, redirect_stdout(f_null) as out:
                yield err, out
