"""
Created on 11 Jun 2026

@author: Bruno Beloff (bbeloff@me.com)

The state of a command station

A DCC control router, initially based on the Roco Z21 digital control centre:
https://www.roco.cc/ren/products/control/digital-control-devices/10820-z21-digital-control-centre.html

Based on code:
https://github.com/botmonster/z21aio/tree/main
"""

from collections import OrderedDict

from mrcs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class ControlRouterReport(JSONable):
    """
    The state of a command station
    """


    @classmethod
    def construct_from_jdict(cls, jdict) -> ControlRouterReport | None:
        if not jdict:
            return None

        type_name = jdict.get('type')

        if type_name != cls.type_name():
            raise TypeError(f'required type:{cls.type_name()} got:{type_name}')

        main_current = jdict.get('main_current')
        prog_current = jdict.get('prog_current')
        filtered_main_current = jdict.get('filtered_main_current')
        supply_voltage = jdict.get('supply_voltage')
        track_voltage = jdict.get('track_voltage')

        temperature = jdict.get('temperature')

        central_state = jdict.get('central_state')
        central_state_ext = jdict.get('central_state_ext')
        capabilities = jdict.get('capabilities')
        reserved = jdict.get('reserved')

        return cls(main_current, prog_current, filtered_main_current,
                   supply_voltage, track_voltage, temperature,
                   central_state, central_state_ext, capabilities, reserved)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, main_current: int, prog_current: int, filtered_main_current: int,
                 supply_voltage: int, track_voltage: int, temperature: int,
                 central_state: int, central_state_ext: int, capabilities: int, reserved: int | None):
        self.__main_current = main_current  # mA
        self.__prog_current = prog_current  # mA
        self.__filtered_main_current = filtered_main_current  # mA
        self.__supply_voltage = supply_voltage  # mV
        self.__track_voltage = track_voltage  # mV

        self.__temperature = temperature  # °C

        self.__central_state = central_state  # bitmask
        self.__central_state_ext = central_state_ext  # bitmask
        self.__capabilities = capabilities  # bitmask
        self.__reserved = reserved


    def __eq__(self, other):
        try:
            return (self.main_current == other.main_current and self.prog_current == other.prog_current and
                    self.filtered_main_current == other.filtered_main_current and
                    self.supply_voltage == other.supply_voltage and self.track_voltage == other.track_voltage and
                    self.temperature == other.temperature and
                    self.central_state == other.central_state and self.central_state_ext == other.central_state_ext and
                    self.capabilities == other.capabilities and self.reserved == other.reserved)
        except (AttributeError, TypeError):
            return False


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        jdict = OrderedDict()

        jdict['type'] = self.type_name()

        jdict['main_current'] = self.main_current
        jdict['prog_current'] = self.prog_current
        jdict['filtered_main_current'] = self.filtered_main_current
        jdict['supply_voltage'] = self.supply_voltage
        jdict['track_voltage'] = self.track_voltage

        jdict['temperature'] = self.temperature

        jdict['central_state'] = self.central_state
        jdict['central_state_ext'] = self.central_state_ext
        jdict['capabilities'] = self.capabilities
        jdict['reserved'] = self.reserved

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def is_track_voltage_off(self) -> bool:
        return bool(self.central_state & 0x02)


    @property
    def is_short_circuit(self) -> bool:
        return bool(self.central_state & 0x04)


    @property
    def is_programming_mode(self) -> bool:
        return bool(self.central_state & 0x20)


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def main_current(self):
        return self.__main_current


    @property
    def prog_current(self):
        return self.__prog_current


    @property
    def filtered_main_current(self):
        return self.__filtered_main_current


    @property
    def supply_voltage(self):
        return self.__supply_voltage


    @property
    def track_voltage(self):
        return self.__track_voltage


    @property
    def temperature(self):
        return self.__temperature


    @property
    def central_state(self):
        return self.__central_state


    @property
    def central_state_ext(self):
        return self.__central_state_ext


    @property
    def capabilities(self):
        return self.__capabilities


    @property
    def reserved(self):
        return self.__reserved


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return (
            f'{self.__class__.__name__}:{{main_current:{self.main_current}, prog_current:{self.prog_current}, '
            f'filtered_main_current:{self.filtered_main_current}, supply_voltage:{self.supply_voltage}, '
            f'track_voltage:{self.track_voltage}, temperature:{self.temperature}, '
            f'central_state:0x{self.central_state:02x}, central_state_ext:0x{self.central_state_ext:02x}, '
            f'capabilities:0x{self.capabilities:02x}, reserved:0x{self.reserved:02x}}}')
