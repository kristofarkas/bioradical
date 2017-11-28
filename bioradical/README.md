## Simulation

Specify the `namd2` executable and possible extensions for files that we need to copy from one
simulation to the next. This is all very NAMD specific for now. The extensions are there so that
there is no need to 'see' what is in the previous `Task`'s folder.

```python
_simulation_file_suffixes = ['.coor', '.xsc', '.vel']
_namd = '/u/sciteam/jphillip/NAMD_LATEST_CRAY-XE-ugni-smp-BlueWaters/namd2'
```

Simulation is a `Task` subclass. It can also turn itself into a `Stage` just by calling `.as_stage()`.
```python
class Simulation(Task):
```

The `step` determines a lot in the Task object: the name, arguments and the **only** file that needs
to be copied over from `$SHARED` that is the configuration file.
```python
@step.setter
def step(self, value):
    self.name = value
    self.arguments = ['{}.conf'.format(self.name)]
    self.copy_input_data = ['$SHARED/{}.conf'.format(self.name)]
```

This is where all the linking happens. Files that are **NOT** edited are linked only (to save on time?).
We link the input topology, any other descriptor file, and all the files from the *previous* step that
have the prefix in `_simulation_file_suffixes`. Note, if this the the first step, then we link the
system PDB file from the shared directory.
```python
def _update_linked_data_list(self):
```