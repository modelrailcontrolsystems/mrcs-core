"""
Created on 24 Sep 2016

@author: Bruno Beloff (bbeloff@me.com)

https://docs.python.org/3/library/struct.html
https://stackoverflow.com/questions/8022530/how-to-check-for-valid-email-address
"""

import re

from datetime import date
from urllib.parse import urlparse


# --------------------------------------------------------------------------------------------------------------------

class Datum(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------
    # effective input...

    @classmethod
    def effective_lines(cls, source):
        for line in source:
            stripped_line = line.strip()

            if not stripped_line:
                continue

            yield stripped_line


    # ----------------------------------------------------------------------------------------------------------------
    # formatting...

    @classmethod
    def is_email_address(cls, value):
        try:
            return bool(re.match(r'[^@\s]+@[^@\s]+\.[^@\s]+', value))
        except TypeError:
            return False


    @classmethod
    def is_url(cls, value):
        try:
            result = urlparse(value)
            return all((result.scheme, result.netloc))
        except AttributeError:
            return False


    @classmethod
    def is_true(cls, value):
        return value in ['True', 'true']


    # ----------------------------------------------------------------------------------------------------------------
    # morphological numeracy...

    @classmethod
    def is_numeric(cls, value):
        return cls.precision(value) is not None


    @classmethod
    def is_int(cls, value):
        precision = cls.precision(value)

        if precision is None:
            return False

        return precision == 0


    @classmethod
    def is_float(cls, value):
        precision = cls.precision(value)

        if precision is None:
            return False

        return precision > 0


    @staticmethod
    def precision(value):
        if value is None:
            return None

        if isinstance(value, bool):
            return None

        try:
            float(value)
        except ValueError:
            return None

        pieces = str(value).split('.')

        # int...
        if len(pieces) == 1:
            return 0                            # warning: round(123, 0) returns 123.0 - use round(123)

        # float...
        return len(pieces[1])                   # warning: interprets 1. as precision 0


    # ----------------------------------------------------------------------------------------------------------------
    # cast or None...

    @staticmethod
    def str(value, default=None):
        if value is None:
            return default

        return str(value)


    @staticmethod
    def bool(value, default=None):
        if value is None:
            return default

        try:
            value = bool(value)
        except ValueError:
            return default

        return value


    @staticmethod
    def int(value, default=None):
        if value is None:
            return default

        try:
            number = int(float(value))              # because int('123.000') raises a ValueError!
        except ValueError:
            return default

        return number


    @staticmethod
    def float(value, ndigits=None, default=None):
        if value is None:
            return default

        try:
            number = float(value)
        except ValueError:
            return default

        return number if ndigits is None else round(number, ndigits)      # warning: round(123, 0) returns 123.0


    @staticmethod
    def date(iso_date):
        if iso_date is None:
            return None

        parts = iso_date.split("-")

        if len(parts) != 3:
            return None

        try:
            year = int(float(parts[0]))
            month = int(float(parts[1]))
            day = int(float(parts[2]))
        except ValueError:
            return None

        return date(year, month, day)
