from radical.entk import Task, Stage

_simulation_file_suffixes = ['.coor', '.xsc', '.vel']
_namd = '/u/sciteam/jphillip/NAMD_LATEST_CRAY-XE-MPI-BlueWaters/namd2'
# _namd = 'namd2'


class Simulation(Task):
    def __init__(self, step, pipeline, system=None):
        """Create a new simulation step.

        :param step: The name of the step, for example: min, eq, prod, sim etc.
        :param pipeline: The pipeline that it will be in. Used to get previous steps.
        :param system: The name of the PDB and topology files. (without suffix)
        """
        super(Simulation, self).__init__()

        self.step = step
        self.pipeline = pipeline

        step.add_tasks(self)
        pipeline.add_stages(step)
        self.arguments = ['{}.conf'.format(step.name)]
        self.copy_input_data = ['$SHARED/{}.conf'.format(step.name)]

        self.system = system

        self.executable = [_namd]
        self.mpi = True

        # self.pre_exec += ['export OMP_NUM_THREADS=1']
        # self.cpu_reqs = {'processes': 1, 'process_type': 'MPI', 'threads_per_process': 31, 'thread_type': None}

    @property
    def system(self):
        return self._system

    @system.setter
    def system(self, new_system):
        self._system = new_system
        self._update_task_info()

    def _update_task_info(self):

        files_to_link = []

        if self.system:
            files_to_link += ['$SHARED/{}.top'.format(self.system.name)]
            files_to_link += ['$SHARED/{}'.format(f) for f in self.system.descriptors]
            self.pre_exec += ["sed -i 's/BOX_X/{}/g' *.conf".format(self.system.box[0]),
                              "sed -i 's/BOX_Y/{}/g' *.conf".format(self.system.box[1]),
                              "sed -i 's/BOX_Z/{}/g' *.conf".format(self.system.box[2])]
            self.cores = self.system.cores

        # Link input data generated by the previous step or the PDB if this is the first step.

        if self.pipeline:
            if self.pipeline.stages.index(self.step) > 0:  # This is not the first stage.
                previous_stage = self.pipeline.stages[self.pipeline.stages.index(self.step)-1]
                # FIXME: This is fucked up!
                previous_task = next(iter(previous_stage.tasks))
                path = '$Pipeline_{}_Stage_{}_Task_{}'.format(self.pipeline.uid, previous_stage.uid, previous_task.uid)
                files_to_link.extend("{}/{}{}".format(path, previous_stage.name, suffix) for suffix in _simulation_file_suffixes)
            elif self.system:
                files_to_link.append('$SHARED/{}.pdb'.format(self.system.name))

        self.link_input_data = files_to_link

    def as_stage(self):
        """Convenience method to convert the Simulation into a stage.

        :return: a Stage instance with self as the only task added to it.
        """
        stage = Stage()
        stage.add_tasks(self)
        return stage

