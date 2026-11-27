"""
Created on 9 Oct 2026

@author: Bruno Beloff (bbeloff@me.com)

Common configuration variable (CV) supported addresses
"""

from enum import IntEnum, unique

from mrcs_core.data.json import JSONable
from mrcs_core.data.meta_enum import ABCMetaEnum


# --------------------------------------------------------------------------------------------------------------------

@unique
class CVAddress(JSONable, IntEnum, metaclass=ABCMetaEnum):
    """
    Common configuration variable (CV) supported addresses
    """

    SHORT_ADDRESS = 1  # 1 - 127 (3)
    START_VOLTAGE = 2  # 1 - 255 (3)
    ACCELERATION = 3  # 0 - 255 (80)
    DECELERATION = 4  # 0 - 255 (80)
    MAX_SPEED = 5  # 0 - 255 (255)
    MID_SPEED = 6  # 0 - 255 (88)
    MANUFACTURER_VERSION = 7
    MANUFACTURER_ID = 8  # Revolution: write to factory reset
    MOTOR_PWM_FREQUENCY = 9  # 10 - 50 (40)
    CONSIST_ADDRESS = 19  # structured, 0 or 128 - disabled (0)
    RAILCOM = 28  # structured, (131)
    CONFIGURATION = 29  # structured, (12)

    ESU_CONTROL_VOLTAGE = 53  # 0 - 255 (0)
    ESU_MASTER_VOLUME = 63  # 0 – 192 (80)

    ZIMO_PID_REGULATION = 56  # 1 - 199 (199)
    ZIMO_BACK_EMF_LOAD = 58  # 0 - 255 (255)
    ZIMO_PWM_FREQUENCY = 112  # 0 - 255 (0)
    ZIMO_SPEED_CALIBRATION = 136  # 0 - 255 (0)
    ZIMO_MASTER_VOLUME = 266  # 0 - 255 (65)


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        return self.name


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return f'{self.name}{{{self.value}}}'
