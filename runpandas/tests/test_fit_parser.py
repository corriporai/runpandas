'''
Test module for FIT reader base module
'''

import os
import pytest
from pandas import DataFrame, TimedeltaIndex
from runpandas import reader
from runpandas import exceptions
from runpandas import types

@pytest.fixture
def dirpath(datapath):
    return datapath("io", "data")

def test_read_file_fit_basic_dataframe(dirpath):
    fit_file = os.path.join(dirpath, "fit", "garmin-fenix-5-basic.fit")
    activity = reader._read_file(fit_file, to_df=True)
    assert isinstance(activity, DataFrame)
    assert isinstance(activity.index, TimedeltaIndex)
    assert  activity.size == 462
    included_data = set(['position_lat', 'position_long', 'distance', 'temperature', 'altitude',
                    'speed', 'heart_rate', 'cadence', 'speed', 'lap', 'session'])
    assert included_data <= set(activity.columns.to_list())

def test_read_file_fit_basic_activity(dirpath):
    gpx_file = os.path.join(dirpath, "fit", "garmin-fenix-5-basic.fit")
    activity = reader._read_file(gpx_file, to_df=False)
    assert type(activity) is types.Activity
    assert isinstance(activity.index, TimedeltaIndex)
    assert  activity.size == 462

    included_data = set(['lat', 'lon', 'alt', 'cad', 'hr'])
    assert included_data <= set(activity.columns.to_list())