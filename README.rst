
.. image:: https://raw.githubusercontent.com/corriporai/runpandas/master/docs/source/_static/images/runpandas_banner.png

RunPandas - Python Package for handing running data from GPS-enabled tracking devices and applications.
=======================================================================================================

.. image:: https://img.shields.io/pypi/v/runpandas.svg
    :target: https://pypi.python.org/pypi/runpandas/

.. image:: https://www.codefactor.io/repository/github/corriporai/runpandas/badge
   :target: https://www.codefactor.io/repository/github/corriporai/runpandas
   :alt: CodeFactor

.. image:: https://travis-ci.com/corriporai/runpandas.svg?branch=master
    :target: https://travis-ci.com/github/corriporai/runpandas

.. image:: https://coveralls.io/repos/github/corriporai/runpandas/badge.svg?branch=master
    :target: https://coveralls.io/github/corriporai/runpandas

.. image:: https://codecov.io/gh/corriporai/runpandas/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/corriporai/runpandas

.. image:: https://readthedocs.org/projects/runpandas/badge/?version=latest
    :target: https://runpandas.readthedocs.io/en/latest/?badge=latest

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
     :target: https://github.com/psf/black

.. image:: https://static.pepy.tech/personalized-badge/runpandas?period=total&units=international_system&left_color=black&right_color=orange&left_text=Downloads
   :target: https://pepy.tech/project/runpandas

=========

Introduction
------------

RunPandas is a project to add support for data collected by GPS-enabled tracking devices,
heart rate monitors data to  [pandas](http://pandas.pydata.org) objects.
It is a Python package that provides infrastructure for importing tracking data
from such devices, enabling statistical and visual analysis for running enthusiasts and lovers.
Its goal is to fill the gap between the routine collection of data and their manual analyses in Pandas and Python.

Documentation
-------------
`Stable documentation `__
is available on
`github.io <https://corriporai.github.io/runpandas/>`__.
A second copy of the stable documentation is hosted on
`read the docs <https://runpandas.readthedocs.io/>`_ for more details.

`Development documentation <https://corriporai.github.io/runpandas/devel/>`__
is available for the latest changes in master.

==> Check out `this Blog post <https://corriporai.github.io/pandasrunner/general/2020/08/01/welcome-to-runpandas.html>`_
for the reasoning and philosophy behind Runpandas, as well as a detailed tutorial with code examples.

==> Follow `this Runpandas live book <https://github.com/corriporai/runpandasbook>`_ in Jupyter notebook format based on `Jupyter Books <https://jupyterbook.org/intro.html>`_.


Install
--------

 RunPandas depends on the following packages:

- ``pandas``
- ``fitparse``
- ``stravalib``

Runpandas was tested to work on \*nix-like systems, including macOS.

-----

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


Get in touch
------------
- Report bugs, suggest features or view the source code [on GitHub](https://github.com/corriporai/runpandas).

I'm very interested in your experience with runpandas.
Please drop me an note with any feedback you have.

Contributions welcome!

\- **Marcel Caraciolo**

License
-------
Runpandas is licensed under the **MIT License**. A copy of which is included in LICENSE.