'''
This is a module for extending pandas dataframes with the runpandas toolbox
'''

from os import access
import numpy as np

import pandas as pd


@pd.api.extensions.register_dataframe_accessor("only_moving")
class _InactivityAssessor(object):
    '''
    Dataframe Accessor to impute the periods of inactivity, as such periods must be
    detected and ignored from the analysis for moving time, heart rate, speed, and
    power-based calculations.

    Parameters
    ----------
    remove_stopped_periods: bool default False
        If True, regions of data with speed below a threshold
         will be removed from the data. Default is False.

    Raises
    ------
    AttributeError
        if at least one of the needed columns is missing.

    '''
    # Speeds less than or equal to this value (in m/s) are considered to be stopped
    STOPPED_THRESHOLD = 0.3

    required_columns = ['speed']

    def __init__(self, activity):
        self._validate(activity)
        self.activity = activity

    def __call__(self, threshold=STOPPED_THRESHOLD):
        '''
        When the speed of a record drops below the threshold speed a 'false' event
        is set to the 'moving'column, and when the speed rises above the
        threshold speed a 'true' event is set to the 'moving' column.
        '''
        #get the time difference between tracking positions and resample it to 1s
        time_diff = (self.activity.index.to_series().diff().fillna(self.activity.index[0]))/np.timedelta64(1,'s')
        #remove all instantaneous with speed below threashold
        self.activity['moving'] = (self.activity['speed'] >= threshold)
        return self.activity

    @staticmethod
    def _validate(activity):
        if not isinstance(activity.index, (pd.DatetimeIndex, pd.TimedeltaIndex)):
            raise AttributeError("An activity needs a DataFrame Index in DateTimeIndex format")

        if any([c not in activity.columns for c in _InactivityAssessor.required_columns]):
            raise AttributeError('To compute the periods of inactivity, ' \
                                +  'it must have the properties [%s].' \
                                 % (', '.join(_InactivityAssessor.required_columns)))