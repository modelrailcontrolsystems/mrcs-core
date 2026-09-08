"""
Created on 6 Sep 2026

@author: Bruno Beloff (bbeloff@me.com)

A DCC motive power unit (MPU) aspect: its speed, heading, and location (distance to end of block)
The label of the MPUAspect is found from the MPU Inventory
"""

from collections import OrderedDict
from typing import Any, Self

from mrcs_core.data.json import JSONable
from mrcs_core.equipment.block.block_enums import BlockDirection


# TODO: replace direction field with Occupancy facing and Block direction, and calculate heading?
# --------------------------------------------------------------------------------------------------------------------

class MPUAspect(JSONable):
    """
    A DCC motive power unit (MPU) aspect
    """


    @classmethod
    def construct_from_jdict(cls, jdict) -> Self:
        label = jdict.get('label')
        mpu_address = jdict.get('addr')
        speed = jdict.get('speed')
        direction = BlockDirection[jdict.get('direction')]
        location = jdict.get('location')

        return cls(label, mpu_address, speed, direction, location)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, label: str, mpu_address: int, speed: int | None, direction: BlockDirection, location: int):
        self._label = label
        self._mpu_address = mpu_address
        self._speed = speed
        self._direction = direction
        self._location = location


    def __eq__(self, other: Any):
        try:
            return (self.label == other.label and self.mpu_address == other.mpu_address and
                    self.speed == other.speed and self.direction == other.direction and
                    self.location == other.location)
        except (AttributeError, TypeError):
            return False


    def __lt__(self, other: Any):
        return self.label < other.label


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        jdict = OrderedDict()

        jdict['type'] = self.type_name()

        jdict['label'] = self.label
        jdict['addr'] = self.mpu_address
        jdict['speed'] = self.speed
        jdict['direction'] = self.direction.name
        jdict['location'] = self.location

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def label(self):
        return self._label


    @property
    def mpu_address(self):
        return self._mpu_address


    @property
    def speed(self):
        return self._speed


    @property
    def direction(self):
        return self._direction


    @property
    def location(self):
        return self._location


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return (f'{self.__class__.__name__}:{{label:{self.label}, mpu_address:{self.mpu_address}, '
                f'speed:{self.speed}, direction:{self.direction}, location:{self.location}}}')
