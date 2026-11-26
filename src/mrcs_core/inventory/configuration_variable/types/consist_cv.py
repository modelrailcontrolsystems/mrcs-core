"""
Created on 7 Oct 2026

@author: Bruno Beloff (bbeloff@me.com)

Configuration variable type for CONSIST_ADDRESS

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
from mrcs_core.inventory.configuration_variable.cv_address import CVAddress
from mrcs_core.inventory.configuration_variable.types.cv import CV


# --------------------------------------------------------------------------------------------------------------------

class ConsistCV(CV):
    """
    configuration variable type for CONSIST_ADDRESS
    """


    @classmethod
    def construct_from_jdict(cls, jdict) -> Self:
        try:
            address = CVAddress[jdict.get('addr')]  # may raise KeyError

            if address != CVAddress.CONSIST_ADDRESS:
                raise ValueError(jdict)

            reverse = bool(jdict.get('reverse'))
            consist_address = int(jdict.get('consist_address'))

        except (TypeError, ValueError):
            raise ValueError(jdict)

        return cls(address, reverse, consist_address)


    @classmethod
    def construct_from_report(cls, report: CVReport) -> Self:
        address = CVAddress(report.address)  # may raise KeyError

        if address != CVAddress.CONSIST_ADDRESS:
            raise ValueError(report)

        reverse = bool(report.value & 0x80)
        consist_address = report.value & 0x7f

        return cls(address, reverse, consist_address)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, address: CVAddress, reverse: bool, consist_address: int):
        super().__init__(address)

        self.__reverse = reverse
        self.__consist_address = consist_address


    def __eq__(self, other: Any):
        try:
            return (self.address == other.address and self.reverse == other.reverse and
                    self.consist_address == other.consist_address)
        except (AttributeError, TypeError):
            return False


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        jdict = OrderedDict()

        jdict['type'] = self.type_name()

        jdict['addr'] = self.address

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
        return (f'ConsistCV{{address:{self.address}, reverse:{self.reverse}, '
                f'consist_address:{self.consist_address}}}')
