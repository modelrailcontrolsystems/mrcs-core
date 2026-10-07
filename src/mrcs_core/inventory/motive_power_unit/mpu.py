"""
Created on 4 Oct 2026

@author: Bruno Beloff (bbeloff@me.com)

A DCC motive power unit (MPU), as listed in an inventory

{
    "label": "lab1",
    "addr": 5,
    "operator": "DB",
    "class": "59",
    "number": "593456",
    "vendor": "Revolution Trains"
    "length": 15,
}
"""

from collections import OrderedDict
from typing import Any, Self

from mrcs_core.data.json import JSONable
from mrcs_core.equipment.motive_power_unit.mpu_enums import MPUDirection
from mrcs_core.equipment.motive_power_unit.mpu_functions import MPUFunctions
from mrcs_core.equipment.motive_power_unit.mpu_status import MPUStatus


# --------------------------------------------------------------------------------------------------------------------

class MPU(JSONable):
    """
    A DCC motive power unit (MPU)
    """


    @classmethod
    def construct_from_jdict(cls, jdict) -> Self:
        try:
            label = jdict.get('label')
            address = int(jdict.get('addr'))

            operator = jdict.get('operator')
            mpu_class = jdict.get('class')
            number = jdict.get('number')
            vendor = jdict.get('vendor')

            length = int(jdict.get('length'))

            # TODO: add decoder, CV pairs here
        except (TypeError, ValueError):
            raise ValueError(jdict)

        return cls(label, address, operator, mpu_class, number, vendor, length)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, label: str, address: int, operator: str, mpu_class: str, number: str, vendor: str,
                 length: int):
        self.__label = label
        self.__address = address

        self.__operator = operator
        self.__mpu_class = mpu_class
        self.__number = number
        self.__vendor = vendor

        self.__length = length


    def __eq__(self, other: Any):
        try:
            return (self.label == other.label and self.address == other.address and self.operator == other.operator and
                    self.mpu_class == other.mpu_class and self.number == other.number and
                    self.vendor == other.vendor and self.length == other.length)
        except (AttributeError, TypeError):
            return False


    def __lt__(self, other: Any):
        if self.label < other.label:
            return True

        if self.label > other.label:
            return False

        return self.address < other.address


    # ----------------------------------------------------------------------------------------------------------------

    def mpu_status(self) -> MPUStatus:
        return MPUStatus(self.label, self.address, MPUFunctions([]), None, None, MPUDirection.UNKNOWN)


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        jdict = OrderedDict()

        jdict['label'] = self.label
        jdict['addr'] = self.address

        jdict['operator'] = self.operator
        jdict['class'] = self.mpu_class
        jdict['number'] = self.number
        jdict['vendor'] = self.vendor

        jdict['length'] = self.length

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def label(self):
        return self.__label


    @property
    def address(self):
        return self.__address


    @property
    def operator(self):
        return self.__operator


    @property
    def mpu_class(self):
        return self.__mpu_class


    @property
    def number(self):
        return self.__number


    @property
    def vendor(self):
        return self.__vendor


    @property
    def length(self):
        return self.__length


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return (f'MPU:{{label:{self.label}, address:{self.address}, operator:{self.operator}, '
                f'mpu_class:{self.mpu_class}, number:{self.number}, vendor:{self.vendor}, '
                f'length:{self.length}}}')
