from radical.entk import AppManager
from bioradical.workflow import TIESWorkflow
from bioradical.system import System


def main():
    # Define the system workflow

    gsk1 = System(path='testsystem/radical-isc/ties/brd4-gsk3-1', name='complex', cores=32)

    wf = TIESWorkflow(number_of_replicas=2, system=gsk1, additional_windows=[0.5, 0.6])

    wf.shared_data += ['testsystem/radical-isc/ties/brd4-gsk3-1/build/complex.pdb',
                       'testsystem/radical-isc/ties/brd4-gsk3-1/build/complex.top',
                       'testsystem/radical-isc/ties/brd4-gsk3-1/build/tags.pdb']

    # Create Application Manager
    app_manager = AppManager()
    app_manager.resource_manager = wf
    app_manager.assign_workflow(wf.generate_pipelines())
    print 'Running on {} cores'.format(wf.cores)
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

