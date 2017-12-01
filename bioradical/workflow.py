import os
import operator
import pkg_resources
from itertools import product
from radical.entk import Pipeline, ResourceManager
from pkgutil import extend_path

from bioradical.ensemble import LambdaWindow, Replica, Systems
from bioradical.simulation import Simulation
from bioradical.step import Step


class Workflow(ResourceManager):

    def __init__(self):
        self._ensembles = list()
        self._steps = list()

    @property
    def steps(self):
        return self._steps

    @steps.setter
    def steps(self, new_steps):
        self._steps = new_steps
        self.update()

    @property
    def ensembles(self):
        return self._ensembles

    @ensembles.setter
    def ensembles(self, new_value):
        self._ensembles = new_value
        self.update()

    def update(self):
        ResourceManager.__init__(self, self._resource_dictionary)
        self.shared_data += [step.path for step in self.steps]

    def generate_pipelines(self):
        pipeline = Pipeline()

        for step in self.steps:
            for ensembles in product(*self.ensembles):
                # Instantiate a new simulation
                simulation = Simulation(step=step, pipeline=pipeline)
                # Apply all the modifications to it
                [modify(simulation) for modify in ensembles]

            pipeline.add_stages(step)

        return pipeline

        # pipelines = set()
        #
        # for ensembles in product(*self.ensembles):
        #     pipeline = Pipeline()
        #
        #     for step in self.steps:
        #         # Instantiate a new simulation
        #         simulation = Simulation(step=step, pipeline=pipeline)
        #         # Apply all the modifications to it
        #         [modify(simulation) for modify in ensembles]
        #         # Add the simulation to the pipeline.
        #         pipeline.add_stages(simulation.as_stage())
        #
        #     pipelines.add(pipeline)
        #
        # return pipelines

    # Private methods

    @staticmethod
    def _inferred_steps(folder):
        steps = [Step(f[:-5], path='{}/{}'.format(d, f)) for (d, _, paths)
                 in os.walk(folder) if paths for f in paths if f.endswith('.conf')]
        steps.sort()
        print('Detected steps (sorted): {}'.format(steps))
        return steps

    @property
    def _resource_dictionary(self):
        return dict(resource='ncsa.bw_aprun',
                    walltime=60,
                    cores=reduce(operator.mul, (e.cores for e in self.ensembles), 1),
                    project='bamm',
                    queue='normal',
                    access_schema='gsissh')


class ESMACSWorkflow(Workflow):
    def __init__(self, system, number_of_replicas, steps=None):
        super(ESMACSWorkflow, self).__init__()
        self.ensembles = [Replica(number_of_replicas),
                          Systems([system])]
        default_steps = pkg_resources.resource_filename(__name__, 'default_configs/esmacs')
        self.steps = steps if steps else self._inferred_steps(folder=default_steps)


class TIESWorkflow(Workflow):
    def __init__(self, system, number_of_replicas, steps=None, number_of_windows=0, additional_windows=None):
        super(TIESWorkflow, self).__init__()
        self.ensembles = [Replica(number_of_replicas),
                          LambdaWindow(number_of_windows, additional_windows),
                          Systems([system])]
        pkg_resources.resource_listdir()
        default_steps = pkg_resources.resource_filename(__name__, 'default_configs/ties')
        self.steps = steps if steps else self._inferred_steps(folder=default_steps)
