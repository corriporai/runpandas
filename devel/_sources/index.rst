.. runpandas documentation master file, created by
   sphinx-quickstart on Wed Jun 24 20:22:44 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to runpandas documentation!
=====================================
.. include:: _version.txt

Runpandas is a python package focused on adding support for data collected by GPS-enabled tracking
devices, heart rate monitors data to [pandas](http://pandas.pydata.org) objects.
Its goal is to fill the gap between the tracking data collection and their manual analyses.


.. warning::
   The current state of the project is "early beta": features might be
   added, removed or changed in backwards incompatible ways.
   Report bugs, suggest features or view the source code `on GitHub`_.

.. _on GitHub: https://github.com/corriporai/runpandas

.. toctree::
   :hidden:

   Home <self>
   Getting started <getting_started>
   User Guide <user_guide/user_guide>
   Reference <reference/reference>
   Changelog <whatsnew>

Quick Start
-----------

Install using ``pip``

.. code-block:: shell

   pip install runpandas

and then import and use one of the tracking readers. This example
loads a local file.tcx.

>>> import runpandas as rpd
>>> activity = rpd.read('/path/to/file.tcx')
>>> activity.head(5)
alt	dist	hr	lon	lat   time
00:00:00	178.942627	0.000000	62.0	-79.093187	35.951880
00:00:01	178.942627	0.000000	62.0	-79.093184	35.951880
00:00:06	178.942627	1.106947	62.0	-79.093172	35.951868
00:00:12	177.500610	13.003035	62.0	-79.093228	35.951774
00:00:16	177.500610	22.405027	60.0	-79.093141	35.951732


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
