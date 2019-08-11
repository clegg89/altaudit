from setuptools import setup, find_packages

setup(
    name='AltAudit',
    version='0.1dev',
    packages=find_packages(exclude=['tests', 'tests.*'])
)
