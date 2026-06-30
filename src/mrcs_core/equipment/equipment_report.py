"""
Created on 20 Jun 2026

@author: Bruno Beloff (bbeloff@me.com)

A constructor to unmarshall equipment reports from JSON

Classes in support of the Rocco Z21 DCC command station:
https://www.z21.eu/en/products/z21
"""

from mrcs_core.data.json import JSONable
from mrcs_core.equipment.block.block_report import BlockOccupancyReport, BlockStatusReport
from mrcs_core.equipment.control_router.control_router_state import ControlRouterState
from mrcs_core.equipment.motive_power_unit.motive_power_unit_decoder import MotivePowerUnitDecoder
from mrcs_core.equipment.motive_power_unit.motive_power_unit_state import MotivePowerUnitState
from mrcs_core.equipment.track.track_state import TrackState
from mrcs_core.equipment.turnout.turnout_state import TurnoutState


# --------------------------------------------------------------------------------------------------------------------

class EquipmentReport(object):
    """
    A constructor to unmarshall equipment reports from JSON
    """

    # TODO: make this an Enum, so that we can build a mapping from command (headers) to return types

    __TYPE_MAPPING = {
        'BlockOccupancyReport': BlockOccupancyReport,
        'BlockStatusReport': BlockStatusReport,
        'ControlRouterState': ControlRouterState,
        'MotivePowerUnitDecoder': MotivePowerUnitDecoder,
        'MotivePowerUnitState': MotivePowerUnitState,
        'TrackState': TrackState,
        'TurnoutState': TurnoutState
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
