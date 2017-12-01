from radical.entk import AppManager
from bioradical.workflow import ESMACSWorkflow
from bioradical.system import System


def main():
    
    # Define the system workflow

    gsk1 = System(path='testsystem/radical-isc/esmacs/brd4-gsk1', name='complex', cores=16)

    wf = ESMACSWorkflow(number_of_replicas=1, system=gsk1)

    wf.shared_data += ['testsystem/radical-isc/esmacs/brd4-gsk1/build/complex.pdb',
                       'testsystem/radical-isc/esmacs/brd4-gsk1/build/complex.top',
                       'testsystem/radical-isc/esmacs/brd4-gsk1/build/complex.pdb',
                       'testsystem/radical-isc/esmacs/brd4-gsk1/constraint/cons.pdb']

    # Create Application Manager
    app_manager = AppManager()
    app_manager.resource_manager = wf
    app_manager.assign_workflow(wf.generate_pipelines())
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

    main()

