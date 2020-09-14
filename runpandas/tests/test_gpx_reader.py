'''
Test module for TCX reader base module
'''

import os
import pytest
from pandas import DataFrame
from runpandas import reader
from runpandas import exceptions
from runpandas import types

@pytest.fixture
def dirpath(datapath):
    return datapath("io", "data")

def test_read_file_gpx_basic_dataframe(dirpath):
    gpx_file = os.path.join(dirpath, "gpx", "garmin_connect.gpx")
    activity = reader._read_file(gpx_file, to_df=True)
    assert isinstance(activity, DataFrame)
    print(activity.head())
    assert  activity.size == 9

    #included_data = set(['latitude_degrees', 'longitude_degrees', 'altitude_meters', 'distance_meters', 'heart_rate_bpm'])
    #assert included_data <= set(activity.columns.to_list())
    #assert  activity.size == 1920
