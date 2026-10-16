"""
Created on 16 Oct 2026

@author: Bruno Beloff (bbeloff@me.com)

Equipment identifiers

https://docs.python.org/3/howto/enum.html
"""

from enum import IntEnum, StrEnum, unique
from typing import Any

from mrcs_core.data.meta_enum import MetaEnum


# --------------------------------------------------------------------------------------------------------------------

@unique
class EquipmentType(StrEnum, metaclass=MetaEnum):
    """
    An enumeration of all the possible equipment types
    """

    API = 'API'  # infrastructure: MRCS Web API
    CLK = 'CLK'  # infrastructure: clock: cron, crontab, etc.
    CRT = 'CRT'  # infrastructure: control router
    REC = 'REC'  # infrastructure: message recorder
    CLU = 'CLU'  # infrastructure: command-line utility
    TST = 'TST'  # infrastructure: test equipment

    DCP = 'DCP'  # operations: decoupler
    LGP = 'LGP'  # operations: lighting group
    LVL = 'LVL'  # operations: level crossing
    MPU = 'MPU'  # operations: motive power unit
    SCH = 'SCH'  # operations: schedule controller
    SIG = 'SIG'  # operations: signal
    TEL = 'TEL'  # operations: motive power unit telemetry
    TRK = 'TRK'  # operations: track: block, track, turnout
    TRS = 'TRS'  # operations: train set (may be multi-headed)

    BOS = 'BOS'  # sensor: block occupancy detector
    LID = 'LID'  # sensor: LiDAR
    VIS = 'VIS'  # sensor: vision


    def __lt__(self, other: Any):
        return self.value < other.value


# --------------------------------------------------------------------------------------------------------------------

@unique
class CLU(IntEnum, metaclass=MetaEnum):
    """
    An enumeration of all the possible CLU equipment types
    """

    SUBSCRIBER = 1  # infrastructure: mrcs_control_subscriber CLU
    COMMANDER = 2  # infrastructure: mrcs_control_command CLU
    LAYOUT_MANAGER = 4  # infrastructure: mrcs_control_layout CLU
    INVENTORY_MANAGER = 3  # infrastructure: mrcs_control_inventory CLU


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return f'{self.name}{{{self.value}}}'


# --------------------------------------------------------------------------------------------------------------------

@unique
class CLK(IntEnum, metaclass=MetaEnum):
    """
    An enumeration of all the CLK equipment types
    """

    CRON = 1  # infrastructure: CronNode
    CRONTAB = 2  # infrastructure: CrontabNode
    CLOCK_CONF = 3  # infrastructure: ClockConfNode
    CLOCK_MANAGER = 4  # infrastructure: ClockManagerNode


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return f'{self.name}{{{self.value}}}'
