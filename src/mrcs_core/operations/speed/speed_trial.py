"""
Created on 25 Oct 2026

@author: Bruno Beloff (bbeloff@me.com)

A collection of speed runs, used to determine the speed curve for an MPU
"""

from collections import OrderedDict
from typing import Any, Self

from mrcs_core.data.json import MultiPersistentJSONable
from mrcs_core.operations.speed.speed_run import SpeedRun


# --------------------------------------------------------------------------------------------------------------------

class SpeedTrial(MultiPersistentJSONable):
    """
    A collection of speed runs, used to determine the speed curve for an MPU
    """

    __FILENAME = "speeds.json"


    @classmethod
    def persistence_location(cls, name):
        filename = cls.__FILENAME if name is None else '_'.join((name, cls.__FILENAME))
        return cls.speeds_dir(), filename


    @classmethod
    def trial_name(cls, mpu_label: str, block_label: str):
        return '_'.join((mpu_label, block_label))


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict, name=None) -> Self:
        mpu_label = jdict.get('mpu_label')
        block_label = jdict.get('block_label')
        runs = [SpeedRun.construct_from_jdict(run_jdict) for run_jdict in jdict.get('runs')]

        return cls(mpu_label, block_label, *runs, name=name)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, mpu_label: str, block_label: str, *runs: SpeedRun, name=None):
        instance_name = name if name else self.trial_name(mpu_label, block_label)
        super().__init__(name=instance_name)

        self.__mpu_label = mpu_label
        self.__block_label = block_label
        self.__runs = list(runs)


    def __eq__(self, other: Any):
        try:
            return (self.mpu_label == other.mpu_label and self.block_label == other.block_label and
                    self.runs == other.runs)
        except (AttributeError, TypeError):
            return False


    # ----------------------------------------------------------------------------------------------------------------

    def add_run(self, run: SpeedRun) -> None:
        self.__runs.append(run)


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        jdict = OrderedDict()

        jdict['mpu_label'] = self.mpu_label
        jdict['block_label'] = self.block_label
        jdict['runs'] = self.runs

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def mpu_label(self):
        return self.__mpu_label


    @property
    def block_label(self):
        return self.__block_label


    @property
    def runs(self):
        return sorted(self.__runs)


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        runs = '[' + ', '.join(map(str, self.runs)) + ']'

        return (f'SpeedTrial:{{name:{self.name}, mpu_label:{self.mpu_label}, block_label:{self.block_label}, '
                f'runs:{runs}}}')
