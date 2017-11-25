from collections import Iterator

import numpy as np


class EnsemblePackage:
    def __init__(self, path_name=None, fn=None, iterator_state=None):
        self.path_name = path_name
        self.fn = fn or self._do_nothing
        self.iterator_state = iterator_state

    def _do_nothing(self, *args):
        pass


class EnsembleIterator(Iterator):
    def __init__(self, name, underlying_iterable):
        self.name = name
        self.underlying_iterable = underlying_iterable

    def __iter__(self):
        self._iterator = iter(self.underlying_iterable)
        return self

    def next(self):
        ens_pack = EnsemblePackage()
        ens_pack.iterator_state = next(self._iterator)
        # ens_pack.path_name = f'{self.name}_{ens_pack.iterator_state.__str__()}'
        return ens_pack

    @classmethod
    def __subclasshook__(cls, C):
        return super(EnsembleIterator, cls).__subclasshook__(C)


class Replica(EnsembleIterator):
    def __init__(self, number_of):
        super(Replica, self).__init__(name='replica', underlying_iterable=range(number_of))


class LambdaWindow(EnsembleIterator):
    def __init__(self, number_of_states=0, number_of_windows=None, additional=None):
        it = range(number_of_states) if number_of_states else np.linspace(0.0, 1.0, number_of_windows, endpoint=True)
        if additional:
            it = np.append(it, additional)
            it.sort()
        super(LambdaWindow, self).__init__(name='lambda', underlying_iterable=it)

    def next(self):
        ens_pack = super(LambdaWindow, self).__next__()
        ens_pack.fn = _lambda_window(ens_pack.iterator_state)
        return ens_pack


def _lambda_window(ld):
    def f(simulation):
        (t, ) = simulation.tasks
        t.pre_exec = ["sed -i '.bak' 's/LAMBDA/{}/g' *".format(ld)]
        t.link_input_data += ['$SHARED/tags.pdb']
    return f
