"""
This is a module for extending pandas activities with session aggregation methods
"""

import pandas as pd
import numpy as np
from runpandas.types import Activity
from runpandas.types import columns
from runpandas.types import summary

@pd.api.extensions.register_dataframe_accessor("session")
class _SessionAcessor(object):
    """
    Dataframe Accessor to compute the aggregated metrics from a MultiIndex
    ``runpandas.types.Activity`` object.

    Raises
    ------
    AttributeError
        if it is not a ``runpandas.types.Activity`` instance or
        not have a ``pd.MultiIndex`` or not have the index levels
        of type ``pd.DateTimeIndex`` or ``pd.TimedeltaIndex``.

    """

    def __init__(self, session):
        self._validate(session)
        self._session = session

    @staticmethod
    def _validate(activity):
        assert isinstance(activity, Activity), "Activity is needed for this accessor"

        if not isinstance(activity.index, pd.MultiIndex) or not \
               set([*map(type, activity.index.levels)]) == set([pd.TimedeltaIndex, pd.DatetimeIndex]) :
            raise AttributeError(
                "An activity needs a DataFrame MultiIndex in (DateTimeIndex, TimedeltaIndex) format"
            )

    def summarize(self):
        return summary.session_summary(self._session)

    def count(self):
        '''
        Returns
        -------
        Returns the total number of activities in the session.

        '''
        return self._session.index.levshape[0]

    def distance(self, correct_distance=False, to_special_column=True, **kwargs):
        for index in self._session.index.unique(level='start'):
                distpos = self._session.xs(index, level=0).compute.distance(correct_distance=correct_distance,
                    to_special_column=to_special_column, **kwargs)
                self._session.loc[pd.IndexSlice[index, distpos.index.tolist()],'distpos']  = distpos.values
                dist = distpos.to_distance()
                self._session.loc[pd.IndexSlice[index, dist.index.tolist()],'dist']  = dist.values
        return self._session

    def speed(self, from_distances=False, to_special_column=True, **kwargs):
        for index in self._session.index.unique(level='start'):
                speed = self._session.xs(index, level=0).compute.speed(from_distances=from_distances,
                    to_special_column=to_special_column, **kwargs)
                self._session.loc[pd.IndexSlice[index, speed.index.tolist()],'speed']  = speed.values
        return self._session

    def vertical_speed(self, to_special_column=True, **kwargs):
        for index in self._session.index.unique(level='start'):
                vam = self._session.xs(index, level=0).compute.vertical_speed(
                    to_special_column=to_special_column, **kwargs)
                self._session.loc[pd.IndexSlice[index, vam.index.tolist()],'vam']  = vam.values
        return self._session

    def gradient(self, to_special_column=True, **kwargs):
        for index in self._session.index.unique(level='start'):
                grad = self._session.xs(index, level=0).compute.gradient(
                    to_special_column=to_special_column, **kwargs)
                self._session.loc[pd.IndexSlice[index, grad.index.tolist()],'grad']  = grad.values
        return self._session

    def pace(self, to_special_column=True, **kwargs):
        for index in self._session.index.unique(level='start'):
                pace = self._session.xs(index, level=0).compute.pace(
                    to_special_column=to_special_column, **kwargs)
                self._session.loc[pd.IndexSlice[index, pace.index.tolist()],'pace']  = pace.values
        return self._session

    def heart_zone(self, bins, labels, **kwargs):
        for index in self._session.index.unique(level='start'):
                hr_zone = self._session.xs(index, level=0).compute.heart_zone(
                    bins=bins, labels=labels, **kwargs)
                self._session.loc[pd.IndexSlice[index, hr_zone.index.tolist()],'hr_zone']  = hr_zone.values
        return self._session

    def only_moving(self, threshold=0.8):
        for index in self._session.index.unique(level='start'):
            moving_series = self._session.xs(index, level=0).only_moving(threshold=threshold)['moving']
            self._session.loc[pd.IndexSlice[index, moving_series.index.tolist()],'moving']  = moving_series.values
        return self._session