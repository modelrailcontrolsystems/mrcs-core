"""
Created on 9 Jul 2026

@author: Bruno Beloff (bbeloff@me.com)

A component of a Block
"""

from abc import ABC, abstractmethod
from collections import OrderedDict

from mrcs_core.data.json import JSONable
from mrcs_core.equipment.turnout.turnout_configuration import TurnoutConfiguration
from mrcs_core.inventory.segment.segment_link import SegmentLink, SimpleSegmentLink, SwitchedSegmentLink


# --------------------------------------------------------------------------------------------------------------------

class Segment(JSONable, ABC):
    """
    An abstract componet of a Block
    """


    @classmethod
    def construct_from_jdict(cls, jdict) -> Segment:
        type_name = jdict.get('type')

        if type_name == TrackSegment.type_name():
            return TrackSegment.construct_from_jdict(jdict)

        if type_name == TurnoutSegment.type_name():
            return TurnoutSegment.construct_from_jdict(jdict)

        raise TypeError(f'invalid segment type: {type_name}')


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, label: str, length: int):
        self.__label = label
        self.__length = length  # mm


    # ----------------------------------------------------------------------------------------------------------------

    def up_link_for_config(self, config: TurnoutConfiguration) -> SegmentLink | None:
        up_link = self.up_link

        if up_link is None:
            return None

        return up_link.link_for_config(config.position(self.label))


    def down_link_for_config(self, config: TurnoutConfiguration) -> SegmentLink | None:
        down_link = self.down_link

        if down_link is None:
            return None

        return down_link.link_for_config(config.position(self.label))


    # ----------------------------------------------------------------------------------------------------------------

    @property
    @abstractmethod
    def up_link(self):
        pass


    @property
    @abstractmethod
    def down_link(self):
        pass


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def label(self):
        return self.__label


    @property
    def length(self):
        return self.__length


# --------------------------------------------------------------------------------------------------------------------

class TrackSegment(Segment):
    """
    A track component of a Block
    """


    @classmethod
    def construct_from_jdict(cls, jdict) -> TrackSegment:
        type_name = jdict.get('type')

        if type_name != cls.type_name():
            raise TypeError(f'required type:{cls.type_name()} got:{type_name}')

        label = jdict.get('label')
        length = jdict.get('length')

        up_link = SimpleSegmentLink.construct_from_jdict(jdict.get('up'))
        down_link = SimpleSegmentLink.construct_from_jdict(jdict.get('down'))

        return cls(label, length, up_link, down_link)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, label: str, length: int,
                 up_link: SimpleSegmentLink | None, down_link: SimpleSegmentLink | None):
        super().__init__(label, length)

        self.__up_link = up_link
        self.__down_link = down_link


    def __eq__(self, other):
        try:
            return (self.label == other.label and self.length == other.length and
                    self.up_link == other.up_link and self.down_link == other.down_link)
        except (AttributeError, TypeError):
            return False


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        jdict = OrderedDict()

        jdict['type'] = self.type_name()

        jdict['label'] = self.label
        jdict['length'] = self.length

        jdict['up'] = self.up_link
        jdict['down'] = self.down_link

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def up_link(self):
        return self.__up_link


    @property
    def down_link(self):
        return self.__down_link


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return (f'TrackSegment:{{label:{self.label}, length:{self.length}, '
                f'up_link:{self.up_link}, down_link:{self.down_link}}}')


# --------------------------------------------------------------------------------------------------------------------

class TurnoutSegment(Segment):
    """
    A turnout component of a Block
    """


    @classmethod
    def construct_from_jdict(cls, jdict) -> TurnoutSegment:
        type_name = jdict.get('type')

        if type_name != cls.type_name():
            raise TypeError(f'required type:{cls.type_name()} got:{type_name}')

        label = jdict.get('label')
        length = jdict.get('length')

        turnout_address = jdict.get('addr')
        switch_is_up = jdict.get('switch_is_up')
        simple_link = SimpleSegmentLink.construct_from_jdict(jdict.get('simple'))
        switched_link = SwitchedSegmentLink.construct_from_jdict(jdict.get('switched'))

        return cls(label, length, turnout_address, switch_is_up, simple_link, switched_link)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, label: str, length: int, turnout_address: int, switch_is_up: bool,
                 simple_link: SimpleSegmentLink | None, switched_link: SwitchedSegmentLink | None):
        super().__init__(label, length)

        self.__turnout_address = turnout_address
        self.__switch_is_up = switch_is_up

        self.__simple_link = simple_link
        self.__switched_link = switched_link


    def __eq__(self, other):
        try:
            return (self.label == other.label and self.length == other.length and
                    self.turnout_address == other.turnout_address and self.switch_is_up == other.switch_is_up and
                    self.up_link == other.up_link and self.down_link == other.down_link)
        except (AttributeError, TypeError):
            return False


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        jdict = OrderedDict()

        jdict['type'] = self.type_name()

        jdict['label'] = self.label
        jdict['length'] = self.length

        jdict['addr'] = self.turnout_address
        jdict['switch_is_up'] = self.switch_is_up
        jdict['simple'] = self.simple_link
        jdict['switched'] = self.switched_link

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def up_link(self):
        return self.switched_link if self.switch_is_up else self.simple_link


    @property
    def down_link(self):
        return self.simple_link if self.switch_is_up else self.switched_link


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def turnout_address(self):
        return self.__turnout_address


    @property
    def switch_is_up(self):
        return self.__switch_is_up


    @property
    def simple_link(self):
        return self.__simple_link


    @property
    def switched_link(self):
        return self.__switched_link


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return (f'TurnoutSegment:{{label:{self.label}, length:{self.length}, '
                f'turnout_address:{self.turnout_address}, switch_is_up:{self.switch_is_up}, '
                f'simple_link:{self.simple_link}, switched_link:{self.switched_link}}}')
