import parmed as pmd


class System(object):
    def __init__(self, path, name, cores):
        self.path = path
        self.name = name
        self.cores = cores

        structure = pmd.load_file(path+'/build/complex.crd')
        self.box = structure.box

    @property
    def descriptors(self):
        return ['cons.pdb', 'tags.pdb']


