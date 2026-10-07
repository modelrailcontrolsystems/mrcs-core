"""
Created on 4 Oct 2026

@author: Bruno Beloff (bbeloff@me.com)

A compendium of motive power unit (MPU) status objects

The intended use of the MPUAbstract is to populate an empty MPU database table. To this end, it should provide
MPUStatus objects which have identity, but no information about the physical state of each MPU.
"""

from typing import Any, List, Self

from mrcs_core.data.json import JSONable
from mrcs_core.equipment.motive_power_unit.mpu_status import MPUStatus


# --------------------------------------------------------------------------------------------------------------------

class MPUAbstract(JSONable):
    """
    a compendium of motive power unit (MPU) status objects
    """


    @classmethod
    def construct_from_jdict(cls, jdict: Any) -> Self:
        items = [MPUStatus.construct_from_jdict(item) for item in jdict]
        return cls(items)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, items: List[MPUStatus]):
        super().__init__()
        self.__items = items


    def __len__(self):
        return len(self.__items)


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        return self.items


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def items(self):
        return self.__items


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        items = '[' + ', '.join(str(item) for item in self.items) + ']'
        return f'MPUAbstract:{{items:{items}}}'
