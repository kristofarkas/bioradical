import os
from radical.entk import ResourceManager, AppManager
from bioradical.workflow import TIESWorkflow


def main():
    
    # ESMACS workflow

    wf = TIESWorkflow(number_of_replicas=1, 
                      steps=['min', 'eq1', 'eq2', 'prod'], 
                      system='complex', 
                      descriptors=['f4.pdb', 'tags.pdb'],
                      additional=[0.5])

    # Resource and AppManager
    
    res_dict = {
            'resource': 'ncsa.bw_aprun',
            'walltime': 30,
            'cores': 16,
            'project': 'bamm',
            'queue': 'normal',
            'access_schema': 'gsissh'
    }
    
    root_directory = 'bace1_b01'

    # Create Resource Manager object with the above resource description
    resource_manager = ResourceManager(res_dict)
    resource_manager.shared_data = ['{}/build/complex.pdb'.format(root_directory), 
                                    '{}/build/complex.top'.format(root_directory),
                                    '{}/build/tags.pdb'.format(root_directory),
                                    '{}/constraint/f4.pdb'.format(root_directory)]
    resource_manager.shared_data += ["confs/{}.conf".format(w) for w in wf.steps]

    # Create Application Manager
    app_manager = AppManager()
    app_manager.resource_manager = resource_manager
    app_manager.assign_workflow(wf.generate_pipelines())
    app_manager.run()

if __name__ == '__main__':
    
    import os
    os.environ['RADICAL_ENTK_VERBOSE'] = 'INFO'
    os.environ['RADICAL_PILOT_DBURL'] = 'mongodb://radical:fg*2GT3^eB@crick.chem.ucl.ac.uk:27017/admin'
    os.environ['RP_ENABLE_OLD_DEFINES'] = 'True'
    os.environ['SAGA_PTY_SSH_TIMEOUT']='2000'
    os.environ['RADICAL_PILOT_PROFILE']='True'
    os.environ['RADICAL_ENMD_PROFILE']='True'
    os.environ['RADICAL_ENMD_PROFILING']='1'

    main()

