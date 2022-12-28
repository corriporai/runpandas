=====
Frame
=====
.. currentmodule:: runpandas.types


A ``Activity`` is a tabular data structure that contains a column
which contains a ``MeasureSeries`` storing special measures.

A ``RaceResult`` object is a ``pandas.DataFrame`` that contains
additional metadata and methods pertinent to analysis of race results.

Constructor
-----------
.. autosummary::
   :toctree: api/

   Activity
   RaceResult

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

RaceResult
----------

.. autosummary::
   :toctree: api/

   RaceResult.summary
   RaceResult.total_participants
   RaceResult.total_finishers
   RaceResult.total_nonfinishers
   RaceResult.winner
   RaceResult.participants