"""
Created on 27 Oct 2026

@author: Bruno Beloff (bbeloff@me.com)

Utilities converting between CSV files and lists of dictionaries (of scalars)

I/O is stdin / stdout or by file. Encoding is utf-8. The CSV supports three data types:
* None
* String
* Float

Warnings:
* read(..) - converts integers to floats
* write(..) - uses the first dictionary in the list to determine the CSV header; all subsequent dictionaries
must have the same keys

https://dev.to/documendous/why-you-should-end-your-source-files-with-a-new-line-156g
"""

import csv
import sys
from contextlib import nullcontext
from typing import Literal


# --------------------------------------------------------------------------------------------------------------------

class CSV(object):
    """
    Utilities converting between CSV files and lists of dictionaries
    """

    __ENCODING = 'utf-8'
    __QUOTING: Literal[4] = csv.QUOTE_STRINGS


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def read(cls, filename: str | None = None) -> list[dict]:
        csv_filename = filename
        csv_file = None
        data = []

        if csv_filename:
            csv_file = open(csv_filename, encoding=cls.__ENCODING)
            context = csv_file
        else:
            context = nullcontext(sys.stdin)

        try:
            with context as channel:
                reader = csv.DictReader(channel, quoting=cls.__QUOTING)
                for row in reader:
                    data.append(row)

            return data

        finally:
            if csv_file:
                csv_file.close()


    @classmethod
    def write(cls, data: list[dict], filename: str | None = None, append: bool = False) -> None:
        csv_filename = filename
        csv_file = None

        if csv_filename:
            mode = 'a' if append else 'w'
            csv_file = open(csv_filename, mode=mode, newline='', encoding=cls.__ENCODING)
            context = csv_file
        else:
            context = nullcontext(sys.stdout)

        if not data:
            return

        try:
            with context as channel:
                fieldnames = data[0].keys()
                writer = csv.DictWriter(channel, fieldnames=fieldnames, quoting=cls.__QUOTING)
                if not append:
                    writer.writeheader()

                for datum in data:
                    writer.writerow(datum)

        finally:
            if csv_file:
                csv_file.close()
