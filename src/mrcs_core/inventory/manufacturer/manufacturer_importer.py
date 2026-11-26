"""
Created on 7 Nov 2026

@author: Bruno Beloff (bbeloff@me.com)

A utility to import manufacturers.csv and generate manufacturer.py items

In the python console:
from mrcs_core.inventory.manufacturer.manufacturer_importer import ManufacturerImporter
ManufacturerImporter.do_import()
"""

import os
import re
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
        abs_filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', cls.FILE)
        rows = CSV.read(filename=abs_filename)

        manufacturers = OrderedDict()  # remove duplicates

        for row in rows:
            name = str(row.get('Manufacturer') or '')
            value = int(row.get('Decimal') or -1)

            name = name.replace(' ', '_').replace('.', '').replace('(', '').replace(')', '').replace('&', 'AND')
            name = name.replace('–', '_').replace('-', '_').replace('/', '_').upper()
            name = name.replace('Å', 'A').replace('Ö', 'O').replace('Ü', 'U')
            name = re.sub('_+', '_', name)
            manufacturers[name] = value

        print()
        print('    ALL = 0')
        print()

        for name, value in manufacturers.items():
            print(f'    {name} = {value}')
