"""
Created on 4 Oct 2026

@author: Bruno Beloff (bbeloff@me.com)

A DCC motive power unit (MPU), as listed in an inventory

{
    "label": "DB59",
    "addr": 5,
    "operator": "DB Schenker",
    "class": "59",
    "number": "59201",
    "vendor": "Revolution Trains",
    "length": 145,
    "cvs": [
        {
            "type": "NumericCV",
            "addr": "ACCELERATION",
            "value": 5
        },
        {
            "type": "NumericCV",
            "addr": "DECELERATION",
            "value": 9
        }
    ]
}
"""

from collections import OrderedDict
from typing import Any, Self

from mrcs_core.data.json import JSONable
from mrcs_core.equipment.motive_power_unit.mpu_enums import MPUDirection
from mrcs_core.equipment.motive_power_unit.mpu_functions import MPUFunctions
from mrcs_core.equipment.motive_power_unit.mpu_status import MPUStatus
from mrcs_core.inventory.configuration_variable.cv import CV
from mrcs_core.inventory.configuration_variable.cv_address import CVAddress
from mrcs_core.inventory.configuration_variable.cv_builder import CVBuilder


# --------------------------------------------------------------------------------------------------------------------

class MPU(JSONable):
    """
    A DCC motive power unit (MPU), as listed in an inventory
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

            cvs = OrderedDict()
            for cv_jdict in jdict.get('cvs', []):
                cv = CVBuilder.construct_from_jdict(cv_jdict)
                if cv.cv_address in cvs:
                    raise ValueError(f'duplicate cv address: {cv.cv_address.name}')

                cvs[cv.cv_address] = cv

        except (TypeError, ValueError):
            raise ValueError(jdict)

        return cls(label, address, operator, mpu_class, number, vendor, length, cvs)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, label: str, address: int, operator: str, mpu_class: str, number: str, vendor: str,
                 length: int, cvs: OrderedDict[CVAddress, CV]):
        self.__label = label
        self.__address = address

        self.__operator = operator
        self.__mpu_class = mpu_class
        self.__number = number
        self.__vendor = vendor

        self.__length = length
        self.__cvs = cvs


    def __eq__(self, other: Any):
        try:
            return (self.label == other.label and self.address == other.address and self.operator == other.operator and
                    self.mpu_class == other.mpu_class and self.number == other.number and
                    self.vendor == other.vendor and self.length == other.length and self.cvs == other.cvs)
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
        jdict['cvs'] = self.cvs

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def cvs(self):
        return tuple(self.__cvs.values())


    def cv(self, address: CVAddress):
        try:
            return self.__cvs[address]
        except KeyError:
            return None


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
        cvs = '[' + ', '.join([str(cv) for cv in self.cvs]) + ']'

        return (f'MPU:{{label:{self.label}, address:{self.address}, operator:{self.operator}, '
                f'mpu_class:{self.mpu_class}, number:{self.number}, vendor:{self.vendor}, length:{self.length}, '
                f'cvs:{cvs}}}')
