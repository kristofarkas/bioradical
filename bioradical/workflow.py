from itertools import product

import radical.entk as e

from bioradical.ensemble import LambdaWindow, Replica
from bioradical.simulation import Simulation


class Workflow(object):
    def __init__(self):
        self.ensembles = list()
        self.steps = list()
        pass

    @property
    def pipelines(self):
        pipelines = set()
        for ensembles in product(*self.ensembles):
            pipeline = e.Pipeline()

            for step in self.steps:
                simulation = Simulation(name=step, p=pipeline)

                for ens in ensembles:
                    ens.fn(simulation)

                pipeline.add_stages(simulation)

            pipelines.add(pipeline)

        return pipelines


class ESMACSWorkflow(Workflow):
    def __init__(self, number_of_replicas, steps):
        super(ESMACSWorkflow, self).__init__()
        self.ensembles = [Replica(number_of_replicas)]
        self.steps = steps


class TIESWorkflow(Workflow):
    def __init__(self, number_of_replicas, steps, lambda_windows):
        super(TIESWorkflow, self).__init__()
        self.ensembles = [Replica(number_of_replicas), LambdaWindow(additional=lambda_windows)]
        self.steps = steps
