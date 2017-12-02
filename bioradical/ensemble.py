from collections import Iterator

import numpy as np


class EnsembleIterator(Iterator):
    def __init__(self, underlying_iterable):
        self.underlying_iterable = underlying_iterable

    def __iter__(self):
        self._iterator = iter(self.underlying_iterable)
        return self

    def next(self):
        next(self._iterator)
        return self._do_nothing

    def _do_nothing(self, *args):
        pass

    @classmethod
    def __subclasshook__(cls, C):
        return super(EnsembleIterator, cls).__subclasshook__(C)

    @property
    def cores(self):
        return len(self.underlying_iterable)


class Systems(EnsembleIterator):
    def __init__(self, systems=None):
        super(Systems, self).__init__(underlying_iterable=systems)

    def next(self):
        system = next(self._iterator)
        
        def modifier(simulation):
            simulation.system = system

        return modifier

    @property
    def cores(self):
        return sum([system.cores for system in self.underlying_iterable])
    

class Replica(EnsembleIterator):
    def __init__(self, number_of_replicas):
        """Runs the *same* simulation multiple times. This is used in molecular dynamics to get
        averages and estimate error.

        :param number_of_replicas: The number of pipelines to run consecutively.
        """
        super(Replica, self).__init__(underlying_iterable=range(number_of_replicas))

    def next(self):

        rep = next(self._iterator)

        def modifier(simulation):
            simulation.name += '_replica_{}'.format(rep)

        return modifier


class LambdaWindow(EnsembleIterator):
    def __init__(self, number_of_windows=0, additional=None):
        """Alchemical free energy transformation lambda window

        :param number_of_windows: Number of equally spaced lambda windows
        :param additional: Additional lambda windows to run.
        """
        it = np.linspace(0.0, 1.0, number_of_windows, endpoint=True)
        if additional:
            it = np.append(it, additional)
            it.sort()
        super(LambdaWindow, self).__init__(underlying_iterable=it)

    def next(self):

        ld = next(self._iterator)

        def modifier(simulation):
            simulation.name += '_lambda_{}'.format(ld)
            simulation.pre_exec += ["sed -i 's/LAMBDA/{}/g' *.conf".format(ld)]

        return modifier
