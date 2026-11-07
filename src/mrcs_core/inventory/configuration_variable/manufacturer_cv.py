"""
Created on 10 Oct 2026

@author: Bruno Beloff (bbeloff@me.com)

Configuration variable for numeric values

{
    "type": "ManufacturerCV",
    "addr": "MANUFACTURER_ID",
    "mfr": "ZIMO"
}
"""

from collections import OrderedDict
from typing import Any, Self

from mrcs_core.equipment.conviguration_variable.cv_report import CVReport
from mrcs_core.inventory.configuration_variable.cv import CV
from mrcs_core.inventory.configuration_variable.cv_address import CVAddress
from mrcs_core.inventory.motive_power_unit.manufacturer import Manufacturer


# --------------------------------------------------------------------------------------------------------------------

class ManufacturerCV(CV):
    """
    Configuration variable for numeric values
    """


    @classmethod
    def construct_from_report(cls, report: CVReport) -> Self:
        cv_address = CVAddress(report.cv_address)  # may raise KeyError
        manufacturer = Manufacturer(report.value)  # may raise KeyError
        return cls(cv_address, manufacturer)


    @classmethod
    def construct_from_jdict(cls, jdict) -> Self:
        try:
            cv_address = CVAddress[jdict.get('addr')]  # may raise KeyError
            manufacturer = Manufacturer[jdict.get('mfr')]  # may raise KeyError

        except (TypeError, ValueError):
            raise ValueError(jdict)

        return cls(cv_address, manufacturer)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, cv_address: CVAddress, manufacturer: Manufacturer):
        super().__init__(cv_address)
        self.__manufacturer = manufacturer


    def __eq__(self, other: Any):
        try:
            return self.cv_address == other.cv_address and self.manufacturer == other.manufacturer
        except (AttributeError, TypeError):
            return False


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        jdict = OrderedDict()

        jdict['type'] = self.type_name()

        jdict['addr'] = self.cv_address.name  # TODO: stop using .name and implement as_json() instead
        jdict['mfr'] = self.manufacturer.name

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def manufacturer(self) -> Manufacturer:
        return self.__manufacturer


    @property
    def value(self) -> int:
        return self.manufacturer.value


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return f'ManufacturerCV{{cv_address:{self.cv_address}, manufacturer:{self.manufacturer}}}'
