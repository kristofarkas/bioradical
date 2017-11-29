## Simulation

```python
_simulation_file_suffixes = ['.coor', '.xsc', '.vel']
_namd = '/u/sciteam/jphillip/NAMD_LATEST_CRAY-XE-ugni-smp-BlueWaters/namd2'
```
Specify the `namd2` executable and possible extensions for files that we need to copy from one
simulation to the next. This is all very NAMD specific for now. The extensions are there so that
there is no need to 'see' what is in the previous `Task`'s folder.

```python
class Simulation(Task):
    def __init__(self, step, pipeline, system=None, descriptors=None):
```
Simulation is a `Task` subclass. It can also turn itself into a `Stage` just by calling `.as_stage()`.

```python
@step.setter
def step(self, value):
    self.name = value
    self.arguments = ['{}.conf'.format(self.name)]
    self.copy_input_data = ['$SHARED/{}.conf'.format(self.name)]
```
The `step` determines a lot about the `Task` object: the name, arguments and the **only** file that needs
to be copied over from `$SHARED` is the configuration file.

```python
def _update_linked_data_list(self):
```
This is where all the linking happens. Files that are **NOT** edited are linked only (to save on time?).
We link the input topology, any other descriptor files, and all the files from the *previous* step that
have the prefix in `_simulation_file_suffixes`. Note, if this the the first step, then we link the
system PDB file from the shared directory.

## Ensemble

We can think of replicas, lambda windows, different test-system (and a lot of other things) as just
an **iterable**. You iterate over something (e.g. the lambda windows, the replica index, the
system name, etc.) and create a new `Simulation` for each, and **most importantly** change the
`Simulation`'s attribute so that it reflects the current state of the iterator (e.g. change the
lambda parameter, the system name, etc.)

The `EnsembleIterator` is an implementation of this idea, and allows for a very flexible way to define
new ensembles. We already have `Replica`, `LambdaWindow`, `Systems` implemented, but it is very easy
to do others too.

The way this works, is that the iterator returns a function every time `next()` is called. This function
has 1 argument, a `Simulation` object. You can pass the simulation through this function, and it
will edit it to reflect the current state of the iterator.

### How to implement an `EnsembleIterator`?

```python
class LambdaWindow(EnsembleIterator):
    def __init__(self, number_of_windows=None, additional=None):
        it = np.linspace(0.0, 1.0, number_of_windows, endpoint=True)
        if additional:
            it = np.append(it, additional)
            it.sort()
        super(LambdaWindow, self).__init__(underlying_iterable=it)
```

Simply subclass it and call `super` passing the underlying iterable, an actual python iterable,
like an array of numbers, strings, etc.

```python
def next(self):

    ld = next(self._iterator)

    def wrapper(simulation):
        simulation.pre_exec += ["sed -i 's/LAMBDA/{}/g' *.conf".format(ld)]

    return wrapper
```
Overwrite `next` and return a function that takes a simulation and edits it in whatever way.
In this case, we append to the pre-executable.

## Workflow

Finally the `Workflow` class. It has two properties: an array of steps (i.e. the names of the steps; these are assumed to be the output name of the conf file too.) and an array of `EnsembleIterator`s. The only function is `generate_pipelines()` which generates the set of `Pipeline` objects.