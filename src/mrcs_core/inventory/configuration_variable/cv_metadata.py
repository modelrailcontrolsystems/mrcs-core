"""
Created on 26 Nov 2026

@author: Bruno Beloff (bbeloff@me.com)

Information that is common to each conviguration variable with a given CVAddress
"""

from typing import Dict, Type

from mrcs_core.inventory.configuration_variable.cv_address import CVAddress
from mrcs_core.inventory.configuration_variable.types.configuration_cv import ConfigurationCV
from mrcs_core.inventory.configuration_variable.types.consist_cv import ConsistCV
from mrcs_core.inventory.configuration_variable.types.manufacturer_cv import ManufacturerCV
from mrcs_core.inventory.configuration_variable.types.numeric_cv import NumericCV
from mrcs_core.inventory.configuration_variable.types.railcom_cv import RailcomCV
from mrcs_core.inventory.manufacturer.manufacturer import Manufacturer


# --------------------------------------------------------------------------------------------------------------------

class CVMetadata(object):
    """
    information that is common to each conviguration variable with a given CVAddress
    """

    __CATALOG: Dict[CVAddress, CVMetadata]


    @classmethod
    def init(cls):
        cls.__CATALOG = {
            CVAddress.SHORT_ADDRESS: cls(NumericCV, Manufacturer.ALL, Manufacturer.ALL),
            CVAddress.START_VOLTAGE: cls(NumericCV, Manufacturer.ALL, Manufacturer.ALL),
            CVAddress.ACCELERATION: cls(NumericCV, Manufacturer.ALL, Manufacturer.ALL),
            CVAddress.DECELERATION: cls(NumericCV, Manufacturer.ALL, Manufacturer.ALL),
            CVAddress.MAX_SPEED: cls(NumericCV, Manufacturer.ALL, Manufacturer.ALL),
            CVAddress.MID_SPEED: cls(NumericCV, Manufacturer.ALL, Manufacturer.ALL),
            CVAddress.MANUFACTURER_VERSION: cls(NumericCV, Manufacturer.ALL, None),
            CVAddress.MANUFACTURER_ID: cls(ManufacturerCV, Manufacturer.ALL, None),
            CVAddress.MOTOR_PWM_FREQUENCY: cls(NumericCV, Manufacturer.ALL, Manufacturer.ALL),
            CVAddress.CONSIST_ADDRESS: cls(ConsistCV, Manufacturer.ALL, Manufacturer.ALL),
            CVAddress.RAILCOM: cls(RailcomCV, Manufacturer.ALL, Manufacturer.ALL),
            CVAddress.CONFIGURATION: cls(ConfigurationCV, Manufacturer.ALL, Manufacturer.ALL),

            CVAddress.ESU_CONTROL_VOLTAGE: cls(NumericCV, Manufacturer.ELECTRONIC_SOLUTIONS_ULM_GMBH,
                                               Manufacturer.ELECTRONIC_SOLUTIONS_ULM_GMBH),
            CVAddress.ESU_MASTER_VOLUME: cls(NumericCV, Manufacturer.ELECTRONIC_SOLUTIONS_ULM_GMBH,
                                             Manufacturer.ELECTRONIC_SOLUTIONS_ULM_GMBH),

            CVAddress.ZIMO_PID_REGULATION: cls(NumericCV, Manufacturer.ZIMO_ELEKTRONIK,
                                               Manufacturer.ZIMO_ELEKTRONIK),
            CVAddress.ZIMO_BACK_EMF_LOAD: cls(NumericCV, Manufacturer.ZIMO_ELEKTRONIK,
                                              Manufacturer.ZIMO_ELEKTRONIK),
            CVAddress.ZIMO_PWM_FREQUENCY: cls(NumericCV, Manufacturer.ZIMO_ELEKTRONIK,
                                              Manufacturer.ZIMO_ELEKTRONIK),
            CVAddress.ZIMO_SPEED_CALIBRATION: cls(NumericCV, Manufacturer.ZIMO_ELEKTRONIK,
                                                  Manufacturer.ZIMO_ELEKTRONIK),
            CVAddress.ZIMO_MASTER_VOLUME: cls(NumericCV, Manufacturer.ZIMO_ELEKTRONIK,
                                              Manufacturer.ZIMO_ELEKTRONIK),
        }


    @classmethod
    def find(cls, address: CVAddress):
        try:
            return cls.__CATALOG[address]
        except KeyError:
            raise ValueError(address)


    # ----------------------------------------------------------------------------------------------------------------


    def __init__(self, cv_type: Type, may_read: Manufacturer, may_write: Manufacturer | None):
        self.__cv_type = cv_type
        self.__may_read = may_read
        self.__may_write = may_write


    # ----------------------------------------------------------------------------------------------------------------

    def may_be_read_from(self, decoder: Manufacturer | None) -> bool:
        if self.may_read == Manufacturer.ALL:
            return True

        return self.may_read == decoder


    def may_be_written_to(self, decoder: Manufacturer | None) -> bool:
        if self.may_write is None:
            return False

        if self.may_write == Manufacturer.ALL:
            return True

        return self.may_write == decoder


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def cv_type(self):
        return self.__cv_type


    @property
    def may_read(self):
        return self.__may_read


    @property
    def may_write(self):
        return self.__may_write


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        cv_type_name = self.cv_type.__name__
        return f'CVMetadata:{{cv_type_name:{cv_type_name}, may_read:{self.may_read}, may_write:{self.may_write}}}'
