import os
from itertools import product
from radical.entk import Pipeline, ResourceManager, AppManager

from bioradical.ensemble import LambdaWindow, Replica, Systems
from bioradical.simulation import Simulation


class Workflow(ResourceManager, AppManager):

    def __init__(self):
        ResourceManager.__init__(self, self._resource_dictionary)
        AppManager.__init__(self)
        self.ensembles = list()
        self.steps = list()

    def generate_pipelines(self):
        pipelines = set()

        for ensembles in product(*self.ensembles):
            pipeline = Pipeline()

            for step in self.steps:
                # Instantiate a new simulation
                simulation = Simulation(step=step, pipeline=pipeline)
                # Apply all the modifications to it
                [modify(simulation) for modify in ensembles]
                # Add the simulation to the pipeline.
                pipeline.add_stages(simulation.as_stage())

            pipelines.add(pipeline)

        return pipelines

    # Private methods

    def _infer_steps(self, folder):
        steps = [f[:-5] for (_, _, paths) in os.walk(folder) if paths for f in paths if f.endswith('.conf')]
        print('Detected steps: {}'.format(steps))
        self.steps = steps

    _resource_dictionary = {
        'resource': 'ncsa.bw_aprun',
        'walltime': 60,
        'cores': 16,
        'project': 'bamm',
        'queue': 'normal',
        'access_schema': 'gsissh'
    }


class ESMACSWorkflow(Workflow):
    def __init__(self, system, descriptors, number_of_replicas, steps):
        super(ESMACSWorkflow, self).__init__()
        self.ensembles = [Replica(number_of_replicas),
                          Systems([(system, descriptors)])]
        self.steps = steps


class TIESWorkflow(Workflow):
    def __init__(self, system, descriptors, number_of_replicas, steps, number_of_windows=0, additional=None):
        super(TIESWorkflow, self).__init__()
        self.ensembles = [Replica(number_of_replicas),
                          LambdaWindow(number_of_windows, additional),
                          Systems([(system, descriptors)])]
        self.steps = steps
