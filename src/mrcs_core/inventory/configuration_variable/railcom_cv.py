"""
Created on 7 Oct 2026

@author: Bruno Beloff (bbeloff@me.com)

Configuration variable for RAILCOM

{
    "type": "RailcomCV",
    "addr": "RAILCOM",
    "ch1_broadcast": true,
    "ch2_broadcast": true,
    "auto_ch1": false,
    "enable_addr_3l": false,
    "current_limit": false,
    "railcom_login": true
}
"""

from collections import OrderedDict
from typing import Any, Self

from mrcs_core.equipment.conviguration_variable.cv_report import CVReport
from mrcs_core.inventory.configuration_variable.cv import CV, CVAddress


# --------------------------------------------------------------------------------------------------------------------

class RailcomCV(CV):
    """
    Configuration variable for RAILCOM
    """


    @classmethod
    def construct_from_jdict(cls, jdict) -> Self:
        try:
            cv_address = CVAddress[jdict.get('addr')]  # may raise KeyError

            if cv_address != CVAddress.RAILCOM:
                raise ValueError(jdict)

            ch1_broadcast = bool(jdict.get('ch1_broadcast'))
            ch2_broadcast = bool(jdict.get('ch2_broadcast'))
            auto_ch1 = bool(jdict.get('auto_ch1'))
            enable_addr_3l = bool(jdict.get('enable_addr_3l'))
            current_limit = bool(jdict.get('current_limit'))
            railcom_login = bool(jdict.get('railcom_login'))

        except (TypeError, ValueError):
            raise ValueError(jdict)

        return cls(cv_address, ch1_broadcast, ch2_broadcast, auto_ch1, enable_addr_3l, current_limit, railcom_login)


    @classmethod
    def construct_from_report(cls, report: CVReport) -> Self:
        cv_address = CVAddress(report.cv_address)  # may raise KeyError

        if cv_address != CVAddress.RAILCOM:
            raise ValueError(report)

        ch1_broadcast = bool(report.value & 0x01)
        ch2_broadcast = bool(report.value & 0x02)
        auto_ch1 = bool(report.value & 0x04)
        enable_addr_3l = bool(report.value & 0x10)
        current_limit = bool(report.value & 0x40)
        railcom_login = bool(report.value & 0x80)

        return cls(cv_address, ch1_broadcast, ch2_broadcast, auto_ch1, enable_addr_3l, current_limit, railcom_login)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, cv_address: CVAddress, ch1_broadcast: bool, ch2_broadcast: bool, auto_ch1: bool,
                 enable_addr_3l: bool, current_limit: bool, railcom_login: bool):
        super().__init__(cv_address)

        self.__ch1_broadcast = ch1_broadcast
        self.__ch2_broadcast = ch2_broadcast
        self.__auto_ch1 = auto_ch1
        self.__enable_addr_3l = enable_addr_3l
        self.__current_limit = current_limit
        self.__railcom_login = railcom_login


    def __eq__(self, other: Any):
        try:
            return (self.cv_address == other.cv_address and self.ch1_broadcast == other.ch1_broadcast and
                    self.ch2_broadcast == other.ch2_broadcast and self.auto_ch1 == other.auto_ch1 and
                    self.enable_addr_3l == other.enable_addr_3l and self.current_limit == other.current_limit and
                    self.railcom_login == other.railcom_login)
        except (AttributeError, TypeError):
            return False


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        jdict = OrderedDict()

        jdict['type'] = self.type_name()

        jdict['addr'] = self.cv_address.name

        jdict['ch1_broadcast'] = self.ch1_broadcast
        jdict['ch2_broadcast'] = self.ch2_broadcast
        jdict['auto_ch1'] = self.auto_ch1
        jdict['enable_addr_3l'] = self.enable_addr_3l
        jdict['current_limit'] = self.current_limit
        jdict['railcom_login'] = self.railcom_login

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def value(self) -> int:
        value = 0

        if self.ch1_broadcast:
            value += 0x01
        if self.ch2_broadcast:
            value += 0x02
        if self.auto_ch1:
            value += 0x04
        if self.enable_addr_3l:
            value += 0x10
        if self.current_limit:
            value += 0x40
        if self.railcom_login:
            value += 0x80

        return value


    @property
    def ch1_broadcast(self):
        return self.__ch1_broadcast


    @property
    def ch2_broadcast(self):
        return self.__ch2_broadcast


    @property
    def auto_ch1(self):
        return self.__auto_ch1


    @property
    def enable_addr_3l(self):
        return self.__enable_addr_3l


    @property
    def current_limit(self):
        return self.__current_limit


    @property
    def railcom_login(self):
        return self.__railcom_login


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return (f'RailcomCV{{cv_address:{self.cv_address}, ch1_broadcast:{self.ch1_broadcast}, '
                f'ch2_broadcast:{self.ch2_broadcast}, auto_ch1:{self.auto_ch1}, enable_addr_3l:{self.enable_addr_3l}, '
                f'current_limit:{self.current_limit}, railcom_login:{self.railcom_login}}}')
