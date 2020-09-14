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

def test_read_file_tcx_basic_dataframe(dirpath):
        tcx_file = os.path.join(dirpath, "tcx", "basic.tcx")
        activity = reader._read_file(tcx_file, to_df=True)
        assert isinstance(activity, DataFrame)
        included_data = set(['latitude_degrees', 'longitude_degrees', 'altitude_meters', 'distance_meters', 'heart_rate_bpm'])
        assert included_data <= set(activity.columns.to_list())
        assert  activity.size == 1920

def test_read_file_tcx_basic_activity(dirpath):
        tcx_file = os.path.join(dirpath, "tcx", "basic.tcx")
        activity = reader._read_file(tcx_file, to_df=False)
        assert type(activity) is types.Activity
        included_data = set(['lat', 'lon', 'alt', 'dist', 'hr'])
        assert included_data <= set(activity.columns.to_list())

        assert activity.size == 1920