"""
Created on 20 Jun 2026

@author: Bruno Beloff (bbeloff@me.com)

A constructor to unmarshall equipment reports from JSON

Classes in support of the Rocco Z21 DCC command station:
https://www.z21.eu/en/products/z21
"""

from mrcs_core.data.json import JSONable
from mrcs_core.equipment.block.block_report import BlockOccupancyReport, BlockStatusReport
from mrcs_core.equipment.control_router.control_router_report import ControlRouterReport
from mrcs_core.equipment.motive_power_unit.mpu_configuration_report import MPUConfigurationReport
from mrcs_core.equipment.motive_power_unit.mpu_decoder_report import MPUDecoderReport
from mrcs_core.equipment.track.track_report import TrackReport
from mrcs_core.equipment.turnout.turnout_report import TurnoutReport


# --------------------------------------------------------------------------------------------------------------------

class EquipmentReport(object):
    """
    A constructor to unmarshall equipment reports from JSON
    """

    __TYPE_MAPPING = {
        'BlockOccupancyReport': BlockOccupancyReport,
        'BlockStatusReport': BlockStatusReport,
        'ControlRouterReport': ControlRouterReport,
        'MPUDecoderReport': MPUDecoderReport,
        'MPUConfigurationReport': MPUConfigurationReport,
        'TrackReport': TrackReport,
        'TurnoutReport': TurnoutReport
    }


    @classmethod
    def __class_for_type_name(cls, type_name):
        # may raise KeyError
        return cls.__TYPE_MAPPING[type_name]


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict) -> JSONable | None:
        if not jdict:
            return None

        type_name = jdict.get('type')

        try:
            equipment_cls = cls.__class_for_type_name(type_name)
        except KeyError:
            raise TypeError(f'unsupported type_name:{type_name}')

        return equipment_cls.construct_from_jdict(jdict)
