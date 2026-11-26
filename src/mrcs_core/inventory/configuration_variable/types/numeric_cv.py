"""
Created on 10 Oct 2026

@author: Bruno Beloff (bbeloff@me.com)

The default configuration variable type

{
    "type": "NumericCV",
    "addr": "ACCELERATION",
    "value": 5
}
"""

from collections import OrderedDict
from typing import Any, Self

from mrcs_core.equipment.conviguration_variable.cv_report import CVReport
from mrcs_core.inventory.configuration_variable.cv_address import CVAddress
from mrcs_core.inventory.configuration_variable.types.cv import CV


# --------------------------------------------------------------------------------------------------------------------

class NumericCV(CV):
    """
    the default configuration variable type
    """


    @classmethod
    def construct_from_report(cls, report: CVReport) -> Self:
        address = CVAddress(report.address)  # may raise KeyError

        return cls(address, report.value)


    @classmethod
    def construct_from_jdict(cls, jdict) -> Self:
        try:
            # may raise KeyError
            address = CVAddress[jdict.get('addr')]
            value = int(jdict.get('value'))

        except (TypeError, ValueError):
            raise ValueError(jdict)

        return cls(address, value)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, address: CVAddress, value: int):
        super().__init__(address)
        self.__value = value


    def __eq__(self, other: Any):
        try:
            return self.address == other.address and self.value == other.value
        except (AttributeError, TypeError):
            return False


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        jdict = OrderedDict()

        jdict['type'] = self.type_name()

        jdict['addr'] = self.address
        jdict['value'] = self.value

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def value(self) -> int:
        return self.__value


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return f'NumericCV{{address:{self.address}, value:{self.value}}}'
