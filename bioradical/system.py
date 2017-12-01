import parmed as pmd


class System(object):
    """A system object describing the files that are required to run the simulation.

    """
    def __init__(self, path, name, cores=16):
        self.path = path
        self.name = name
        self.cores = cores

        structure = pmd.load_file(path+'/build/complex.crd')
        self.box = structure.box

    @property
    def descriptors(self):
        return ['cons.pdb']


