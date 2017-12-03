from radical.entk import Task

NAMD2 = '/u/sciteam/jphillip/NAMD_LATEST_CRAY-XE-MPI-BlueWaters/namd2'

_simulation_file_suffixes = ['.coor', '.xsc', '.vel']


class Simulation(object):
    def __init__(self, pipeline, stage, system=None):
        self.name = 'simulation'
        self.stage = stage
        self.pipeline = pipeline
        self.system = system
        self.lambda_window = None

    def as_task(self):
        if not all([self.pipeline, self.stage, self.system]) and self.stage in self.pipeline.stages:
            raise ValueError('Please set everything before converting to task.')

        task = Task()

        task.name = self.name
        task.arguments = ['{}.conf'.format(self.stage.name)]
        task.copy_input_data = ['$SHARED/{}.conf'.format(self.stage.name)]
        task.executable = [NAMD2]

        # For rc/0.46.3 stack
        task.mpi = True
        task.cores = self.system.cores

        # For gpu branch
        # self.pre_exec += ['export OMP_NUM_THREADS=1']
        # self.cpu_reqs = {'processes': 1, 'process_type': 'MPI', 'threads_per_process': 31, 'thread_type': None}

        # Linking

        link = []
        link += ['$SHARED/{}.top'.format(self.system.name)]
        link += ['$SHARED/{}'.format(f) for f in self.system.descriptors]

        index = self.pipeline.stages.index(self.stage)
        if index:
            previous_stage = self.pipeline.stages[index-1]
            previous_task = next(task for task in previous_stage.tasks if task.name == self.name)
            path = '$Pipeline_{}_Stage_{}_Task_{}/'.format(self.pipeline.uid, previous_stage.uid, previous_task.uid)
            link += [path+previous_stage.name+suffix for suffix in _simulation_file_suffixes]
        else:
            link += ['$SHARED/{}.pdb'.format(self.system.name)]

        task.link_input_data = link

        # Modify configuration file

        task.pre_exec += ["sed -i 's/BOX_X/{}/g' *.conf".format(self.system.box[0]),
                          "sed -i 's/BOX_Y/{}/g' *.conf".format(self.system.box[1]),
                          "sed -i 's/BOX_Z/{}/g' *.conf".format(self.system.box[2])]

        if self.lambda_window is not None:
            task.pre_exec += ["sed -i 's/LAMBDA/{}/g' *.conf".format(self.lambda_window)]

        return task
