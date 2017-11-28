# Bioradical

Binding free energy calculation workflows using *Radical*.

**Under development! Use with caution.**

## Example usage

```python

from radical.entk import ResourceManager, AppManager
from bioradical.workflow import ESMACSWorkflow

wf = ESMACSWorkflow(number_of_replicas=25, steps=['eq0', 'eq1', 'eq2', 'sim1'])

# Resource and AppManager

res_dict = { .. }

# Create Resource Manager object with the above resource description
resource_manager = ResourceManager(res_dict)
resource_manager.shared_data = ['{}/build/complex.pdb'.format(root_directory),
                                '{}/build/complex.top'.format(root_directory),
                                '{}/constraint/cons.pdb'.format(root_directory)]
resource_manager.shared_data += ["confs/{}.conf".format(w) for w in wf.steps]

app_manager = AppManager()
app_manager.resource_manager = resource_manager

# The pipelines are generated here.
app_manager.assign_workflow(wf.pipelines)
app_manager.run()
```
