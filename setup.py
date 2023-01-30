from setuptools import find_packages, setup

setup(
    name='mlops-sample-demo',
    packages=find_packages(exclude=['tests', 'tests.*']),
    setup_requires=['wheel'],
    description='Repository implementing an end-to-end MLOps workflow on Databricks for sample data',
    authors=''
)