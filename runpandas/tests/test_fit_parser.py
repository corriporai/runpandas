"""
Test module for FIT reader base module
"""

import os
import pytest
from pandas import DataFrame, TimedeltaIndex, Timedelta, Timestamp
from runpandas import reader
from runpandas import types
import runpandas.io.fit._parser as fit_parser
from fitparse.utils import FitParseError

pytestmark = pytest.mark.stable


@pytest.fixture
def dirpath(datapath):
    return datapath("io", "data")


def test_read_file_fit_no_fit(dirpath):
    gpx_file = os.path.join(dirpath, "gpx", "garmin_connect.gpx")
    with pytest.raises(FitParseError):
        fit_parser.read(gpx_file)


@pytest.fixture
def pandas_activity(dirpath):
    fit_file = os.path.join(dirpath, "fit", "garmin-fenix-5-basic.fit")
    return reader._read_file(fit_file, to_df=True)


@pytest.fixture
def runpandas_activity(dirpath):
    fit_file = os.path.join(dirpath, "fit", "garmin-fenix-5-basic.fit")
    return reader._read_file(fit_file, to_df=False)


test_data = [
    (pytest.lazy_fixture("pandas_activity"), "heart_rate", 0, 61),
    (pytest.lazy_fixture("pandas_activity"), "heart_rate", -1, 112),
    (pytest.lazy_fixture("pandas_activity"), "altitude", 0, 2.1999999999999886),
    (pytest.lazy_fixture("pandas_activity"), "altitude", -1, 4.199999999999989),
    (pytest.lazy_fixture("pandas_activity"), "position_lat", 0, 456099128),
    (pytest.lazy_fixture("pandas_activity"), "position_long", 0, -1463077077),
    (pytest.lazy_fixture("pandas_activity"), "distance", -1, 157.56),
    (pytest.lazy_fixture("pandas_activity"), "distance", 0, 0.0),
    (pytest.lazy_fixture("pandas_activity"), "temperature", 0, 25),
    (pytest.lazy_fixture("pandas_activity"), "temperature", -1, 24),
    (pytest.lazy_fixture("pandas_activity"), "speed", 0, 0.0),
    (pytest.lazy_fixture("pandas_activity"), "speed", -1, 2.865),
    (pytest.lazy_fixture("pandas_activity"), "cadence", 0, 0.0),
    (pytest.lazy_fixture("pandas_activity"), "cadence", -1, 88),
    (pytest.lazy_fixture("runpandas_activity"), "hr", 0, 61),
    (pytest.lazy_fixture("runpandas_activity"), "hr", -1, 112),
    (pytest.lazy_fixture("runpandas_activity"), "alt", 0, 2.1999999999999886),
    (pytest.lazy_fixture("runpandas_activity"), "alt", -1, 4.199999999999989),
    (pytest.lazy_fixture("runpandas_activity"), "lat", 0, 38.22978727519512),
    (pytest.lazy_fixture("runpandas_activity"), "lon", 0, -122.63370391912758),
    (pytest.lazy_fixture("runpandas_activity"), "dist", -1, 157.56),
    (pytest.lazy_fixture("runpandas_activity"), "dist", 0, 0.0),
    (pytest.lazy_fixture("runpandas_activity"), "cad", -1, 88),
    (pytest.lazy_fixture("runpandas_activity"), "cad", 0, 0),
    (pytest.lazy_fixture("runpandas_activity"), "temp", -1, 24),
    (pytest.lazy_fixture("runpandas_activity"), "temp", 0, 25),
    (pytest.lazy_fixture("runpandas_activity"), "speed", -1, 2.865),
    (pytest.lazy_fixture("runpandas_activity"), "speed", 0, 0.0),
]


@pytest.mark.parametrize("activity,column,index,expected", test_data)
def test_fit_values(activity, column, index, expected):
    assert activity[column].iloc[index] == expected
    assert activity.index[-1] == Timedelta("0 days 00:00:57")

    if isinstance(activity, types.Activity):
        assert activity.start == Timestamp("2017-06-11 14:34:09+00:00")


def test_read_file_fit_basic_dataframe(dirpath):
    fit_file = os.path.join(dirpath, "fit", "garmin-fenix-5-basic.fit")
    activity = reader._read_file(fit_file, to_df=True)
    assert isinstance(activity, DataFrame)
    assert isinstance(activity.index, TimedeltaIndex)
    assert activity.size == 462
    included_data = set(
        [
            "position_lat",
            "position_long",
            "distance",
            "temperature",
            "altitude",
            "speed",
            "heart_rate",
            "cadence",
            "speed",
            "lap",
            "session",
        ]
    )
    assert included_data <= set(activity.columns.to_list())

    assert "lap" in activity.columns
    assert activity["lap"].max() == 0  # no laps

    assert "session" in activity.columns
    assert activity["session"].max() == 0  # no sessions


def test_read_file_fit_basic_activity(dirpath):
    gpx_file = os.path.join(dirpath, "fit", "garmin-fenix-5-basic.fit")
    activity = reader._read_file(gpx_file, to_df=False)
    assert type(activity) is types.Activity
    assert isinstance(activity.index, TimedeltaIndex)
    assert activity.size == 462

    included_data = set(["lat", "lon", "alt", "cad", "hr", "speed", "temp"])
    assert included_data <= set(activity.columns.to_list())

    assert "lap" in activity.columns
    assert activity["lap"].max() == 0  # no laps

    assert "session" in activity.columns
    assert activity["session"].max() == 0  # no sessions
