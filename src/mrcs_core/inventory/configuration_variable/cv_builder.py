"""
Created on 10 Oct 2026

@author: Bruno Beloff (bbeloff@me.com)

Factory methods for all inventory CV types
"""

from mrcs_core.equipment.conviguration_variable.cv_report import CVReport
from mrcs_core.inventory.configuration_variable.configuration_cv import ConfigurationCV
from mrcs_core.inventory.configuration_variable.consist_cv import ConsistCV
from mrcs_core.inventory.configuration_variable.cv import CV
from mrcs_core.inventory.configuration_variable.cv_address import CVAddress
from mrcs_core.inventory.configuration_variable.numeric_cv import NumericCV
from mrcs_core.inventory.configuration_variable.railcom_cv import RailcomCV


# --------------------------------------------------------------------------------------------------------------------

class CVBuilder(object):
    """
    Factory methods for all inventory CV types
    """


    @classmethod
    def construct_from_report(cls, report: CVReport) -> CV:
        try:
            cv_address = CVAddress(report.cv_address)
        except ValueError:
            raise TypeError(report)

        if cv_address == CVAddress.CONFIGURATION:
            return ConfigurationCV.construct_from_report(report)

        if cv_address == CVAddress.CONSIST_ADDRESS:
            return ConsistCV.construct_from_report(report)

        if cv_address == CVAddress.RAILCOM:
            return RailcomCV.construct_from_report(report)

        return NumericCV.construct_from_report(report)


    @classmethod
    def construct_from_jdict(cls, jdict) -> CV:
        type_name = jdict.get('type')

        if type_name == ConfigurationCV.type_name():
            return ConfigurationCV.construct_from_jdict(jdict)

        if type_name == ConsistCV.type_name():
            return ConsistCV.construct_from_jdict(jdict)

        if type_name == NumericCV.type_name():
            return NumericCV.construct_from_jdict(jdict)

        if type_name == RailcomCV.type_name():
            return RailcomCV.construct_from_jdict(jdict)

        raise TypeError(f'invalid cv: {jdict}')
