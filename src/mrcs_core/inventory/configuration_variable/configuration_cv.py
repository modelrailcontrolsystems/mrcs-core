"""
Created on 10 Oct 2026

@author: Bruno Beloff (bbeloff@me.com)

Configuration variable for RAILCOM

{
    "type": "ConfigurationCV",
    "addr": "CONFIGURATION",
    "reverse": false,
    "speed_128": true,
    "analog_enabled": false,
    "railcom_enabled": true,
    "speed_curve": false,
    "long_address": false,
    "accessory_decoder": false
}
"""

from collections import OrderedDict
from typing import Any, Self

from mrcs_core.equipment.conviguration_variable.cv_report import CVReport
from mrcs_core.inventory.configuration_variable.cv import CV, CVAddress


# --------------------------------------------------------------------------------------------------------------------

class ConfigurationCV(CV):
    """
    Configuration variable for CONFIGURATION
    """


    @classmethod
    def construct_from_jdict(cls, jdict) -> Self:
        try:
            cv_address = CVAddress[jdict.get('addr')]  # may raise KeyError

            if cv_address != CVAddress.CONFIGURATION:
                raise ValueError(jdict)

            reverse = bool(jdict.get('reverse'))
            speed_128 = bool(jdict.get('speed_128'))
            analog_enabled = bool(jdict.get('analog_enabled'))
            railcom_enabled = bool(jdict.get('railcom_enabled'))
            speed_curve = bool(jdict.get('speed_curve'))
            long_address = bool(jdict.get('long_address'))
            accessory_decoder = bool(jdict.get('accessory_decoder'))

        except (TypeError, ValueError):
            raise ValueError(jdict)

        return cls(cv_address, reverse, speed_128, analog_enabled, railcom_enabled, speed_curve, long_address,
                   accessory_decoder)


    @classmethod
    def construct_from_report(cls, report: CVReport) -> Self:
        cv_address = CVAddress(report.cv_address)  # may raise KeyError

        if cv_address != CVAddress.CONFIGURATION:
            raise ValueError(report)

        reverse = bool(report.value & 0x01)
        speed_128 = bool(report.value & 0x02)
        analog_enabled = bool(report.value & 0x04)
        railcom_enabled = bool(report.value & 0x08)
        speed_curve = bool(report.value & 0x10)
        long_address = bool(report.value & 0x20)
        accessory_decoder = bool(report.value & 0x80)

        return cls(cv_address, reverse, speed_128, analog_enabled, railcom_enabled, speed_curve, long_address,
                   accessory_decoder)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, cv_address: CVAddress, reverse: bool, speed_128: bool, analog_enabled: bool,
                 railcom_enabled: bool, speed_curve: bool, long_address: bool, accessory_decoder: bool):
        super().__init__(cv_address)

        self.__reverse = reverse
        self.__speed_128 = speed_128
        self.__analog_enabled = analog_enabled
        self.__railcom_enabled = railcom_enabled
        self.__speed_curve = speed_curve
        self.__long_address = long_address
        self.__accessory_decoder = accessory_decoder


    def __eq__(self, other: Any):
        try:
            return (self.cv_address == other.cv_address and self.reverse == other.reverse and
                    self.speed_128 == other.speed_128 and self.analog_enabled == other.analog_enabled and
                    self.railcom_enabled == other.railcom_enabled and self.speed_curve == other.speed_curve and
                    self.long_address == other.long_address and self.accessory_decoder == other.accessory_decoder)
        except (AttributeError, TypeError):
            return False


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        jdict = OrderedDict()

        jdict['type'] = self.type_name()

        jdict['addr'] = self.cv_address.name

        jdict['reverse'] = self.reverse
        jdict['speed_128'] = self.speed_128
        jdict['analog_enabled'] = self.analog_enabled
        jdict['railcom_enabled'] = self.railcom_enabled
        jdict['speed_curve'] = self.speed_curve
        jdict['long_address'] = self.long_address
        jdict['accessory_decoder'] = self.accessory_decoder

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def value(self) -> int:
        value = 0

        if self.reverse:
            value += 0x01
        if self.speed_128:
            value += 0x02
        if self.analog_enabled:
            value += 0x04
        if self.railcom_enabled:
            value += 0x08
        if self.speed_curve:
            value += 0x10
        if self.long_address:
            value += 0x20
        if self.accessory_decoder:
            value += 0x80

        return value


    @property
    def reverse(self):
        return self.__reverse


    @property
    def speed_128(self):
        return self.__speed_128


    @property
    def analog_enabled(self):
        return self.__analog_enabled


    @property
    def railcom_enabled(self):
        return self.__railcom_enabled


    @property
    def speed_curve(self):
        return self.__speed_curve


    @property
    def long_address(self):
        return self.__long_address


    @property
    def accessory_decoder(self):
        return self.__accessory_decoder


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return (f'ConfigurationCV{{cv_address:{self.cv_address}, reverse:{self.reverse}, speed_128:{self.speed_128}, '
                f'analog_enabled:{self.analog_enabled}, railcom_enabled:{self.railcom_enabled}, '
                f'speed_curve:{self.speed_curve}, long_address:{self.long_address}, '
                f'accessory_decoder:{self.accessory_decoder}}}')
