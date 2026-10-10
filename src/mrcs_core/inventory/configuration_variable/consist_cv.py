"""
Created on 7 Oct 2026

@author: Bruno Beloff (bbeloff@me.com)

Configuration variable for CONSIST_ADDRESS

{
    "type": "ConsistCV",
    "addr": "CONSIST_ADDRESS",
    "reverse": true,
    "consist_address": 27
}
"""

from collections import OrderedDict
from typing import Any, Self

from mrcs_core.equipment.conviguration_variable.cv_report import CVReport
from mrcs_core.inventory.configuration_variable.cv import CV, CVAddress


# --------------------------------------------------------------------------------------------------------------------

class ConsistCV(CV):
    """
    Configuration variable for CONSIST_ADDRESS
    """


    @classmethod
    def construct_from_jdict(cls, jdict) -> Self:
        try:
            cv_address = CVAddress[jdict.get('addr')]  # may raise KeyError

            if cv_address != CVAddress.CONSIST_ADDRESS:
                raise ValueError(jdict)

            reverse = bool(jdict.get('reverse'))
            consist_address = int(jdict.get('consist_address'))

        except (TypeError, ValueError):
            raise ValueError(jdict)

        return cls(cv_address, reverse, consist_address)


    @classmethod
    def construct_from_report(cls, report: CVReport) -> Self:
        cv_address = CVAddress(report.cv_address)  # may raise KeyError

        if cv_address != CVAddress.CONSIST_ADDRESS:
            raise ValueError(report)

        reverse = bool(report.value & 0x80)
        consist_address = report.value & 0x7f

        return cls(cv_address, reverse, consist_address)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, cv_address: CVAddress, reverse: bool, consist_address: int):
        super().__init__(cv_address)

        self.__reverse = reverse
        self.__consist_address = consist_address


    def __eq__(self, other: Any):
        try:
            return (self.cv_address == other.cv_address and self.reverse == other.reverse and
                    self.consist_address == other.consist_address)
        except (AttributeError, TypeError):
            return False


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        jdict = OrderedDict()

        jdict['type'] = self.type_name()

        jdict['addr'] = self.cv_address.name

        jdict['reverse'] = self.reverse
        jdict['consist_address'] = self.consist_address

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def value(self) -> int:
        value = self.consist_address

        if self.reverse:
            value += 0x80

        return value


    @property
    def reverse(self):
        return self.__reverse


    @property
    def consist_address(self):
        return self.__consist_address


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return (f'ConsistCV{{cv_address:{self.cv_address}, reverse:{self.reverse}, '
                f'consist_address:{self.consist_address}}}')
