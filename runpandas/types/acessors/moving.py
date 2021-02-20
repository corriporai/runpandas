'''
This is a module for extending pandas dataframes with the runpandas toolbox
'''

from os import access

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

    required_columns = []

    def __init__(self, activity):
        self._validate(activity)
        self.activity = activity

    def __call__(self, threshold=STOPPED_THRESHOLD):
        #calculate the instant speed
        #remove all instantaneous with speed below threshold
        pass

    @staticmethod
    def _validate(activity):
        if not isinstance(activity.index, (pd.DatetimeIndex, pd.TimedeltaIndex)):
            raise AttributeError("An activity needs a DataFrame Index in DateTimeIndex format")