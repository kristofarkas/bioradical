from radical.entk import AppManager

from bioradical.system import System
from bioradical.workflow import TIESWorkflow


def main():
    # Define the system workflow

    gsk1 = System(path='testsystem/radical-isc/ties/brd4-gsk3-1', name='complex', cores=32)

    wf = TIESWorkflow(number_of_replicas=2, system=gsk1, number_of_windows=11)

    rman = wf.resource_manager()

    rman.shared_data += ['testsystem/radical-isc/ties/brd4-gsk3-1/build/complex.pdb',
                         'testsystem/radical-isc/ties/brd4-gsk3-1/build/complex.top',
                         'testsystem/radical-isc/ties/brd4-gsk3-1/build/tags.pdb']

    # Create Application Manager
    app_manager = AppManager()
    app_manager.resource_manager = rman
    app_manager.assign_workflow(wf.generate_pipeline())
    app_manager.run()


if __name__ == '__main__':
    import os

    os.environ['RADICAL_ENTK_VERBOSE'] = 'INFO'
    os.environ['RADICAL_PILOT_DBURL'] = 'mongodb://radical:fg*2GT3^eB@crick.chem.ucl.ac.uk:27017/admin'
    os.environ['RP_ENABLE_OLD_DEFINES'] = 'True'
    os.environ['SAGA_PTY_SSH_TIMEOUT'] = '2000'
    os.environ['RADICAL_PILOT_PROFILE'] = 'True'
    os.environ['RADICAL_ENMD_PROFILE'] = 'True'
    os.environ['RADICAL_ENMD_PROFILING'] = '1'
    os.environ['RADICAL_GPU'] = 'False'

    main()


