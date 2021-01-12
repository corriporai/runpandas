#!/usr/bin/env/python
"""Installation script

"""

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from setuptools import setup, find_packages

import versioneer

LONG_DESCRIPTION = """RunPandas is a project to add support for data collected
by GPS-enabled tracking devices, heart rate monitors data to `pandas`_ objects.

RunPandas is a Python package that provides infrastructure for importing
tracking data from such devices, enabling statistical and visual analysis
for running enthusiasts and lovers. Its goal is to fill the gap between
the routine collection of data and their manual analyses in Pandas and Python.

.. _pandas: http://pandas.pydata.org
"""


INSTALL_REQUIRES = []
TEST_REQUIRES = []
with open("./requirements.txt") as f:
    INSTALL_REQUIRES = f.read().splitlines()
with open("./requirements-dev.txt") as f:
    TEST_REQUIRES = f.read().splitlines()

# get all data dirs in the datasets module
data_files = []

setup(
    name="runpandas",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description="Running Tracking Analysis",
    license="BSD",
    author="RunPandas contributors",
    author_email="marcel@caraciolo.com.br",
    url="https://github.com/corriporai/runpandas",
    long_description=LONG_DESCRIPTION,
    python_requires=">=3.6",
    include_package_data=True,
    install_requires=INSTALL_REQUIRES,
    packages=find_packages(exclude=['tests*']),
    zip_safe=False,
)
