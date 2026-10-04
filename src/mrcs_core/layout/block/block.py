"""
Created on 9 Jul 2026

@author: Bruno Beloff (bbeloff@me.com)

A component of a Layout, monitored by a block detector
Blocks contain track and turnout segments. A Block may have a fixed direction, or may be reversible.
"""

from collections import OrderedDict
from typing import Any

from mrcs_core.data.json import JSONable
from mrcs_core.equipment.block.block_address import BlockAddress
from mrcs_core.equipment.block.block_enums import BlockHeading, BlockVoltage
from mrcs_core.equipment.block.block_status import BlockStatus
from mrcs_core.layout.block.block_operation import BlockOperation
from mrcs_core.layout.segment.segment import Segment
from mrcs_core.layout.segment.segment_builder import SegmentBuilder


# --------------------------------------------------------------------------------------------------------------------

class Block(JSONable):
    """
    A component of a layout, monitored by a block detector
    """


    @classmethod
    def construct_from_jdict(cls, jdict) -> Block:
        label = jdict.get('label')
        address = BlockAddress.construct_from_jdict(jdict.get('addr'))
        operation = BlockOperation(jdict.get('operation'))

        segments = OrderedDict()
        for segment_jdict in jdict.get('segments', []):
            segment = SegmentBuilder.construct_from_jdict(segment_jdict)
            segments[segment.label] = segment

        return cls(label, address, operation, segments)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, label: str, address: BlockAddress, operation: BlockOperation,
                 segments: OrderedDict[str, Segment]):
        self.__label = label
        self.__address = address
        self.__operation = operation
        self.__segments = segments


    def __eq__(self, other: Any):
        try:
            return self.label == other.label and self.address == other.address and self.segments == other.segments
        except (AttributeError, TypeError):
            return False


    def __lt__(self, other: Any):
        return self.label < other.label


    # ----------------------------------------------------------------------------------------------------------------

    def status(self):
        return BlockStatus(self.label, self.address, BlockHeading.UNASSIGNED, BlockVoltage.UNKNOWN)


    # ----------------------------------------------------------------------------------------------------------------

    def segment_report(self, segment_label: str | None) -> Block:
        try:
            segments = self.__segments if segment_label is None else {segment_label: self.__segments[segment_label]}
        except KeyError:
            raise KeyError(segment_label)

        return Block(self.label, self.address, self.operation, OrderedDict(segments))


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        jdict = OrderedDict()

        jdict['label'] = self.label
        jdict['addr'] = self.address
        jdict['operation'] = self.operation.name
        jdict['segments'] = self.segments

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def label(self):
        return self.__label


    @property
    def address(self):
        return self.__address


    @property
    def operation(self):
        return self.__operation


    @property
    def segments(self):
        return tuple(self.__segments.values())


    def segment(self, label):
        try:
            return self.__segments[label]
        except KeyError:
            return None


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        segments = '[' + ', '.join([str(segment) for segment in self.segments]) + ']'

        return (f'Block:{{label:{self.label}, address:{self.address}, operation:{self.operation.name}, '
                f'segments:{segments}}}')
