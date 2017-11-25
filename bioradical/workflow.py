from itertools import product
import os

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


if __name__ == '__main__':
    os.environ['RADICAL_ENTK_VERBOSE'] = 'INFO'
    os.environ['RADICAL_PILOT_DBURL'] = 'mongodb://radical:fg*2GT3^eB@crick.chem.ucl.ac.uk:27017/admin'
    os.environ['RP_ENABLE_OLD_DEFINES'] = 'True'

    wf = ESMACSWorkflow(number_of_replicas=5, steps=['eq0', 'eq1', 'eq2', 'sim'])

    # Resource and AppManager

    res_dict = {
            'resource': 'local.localhost',
            'walltime': 10,
            'cores': 1,
            'project': '',
    }

    # Create Resource Manager object with the above resource description
    resource_manager = e.ResourceManager(res_dict)
    resource_manager.shared_data = ['complex.pdb', 'complex.top']
    resource_manager.shared_data += ["{}.conf".format(w) for w in wf.steps]

    # Create Application Manager
    app_manager = e.AppManager()
    app_manager.resource_manager = resource_manager
    app_manager.assign_workflow(wf.pipelines)
    app_manager.run()

