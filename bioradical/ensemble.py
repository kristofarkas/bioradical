from collections import Iterator

import numpy as np


class EnsembleIterator(Iterator):
    def __init__(self, name, underlying_iterable):
        self.name = name
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


class Systems(EnsembleIterator):
    def __init__(self, systems=None):
        super(Systems, self).__init__(name='system', underlying_iterable=systems)

    def next(self):
        system = next(self._iterator)
        
        def wrapper(simulation):
            (simulation.system, simulation.descriptors) = system

        return wrapper
    

class Replica(EnsembleIterator):
    def __init__(self, number_of):
        """Runs the *same* simulation multiple times. This is used in molecular dynamics to get
        averages and estimate error.

        :param number_of: The number of pipelines to run consecutively.
        """
        super(Replica, self).__init__(name='replica', underlying_iterable=range(number_of))


class LambdaWindow(EnsembleIterator):
    def __init__(self, number_of_states=0, number_of_windows=None, additional=None):
        """Alchemical free energy transformation

        :param number_of_states: This is for GROMACS type configuration files only.
        :param number_of_windows: Number of equally spaced lambda windows
        :param additional: Additional lambda windows to run.
        """
        it = range(number_of_states) if number_of_states is not None else np.linspace(0.0, 1.0, number_of_windows, endpoint=True)
        if additional:
            it = np.append(it, additional)
            it.sort()
        super(LambdaWindow, self).__init__(name='lambda', underlying_iterable=it)

    def next(self):

        ld = next(self._iterator)

        def wrapper(simulation):
            simulation.pre_exec += ["sed -i '.bak' 's/LAMBDA/{}/g' *.conf".format(ld)]

        return wrapper
