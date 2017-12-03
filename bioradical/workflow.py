import os
import operator
import pkg_resources
from itertools import product

from radical.entk import Pipeline, ResourceManager

from bioradical.step import Step
from bioradical.simulation import Simulation
from bioradical.ensemble import LambdaWindow, Replica, Systems


class Workflow(object):

    def __init__(self, ensembles, steps):
        self.ensembles = ensembles
        self.steps = steps

    def generate_pipeline(self):
        # Create a new pipeline
        pipeline = Pipeline()

        # Create the stages, and add them all to the pipeline
        stages = [step.as_stage() for step in self.steps]
        pipeline.add_stages(stages)

        # Loop through all the stages, and generate all the tasks.
        for stage in stages:
            for ensembles in product(*self.ensembles):
                simulation = Simulation(stage=stage, pipeline=pipeline)
                [modify(simulation) for modify in ensembles]
                stage.add_tasks(simulation.as_task())

        return pipeline

    def resource_manager(self):
        resource_manager = ResourceManager(self._resource_dictionary)
        resource_manager.shared_data = [step.path for step in self.steps]
        return resource_manager

    # Private methods
    @staticmethod
    def _inferred_steps(folder):
        steps = [Step(f[:-5], path='{}/{}'.format(d, f)) for (d, _, paths)
                 in os.walk(folder) if paths for f in paths if f.endswith('.conf')]
        steps.sort()
        return steps

    @property
    def _resource_dictionary(self):
        return dict(resource='ncsa.bw_aprun',
                    walltime=60,
                    cpus=reduce(operator.mul, (e.cores for e in self.ensembles), 1),
                    project='bamm',
                    queue='normal',
                    access_schema='gsissh')


class ESMACSWorkflow(Workflow):
    def __init__(self, system, number_of_replicas, steps=None):
        ensembles = [Replica(number_of_replicas), Systems([system])]

        default_steps = pkg_resources.resource_filename(__name__, 'default_configs/esmacs')
        steps = steps if steps else self._inferred_steps(folder=default_steps)

        super(ESMACSWorkflow, self).__init__(ensembles, steps)


class TIESWorkflow(Workflow):
    def __init__(self, system, number_of_replicas, steps=None, number_of_windows=0, additional_windows=None):
        ensembles = [Replica(number_of_replicas), Systems([system]),
                     LambdaWindow(number_of_windows, additional_windows)]

        default_steps = pkg_resources.resource_filename(__name__, 'default_configs/ties')
        steps = steps if steps else self._inferred_steps(folder=default_steps)

        super(TIESWorkflow, self).__init__(ensembles, steps)
