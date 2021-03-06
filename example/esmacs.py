from radical.entk import AppManager

from bioradical.system import System
from bioradical.workflow import ESMACSWorkflow


def main():
    
    # Define the system workflow

    gsk1 = System(path='testsystem/radical-isc/esmacs/brd4-gsk1', name='complex', cores=32)

    wf = ESMACSWorkflow(number_of_replicas=2, system=gsk1)

    rman = wf.resource_manager()

    rman.shared_data += ['testsystem/radical-isc/esmacs/brd4-gsk1/build/complex.pdb',
                         'testsystem/radical-isc/esmacs/brd4-gsk1/build/complex.top',
                         'testsystem/radical-isc/esmacs/brd4-gsk1/constraint/cons.pdb']

    # Create Application Manager
    app_manager = AppManager()
    app_manager.resource_manager = rman
    app_manager.assign_workflow(wf.generate_pipeline())
    app_manager.run()


if __name__ == '__main__':
    
    import os
    os.environ['RADICAL_ENTK_VERBOSE'] = 'DEBUG'
    os.environ['RADICAL_PILOT_DBURL'] = 'mongodb://radical:fg*2GT3^eB@crick.chem.ucl.ac.uk:27017/admin'
    os.environ['RP_ENABLE_OLD_DEFINES'] = 'True'
    os.environ['SAGA_PTY_SSH_TIMEOUT'] = '2000'
    os.environ['RADICAL_PILOT_PROFILE'] = 'True'
    os.environ['RADICAL_ENMD_PROFILE'] = 'True'
    os.environ['RADICAL_ENMD_PROFILING'] = '1'
    os.environ['RADICAL_GPU'] = 'False'

    main()

