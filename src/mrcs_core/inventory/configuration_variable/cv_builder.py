"""
Created on 10 Oct 2026

@author: Bruno Beloff (bbeloff@me.com)

Factory methods for all inventory CV types
"""

from mrcs_core.equipment.conviguration_variable.cv_report import CVReport
from mrcs_core.inventory.configuration_variable import CVMetadata
from mrcs_core.inventory.configuration_variable.cv_address import CVAddress
from mrcs_core.inventory.configuration_variable.types.configuration_cv import ConfigurationCV
from mrcs_core.inventory.configuration_variable.types.consist_cv import ConsistCV
from mrcs_core.inventory.configuration_variable.types.cv import CV
from mrcs_core.inventory.configuration_variable.types.manufacturer_cv import ManufacturerCV
from mrcs_core.inventory.configuration_variable.types.numeric_cv import NumericCV
from mrcs_core.inventory.configuration_variable.types.railcom_cv import RailcomCV


# --------------------------------------------------------------------------------------------------------------------

class CVBuilder(object):
    """
    Factory methods for all inventory CV types
    """


    @classmethod
    def construct_from_report(cls, report: CVReport) -> CV:
        try:
            address = CVAddress(report.address)
        except ValueError:
            raise TypeError(report)

        cv_meta = CVMetadata.find(address)  # May raise ValueError

        return cv_meta.cv_type.construct_from_report(report)


    @classmethod
    def construct_from_jdict(cls, jdict) -> CV:
        type_name = jdict.get('type')

        if type_name == ConfigurationCV.type_name():
            return ConfigurationCV.construct_from_jdict(jdict)

        if type_name == ConsistCV.type_name():
            return ConsistCV.construct_from_jdict(jdict)

        if type_name == ManufacturerCV.type_name():
            return ManufacturerCV.construct_from_jdict(jdict)

        if type_name == NumericCV.type_name():
            return NumericCV.construct_from_jdict(jdict)

        if type_name == RailcomCV.type_name():
            return RailcomCV.construct_from_jdict(jdict)

        raise TypeError(f'invalid cv: {jdict}')
