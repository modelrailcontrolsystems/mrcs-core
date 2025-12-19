"""
Created on 27 May 2017

@author: Bruno Beloff (bbeloff@me.com)

A stdio abstraction

WARNING: macOS (darwin) users must install the gnureadline package
"""

import sys
import termios

from getpass import getpass


# --------------------------------------------------------------------------------------------------------------------

class StdIO(object):
    """
    classdocs
    """

    @staticmethod
    def prompt(request, default=None):
        try:
            termios.tcflush(sys.stdin, termios.TCIOFLUSH)           # flush stdin
        except termios.error:
            pass

        prompt_str = f'{request} ({default}): ' if default else f'{request}: '
        line = input(prompt_str).strip()

        return line.strip() if line else default


    @staticmethod
    def password(request):
        try:
            termios.tcflush(sys.stdin, termios.TCIOFLUSH)           # flush stdin
        except termios.error:
            pass

        return getpass(f'{request}: ').strip()
