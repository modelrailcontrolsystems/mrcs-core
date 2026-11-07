"""
Created on 7 Nov 2026

@author: Bruno Beloff (bbeloff@me.com)

Import manufacturers.csv and generate manufacturer.py items
"""

import os
from collections import OrderedDict

from mrcs_core.data.csv import CSV


# --------------------------------------------------------------------------------------------------------------------

class ManufacturerImporter(object):
    """
    import manufacturers.csv and generate manufacturer.py items
    """

    FILE = 'manufacturers.csv'


    @classmethod
    def do_import(cls) -> None:
        abs_filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), cls.FILE)
        rows = CSV.read(filename=abs_filename)

        manufacturers = OrderedDict()  # remove duplicates

        for row in rows:
            name = row.get('Manufacturer', '')
            value = int(row.get('Decimal', -1))

            name = name.replace(' ', '_').replace('.', '').replace('(', '').replace(')', '').replace('&', 'AND')
            name = name.replace('–', '_').replace('-', '_').replace('/', '_').upper()
            name = name.replace('Å', 'A').replace('Ö', 'O').replace('Ü', 'U').replace('__', '_')
            manufacturers[name] = value

        for name, value in manufacturers.items():
            print(f'    {name} = {value}')
