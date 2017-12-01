from setuptools import setup, find_packages

setup(
    name='bioradical',

    version='0.1',

    description='Bioradical',

    long_description='Copy from README file',

    url='http://ccs.chem.ucl.ac.uk',

    author='CCS',

    packages=find_packages(),

    install_requires=['numpy', 'radical.entk', 'parmed']
)

