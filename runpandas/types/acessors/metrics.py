'''
This is a module for extending pandas dataframes with the runpandas toolbox
'''

import pandas as pd
import numpy as np
from haversine import haversine as hv
from haversine import Unit
from runpandas import exceptions
from runpandas._utils import special_column
from runpandas.types import Activity


@pd.api.extensions.register_dataframe_accessor("compute")
class MetricsAcessor(object):
    '''
    Dataframe Accessor to compute all available metrics from an activity

    Raises
    ------
    AttributeError
        if at least one of the needed columns is missing.

    '''
    def __init__(self, activity):
        self._validate(activity)
        self._activity = activity

    @staticmethod
    def _validate(activity):
        assert isinstance(activity, Activity), "Activity is needed for this accessor"

        if not isinstance(activity.index, (pd.DatetimeIndex, pd.TimedeltaIndex)):
            raise AttributeError("An activity needs a DataFrame Index in DateTimeIndex format")

    def __correct_distance(self, distance_series, col_alt='alt'):
        if col_alt not in self._activity.columns:
            raise exceptions.RequiredColumnError(col_alt)
        #TODO: MUST OPTIMIZE THE CORRECTION DISTANCE FORMULA
        self._activity['shift_alt'] = self._activity[col_alt].shift(1)
        self._activity['alt_dif'] = self._activity.apply(lambda x: x['shift_alt'] - x[col_alt], axis=1)
        self._activity['distance_haversine'] = distance_series
        distance_corrected = self._activity.apply(lambda x: np.sqrt(x['distance_haversine']**2 + (x['alt_dif'])**2), axis=1)
        self._activity.drop(['shift_alt', 'alt_dif', 'distance_haversine'], axis=1, inplace=True)

        return distance_corrected


    @special_column(required_columns=('lat','lon'), name='dist')
    def distance(self, correct_distance=False, **kwargs):
        '''
        Calculates the distance in meters using haversine distance formula on an Activity frame.
        -----------------------------------
        correct_distance: bool, optional
            It computes the distance corrected by the altitude. default is False.

        **kwargs : Keyword args to be passed to the `haversine` method

        Returns
        -------
        haversine_dist : pandas.Series
            A Series of floats representing the distance in meters
            with the same index of the accessed activity object.
        '''
        #TODO: MUST OPTIMIZE THIS SECTION FOR HAVERSINE CALCULATION!
        self._activity['point'] = self._activity.apply(lambda x: (x['lat'], x['lon']), axis=1)
        self._activity['point_next'] = self._activity['point'].shift(1)
        self._activity.loc[self._activity['point_next'].isna(), 'point_next'] = None
        haversine_dist = self._activity.apply(lambda x: hv(x['point'], x['point_next'], unit=Unit.METERS) if x['point_next'] is not None else float('nan'),  axis=1)
        self._activity.drop(['point_next', 'point'], axis=1, inplace=True)

        if correct_distance:
            haversine_dist =  self.__correct_distance(haversine_dist)
        return haversine_dist