"""
Created on 7 Oct 2026

@author: Bruno Beloff (bbeloff@me.com)

An abstract configuration variable
"""

from abc import ABC, abstractproperty

from mrcs_core.data.json import JSONable
from mrcs_core.equipment.conviguration_variable.cv_report import CVReport
from mrcs_core.inventory.configuration_variable.cv_address import CVAddress
from mrcs_core.inventory.manufacturer.manufacturer import Manufacturer


# --------------------------------------------------------------------------------------------------------------------

class CV(JSONable, ABC):
    """
    A configuration variable
    """


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, address: CVAddress):
        self.__address = address


    # ----------------------------------------------------------------------------------------------------------------

    def may_be_written_to(self, decoder: Manufacturer | None):
        from mrcs_core.inventory.configuration_variable import CVMetadata  # late import


        cv_metadata = CVMetadata.find(self.address)
        return cv_metadata.may_be_written_to(decoder)


    # ----------------------------------------------------------------------------------------------------------------

    def as_report(self):
        return CVReport(self.address.value, self.value)


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def address(self):
        return self.__address


    @abstractproperty
    def value(self) -> int:
        pass
