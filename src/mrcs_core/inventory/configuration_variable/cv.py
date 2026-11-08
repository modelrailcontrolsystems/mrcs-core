"""
Created on 7 Oct 2026

@author: Bruno Beloff (bbeloff@me.com)

An abstract configuration variable
"""

from abc import ABC, abstractmethod, abstractproperty
from typing import Self

from mrcs_core.data.json import JSONable
from mrcs_core.equipment.conviguration_variable.cv_report import CVReport
from mrcs_core.inventory.configuration_variable.cv_address import CVAddress
from mrcs_core.inventory.motive_power_unit.manufacturer import Manufacturer


# --------------------------------------------------------------------------------------------------------------------

class CV(JSONable, ABC):
    """
    A configuration variable
    """

    __WRITEABLE_WHITELISTS = {
        Manufacturer.ZIMO_ELEKTRONIK: [CVAddress.ZIMO_SPEED_CALIBRATION],
        Manufacturer.ELECTRONIC_SOLUTIONS_ULM_GMBH: [CVAddress.ESU_CONTROL_VOLTAGE]
    }

    __WRITEABLE_BLACKLIST = (
        CVAddress.MANUFACTURER_VERSION,
        CVAddress.MANUFACTURER_ID,
        CVAddress.ZIMO_SPEED_CALIBRATION,
        CVAddress.ESU_CONTROL_VOLTAGE,
    )


    @classmethod
    def writeable_whitelist(cls, decoder: Manufacturer | None) -> list[CVAddress]:
        if decoder is None:
            return []

        try:
            return cls.__WRITEABLE_WHITELISTS[decoder]
        except KeyError:
            return []


    @classmethod
    def writeable_blacklist(cls):
        return cls.__WRITEABLE_BLACKLIST


    @classmethod
    @abstractmethod
    def construct_from_report(cls, report: CVReport) -> Self:
        pass


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, cv_address: CVAddress):
        self.__cv_address = cv_address


    # ----------------------------------------------------------------------------------------------------------------

    def is_writeable(self, decoder: Manufacturer | None):
        if self.cv_address in self.writeable_whitelist(decoder):
            return True

        return self.cv_address not in self.writeable_blacklist()


    # ----------------------------------------------------------------------------------------------------------------

    def as_report(self):
        return CVReport(self.cv_address.value, self.value)


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def cv_address(self):
        return self.__cv_address


    @abstractproperty
    def value(self) -> int:
        pass
