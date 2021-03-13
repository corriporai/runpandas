=====
Frame
=====
.. currentmodule:: runpandas.types


A ``Activity`` is a tabular data structure that contains a column
which contains a ``MeasureSeries`` storing special measures.

Constructor
-----------
.. autosummary::
   :toctree: api/

   Activity

Reading and writing files
-------------------------

.. autosummary::
   :toctree: api/

   Activity.from_file

Activity handling
-----------------

.. autosummary::
   :toctree: api/

   Activity.set_specs
   Activity.to_pandas


Special Metrics
----------------

.. autosummary::
   :toctree: api/

   Activity.ellapsed_time
   Activity.moving_time
   Activity.distance
