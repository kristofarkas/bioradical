from enum import IntEnum
from functools import total_ordering

from radical.entk import Stage


@total_ordering
class Step(object):
    def __init__(self, name, path):
        self.name = name
        self.type = self._StepType.get(name)
        self.path = path

    def as_stage(self):
        stage = Stage()
        stage.name = self.name

        return stage

    def __eq__(self, other):
        eq = self.type == other.type
        return self.name == other.name if eq else False

    def __lt__(self, other):
        lt = self.type < other.type
        eq = self.type == other.type
        return True if lt else self.name < other.name if eq else False

    class _StepType(IntEnum):
        minimize = 0
        equilibration = 1
        simulate = 2
        production = 3

        @classmethod
        def get(cls, value):
            if value.startswith('min'):
                return cls.minimize
            if value.startswith('eq'):
                return cls.equilibration
            if value.startswith('sim'):
                return cls.equilibration
            if value.startswith('prod'):
                return cls.production
            return NotImplemented


class TIESAnalysis(object):

    _NAMD_TI_ANALYSIS = "/u/sciteam/farkaspa/namd/ti/namd2_ti.pl"

    def __init__(self):
        pass

