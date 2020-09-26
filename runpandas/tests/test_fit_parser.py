'''
Test module for FIT reader base module
'''

import os
import pytest
from pandas import DataFrame, TimedeltaIndex
from runpandas import reader
from runpandas import exceptions
from runpandas import types
import runpandas.io.fit._parser as fit_parser
from fitparse.utils import FitParseError

@pytest.fixture
def dirpath(datapath):
    return datapath("io", "data")

def test_read_file_fit_no_fit(dirpath):
    gpx_file = os.path.join(dirpath, "gpx", "garmin_connect.gpx")
    with pytest.raises(FitParseError):
        activity = fit_parser.read(gpx_file)

def test_read_file_fit_basic_dataframe(dirpath):
    fit_file = os.path.join(dirpath, "fit", "garmin-fenix-5-basic.fit")
    activity = reader._read_file(fit_file, to_df=True)
    assert isinstance(activity, DataFrame)
    assert isinstance(activity.index, TimedeltaIndex)
    assert  activity.size == 462
    included_data = set(['position_lat', 'position_long', 'distance', 'temperature', 'altitude',
                    'speed', 'heart_rate', 'cadence', 'speed', 'lap', 'session'])
    assert included_data <= set(activity.columns.to_list())

    assert "lap" in activity.columns
    assert activity["lap"].max() == 0 #no laps

    assert "session" in activity.columns
    assert activity["session"].max() == 0 #no sessions


def test_read_file_fit_basic_activity(dirpath):
    gpx_file = os.path.join(dirpath, "fit", "garmin-fenix-5-basic.fit")
    activity = reader._read_file(gpx_file, to_df=False)
    assert type(activity) is types.Activity
    assert isinstance(activity.index, TimedeltaIndex)
    assert  activity.size == 462

    included_data = set(['lat', 'lon', 'alt', 'cad', 'hr'])
    assert included_data <= set(activity.columns.to_list())

    assert "lap" in activity.columns
    assert activity["lap"].max() == 0 #no laps

    assert "session" in activity.columns
    assert activity["session"].max() == 0 #no sessions

