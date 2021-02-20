'''
This is a module for extending pandas dataframes with the runpandas toolbox
'''

import pandas as pd
import numpy as np
from runpandas._utils import special_column
from runpandas.types import Activity
from haversine import haversine as hv
from haversine import Unit

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
        if not isinstance(activity.index, (pd.DatetimeIndex, pd.TimedeltaIndex)):
            raise AttributeError("An activity needs a DataFrame Index in DateTimeIndex format")

    @special_column(required_columns=('lat','lon'), name='dist')
    def distance(self, distance_formula='haversine', **kwargs):
        #TODO: MUST OPTIMIZE THIS SECTION FOR HAVERSINE CALCULATION!
        self._activity['point'] = self._activity.apply(lambda x: (x['lat'], x['lon']), axis=1)
        self._activity['point_next'] = self._activity['point'].shift(1)
        self._activity.loc[self._activity['point_next'].isna(), 'point_next'] = None
        haversine_dist = self._activity.apply(lambda x: hv(x['point'], x['point_next'], unit=Unit.METERS) if x['point_next'] is not None else float('nan'),  axis=1)
        self._activity = self._activity.drop(['point_next', 'point'], axis=1)
        return haversine_dist