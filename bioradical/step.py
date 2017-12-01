from enum import IntEnum
from functools import total_ordering

from radical.entk import Stage


@total_ordering
class Step(Stage):
    def __init__(self, name, path):
        super(Step, self).__init__()
        self.name = name
        self.type = self._StepType.get(name)
        self.path = path

    def __eq__(self, other):
        eq = self.type == other.type
        return self.name == other.name if eq else False

    def __lt__(self, other):
        lt = self.type < other.type
        eq = self.type == other.type
        return True if lt else self.name < other.name if eq else False

    def __repr__(self):
        return self.name

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
