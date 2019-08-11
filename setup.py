from setuptools import setup, find_packages

from altaudit.constants import VERSION

setup(
    name='AltAudit',
    version=VERSION,
    packages=find_packages(exclude=['tests', 'tests.*'])
)
