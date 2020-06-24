RunPandas
=========

Python Package for handing running data from GPS-enabled tracking devices and applications.

.. image:: https://img.shields.io/pypi/v/runpandas.svg
    :target: https://pypi.python.org/pypi/runpandas/

.. image:: https://travis-ci.org/corriporai/runpandas.png?branch=master
    :target: https://travis-ci.org/corriporai/runpandas

.. image:: https://coveralls.io/repos/corriporai/runpandas/badge.svg?branch=master
    :target: https://coveralls.io/r/corriporai/runpandas

.. image:: https://codecov.io/gh/corriporai/runpandas/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/corriporai/runpandas

.. image:: https://readthedocs.org/projects/runpandas/badge/?version=latest
    :target: https://runpandas.readthedocs.io/en/latest/

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
     :target: https://github.com/psf/black

=========

Introduction
------------

RunPandas is a project to add support for data collected by GPS-enabled tracking devices, heart rate monitors data to
[pandas](http://pandas.pydata.org) objects. It is a Python package that provides infrastructure for importing tracking data from such devices, enabling statistical and visual analysis for running enthusiasts and lovers. Its goal is to fill the gap between the routine collection of data and their manual analyses in Pandas and Python.

Documentation
-------------
`Stable documentation `__
is available on
`github.io <https://corriporai.github.io/runpandas/>`__.
A second copy of the stable documentation is hosted on
`read the docs <https://runpandas.readthedocs.io/>`_ for more details.

`Development documentation <https://corriporai.github.io/runpandas/devel/>`__
is available for the latest changes in master.


Install
--------

 RunPandas depends on the following packages:

- ``pandas``

Get in touch
------------
- Report bugs, suggest features or view the source code [on GitHub](https://github.com/corriporai/runpandas).


Install latest release version via pip
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: shell

   $ pip install runpandas

Install latest development version
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: shell

    $ pip install git+https://github.com/corriporai/runpandas.git

or

.. code-block:: shell

    $ git clone https://github.com/corriporai/runpandas.git
    $ python setup.py install


Examples
--------

