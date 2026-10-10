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


# --------------------------------------------------------------------------------------------------------------------

class CV(JSONable, ABC):
    """
    A configuration variable
    """


    @classmethod
    @abstractmethod
    def construct_from_report(cls, report: CVReport) -> Self:
        pass


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, cv_address: CVAddress):
        self.__cv_address = cv_address


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
