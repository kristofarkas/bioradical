from itertools import product

from radical.entk import Pipeline

from bioradical.ensemble import LambdaWindow, Replica, Systems
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
            pipeline = Pipeline()

            for step in self.steps:
                simulation = Simulation(step=step, pipeline=pipeline)

                for mod in ensembles:
                    mod(simulation)

                pipeline.add_stages(simulation.as_stage)

            pipelines.add(pipeline)

        return pipelines


class ESMACSWorkflow(Workflow):
    def __init__(self, system, descriptors, number_of_replicas, steps):
        super(ESMACSWorkflow, self).__init__()
        self.ensembles = [Replica(number_of_replicas),
                          Systems([(system, descriptors)])
                          ]
        self.steps = steps


class TIESWorkflow(Workflow):
    def __init__(self, system, descriptors, number_of_replicas, steps, lambda_windows):
        super(TIESWorkflow, self).__init__()
        self.ensembles = [Replica(number_of_replicas),
                          LambdaWindow(additional=lambda_windows),
                          Systems([(system, descriptors)])
                          ]
        self.steps = steps
