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
from typing import Any, Literal


# --------------------------------------------------------------------------------------------------------------------

class CSV(object):
    """
    Utilities converting between CSV files and lists of dictionaries
    """

    __ENCODING = 'utf-8'
    __QUOTING: Literal[4] = csv.QUOTE_STRINGS        # Literal[4] is QUOTE_STRINGS - keeps PyCharm and mypy happy


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def read(cls, filename: str | None = None) -> list[dict[str, str | float | None]]:
        data: list[dict[str, str | float | None]] = []

        with open(filename, encoding=cls.__ENCODING) if filename else nullcontext(sys.stdin) as channel:
            for row in csv.DictReader(channel, quoting=cls.__QUOTING):
                data.append(row)

        return data


    @classmethod
    def write(cls, data: list[dict[str, Any]], filename: str | None = None, append: bool = False) -> None:
        mode = 'a' if append else 'w'

        with (open(filename, mode=mode, newline='', encoding=cls.__ENCODING) if filename
              else nullcontext(sys.stdout)) as channel:
            if not data:
                return

            writer = csv.DictWriter(channel, fieldnames=data[0].keys(), quoting=cls.__QUOTING)
            if not append:
                writer.writeheader()

            for datum in data:
                writer.writerow(datum)
