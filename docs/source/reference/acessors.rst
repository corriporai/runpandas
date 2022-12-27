========
Acessors
========
.. currentmodule:: runpandas.types.acessors


Special acessors to perform activity transformations or derived observations based on activity data.

Moving
------

.. autosummary::
   :toctree: api/

   moving._InactivityAssessor

Metrics
-------

.. autosummary::
   :toctree: api/

   metrics.MetricsAcessor
   metrics.MetricsAcessor.speed
   metrics.MetricsAcessor.distance
   metrics.MetricsAcessor.vertical_speed
   metrics.MetricsAcessor.gradient
   metrics.MetricsAcessor.pace
   metrics.MetricsAcessor.heart_zone
   metrics.MetricsAcessor.time_in_zone


Session
-------

.. autosummary::
   :toctree: api/

   session._SessionAcessor
   session._SessionAcessor.summarize
   session._SessionAcessor.count
   session._SessionAcessor.distance
   session._SessionAcessor.speed
   session._SessionAcessor.vertical_speed
   session._SessionAcessor.gradient
   session._SessionAcessor.pace
   session._SessionAcessor.heart_zone
   session._SessionAcessor.only_moving

Splits
-------

.. autosummary::
   :toctree: api/

   splits._RaceSplitsAcessor.pick_athlete
