"""
Created on 10 Oct 2026

@author: Bruno Beloff (bbeloff@me.com)

Configuration variable type for MANUFACTURER_ID

{
    "type": "ManufacturerCV",
    "addr": "MANUFACTURER_ID",
    "mfr": "ZIMO"
}
"""

from collections import OrderedDict
from typing import Any, Self

from mrcs_core.equipment.conviguration_variable.cv_report import CVReport
from mrcs_core.inventory.configuration_variable.cv_address import CVAddress
from mrcs_core.inventory.configuration_variable.types.cv import CV
from mrcs_core.inventory.manufacturer.manufacturer import Manufacturer


# --------------------------------------------------------------------------------------------------------------------

class ManufacturerCV(CV):
    """
    configuration variable type for MANUFACTURER_ID
    """


    @classmethod
    def construct_from_report(cls, report: CVReport) -> Self:
        address = CVAddress(report.address)  # may raise KeyError
        manufacturer = Manufacturer(report.value)  # may raise KeyError
        return cls(address, manufacturer)


    @classmethod
    def construct_from_jdict(cls, jdict) -> Self:
        try:
            address = CVAddress[jdict.get('addr')]  # may raise KeyError
            manufacturer = Manufacturer[jdict.get('mfr')]  # may raise KeyError

        except (TypeError, ValueError):
            raise ValueError(jdict)

        return cls(address, manufacturer)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, address: CVAddress, manufacturer: Manufacturer):
        super().__init__(address)
        self.__manufacturer = manufacturer


    def __eq__(self, other: Any):
        try:
            return self.address == other.address and self.manufacturer == other.manufacturer
        except (AttributeError, TypeError):
            return False


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        jdict = OrderedDict()

        jdict['type'] = self.type_name()

        jdict['addr'] = self.address
        jdict['mfr'] = self.manufacturer

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
        return f'ManufacturerCV{{address:{self.address}, manufacturer:{self.manufacturer}}}'
