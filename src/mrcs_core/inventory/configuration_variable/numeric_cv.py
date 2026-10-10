"""
Created on 10 Oct 2026

@author: Bruno Beloff (bbeloff@me.com)

Configuration variable for numeric values

{
    "type": "NumericCV",
    "addr": "ACCELERATION",
    "value": 5
}
"""

from collections import OrderedDict
from typing import Any, Self

from mrcs_core.equipment.conviguration_variable.cv_report import CVReport
from mrcs_core.inventory.configuration_variable.cv import CV
from mrcs_core.inventory.configuration_variable.cv_address import CVAddress


# --------------------------------------------------------------------------------------------------------------------

class NumericCV(CV):
    """
    Configuration variable for numeric values
    """


    @classmethod
    def construct_from_report(cls, report: CVReport) -> Self:
        cv_address = CVAddress(report.cv_address)  # may raise KeyError

        return cls(cv_address, report.value)


    @classmethod
    def construct_from_jdict(cls, jdict) -> Self:
        try:
            # may raise KeyError
            cv_address = CVAddress[jdict.get('addr')]
            value = int(jdict.get('value'))

        except (TypeError, ValueError):
            raise ValueError(jdict)

        return cls(cv_address, value)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, cv_address: CVAddress, value: int):
        super().__init__(cv_address)
        self.__value = value


    def __eq__(self, other: Any):
        try:
            return self.cv_address == other.cv_address and self.value == other.value
        except (AttributeError, TypeError):
            return False


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        jdict = OrderedDict()

        jdict['type'] = self.type_name()

        jdict['addr'] = self.cv_address.name
        jdict['value'] = self.value

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def value(self) -> int:
        return self.__value


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return f'NumericCV{{cv_address:{self.cv_address}, value:{self.value}}}'
