"""
Created on 6 Nov 2025

@author: Bruno Beloff (bbeloff@me.com)

A structured record that uniquely identifies each piece of equipment

https://docs.python.org/3/howto/enum.html
"""

from abc import ABC
from enum import unique, StrEnum

from mrcs_core.data.json import JSONable
from mrcs_core.data.meta_enum import MetaEnum


# --------------------------------------------------------------------------------------------------------------------

@unique
class EquipmentType(StrEnum, metaclass=MetaEnum):
    """
    An enumeration of all the possible equipment types
    """

    API = 'API'         # infrastructure: MRCS Web API
    CRN = 'CRN'         # infrastructure: cron
    CRT = 'CRT'         # infrastructure: control router
    MLG = 'MLG'         # infrastructure: message logger
    TST = 'TST'         # infrastructure: test equipment

    DCP = 'DCP'         # operations: decoupler
    LGP = 'LGP'         # operations: lighting group
    LVL = 'LVL'         # operations: level crossing
    MPU = 'MPU'         # operations: motive power unit
    SCH = 'SCH'         # operations: schedule controller
    SIG = 'SIG'         # operations: signal
    TRN = 'TRN'         # operations: turnout (point)
    TRS = 'TRS'         # operations: train set (may be multi-headed)

    BOS = 'BOS'         # sensor: block occupancy
    LID = 'LID'         # sensor: LiDAR
    VIS = 'VIS'         # sensor: vision


# TODO: create int enums of equipment numbers (for CRN)
# --------------------------------------------------------------------------------------------------------------------

class EquipmentSpecification(JSONable, ABC):
    """
    An abstract specification of a piece of equipment, with type, sector ID, and within-sector serial number
    """

    def __init__(self, equipment_type: EquipmentType | None, sector_number: int | None, serial_number: int | None):
        self.__equipment_type = equipment_type
        self.__sector_number = sector_number
        self.__serial_number = serial_number


    def __eq__(self, other):
        try:
            return (self.equipment_type == other.equipment_type and self.sector_number == other.sector_number and
                    self.serial_number == other.serial_number)
        except (AttributeError, TypeError):
            return False


    def __lt__(self, other):
        if self.equipment_type != other.equipment_type:
            if self.equipment_type is None and other.equipment_type is not None:
                return True

            if self.equipment_type is not None and other.equipment_type is None:
                return False

            if self.equipment_type < other.equipment_type:
                return True

            if self.equipment_type > other.equipment_type:
                return False

        if self.sector_number != other.sector_number:
            if self.sector_number is None and other.sector_number is not None:
                return True

            if self.sector_number is not None and other.sector_number is None:
                return False

            if self.sector_number is None or self.sector_number < other.sector_number:
                return True

            if other.sector_number is None or self.sector_number > other.sector_number:
                return False

        if self.serial_number != other.serial_number:
            if self.serial_number is None and other.serial_number is not None:
                return True

            if self.serial_number is not None and other.serial_number is None:
                return False

            if self.serial_number < other.serial_number:
                return True

            if self.serial_number > other.serial_number:
                return False

        return False


    # ----------------------------------------------------------------------------------------------------------------

    def matches(self, other):
        try:
            return ((other.equipment_type is None or self.equipment_type == other.equipment_type) and
                    (other.sector_number is None or self.sector_number == other.sector_number) and
                    (other.serial_number is None or self.serial_number == other.serial_number))
        except (AttributeError, TypeError):
            return False


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def equipment_type(self):
        return self.__equipment_type


    @property
    def sector_number(self):
        return self.__sector_number


    @property
    def serial_number(self):
        return self.__serial_number


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return (f'{self.__class__.__name__}:{{equipment_type:{self.equipment_type}, '
                f'sector_number:{self.sector_number}, serial_number:{self.serial_number}}}')


# --------------------------------------------------------------------------------------------------------------------

class EquipmentIdentifier(EquipmentSpecification, JSONable):
    """
    A fully-specified equipment identifier, for use by publishers
    """

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        pieces = str(jdict).split('.')

        try:
            equipment_type = EquipmentType(pieces[0])
            sector_number = None if pieces[1] == '*' else int(pieces[1])
            serial_number = int(pieces[2])
        except ValueError:
            raise ValueError(jdict)

        return cls(equipment_type, sector_number, serial_number)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, equipment_type: EquipmentType, sector_number: int | None, serial_number: int):
        super().__init__(equipment_type, sector_number, serial_number)


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        equipment_type = self.equipment_type
        sector_number = '*' if self.sector_number is None else f'{self.sector_number:03d}'
        serial_number = f'{self.serial_number:03d}'

        return f'{equipment_type}.{sector_number}.{serial_number}'


# --------------------------------------------------------------------------------------------------------------------

class EquipmentFilter(EquipmentSpecification):
    """
    A partially-specified equipment identifier, for use by subscribers
    """

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        pieces = str(jdict).split('.')

        try:
            equipment_type = None if pieces[0] == '*' else EquipmentType(pieces[0])
            sector_number = None if pieces[1] == '*' else int(pieces[1])
            serial_number = None if pieces[2] == '*' else int(pieces[2])
        except ValueError:
            raise ValueError(jdict)

        return cls(equipment_type, sector_number, serial_number)


    @classmethod
    def construct(cls, equipment_type_spec: EquipmentType | None, sector_number_spec: int | None,
                  serial_number_spec: int | None):
        try:
            equipment_type = None if equipment_type_spec is None else EquipmentType(equipment_type_spec)
        except ValueError:
            raise ValueError(f'{equipment_type_spec} not in {list(EquipmentType.keys())}')

        sector_number = None if sector_number_spec is None else int(sector_number_spec)
        serial_number = None if serial_number_spec is None else int(serial_number_spec)

        return cls(equipment_type, sector_number, serial_number)


    @classmethod
    def any(cls):
        return cls(None, None, None)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, equipment_type: EquipmentType | None, sector_number: int | None, serial_number: int | None):
        super().__init__(equipment_type, sector_number, serial_number)


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        equipment_type = '*' if self.equipment_type is None else self.equipment_type
        sector_number = '*' if self.sector_number is None else f'{self.sector_number:03d}'
        serial_number = '*' if self.serial_number is None else f'{self.serial_number:03d}'

        return f'{equipment_type}.{sector_number}.{serial_number}'
