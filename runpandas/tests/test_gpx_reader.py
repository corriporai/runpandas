"""
Test module for TCX reader base module
"""

import os
import pytest
from pandas import DataFrame, Timedelta, TimedeltaIndex, Timestamp
from runpandas import reader
from runpandas import types

pytestmark = pytest.mark.stable


@pytest.fixture
def dirpath(datapath):
    return datapath("io", "data")


@pytest.fixture
def pandas_activity(dirpath):
    gpx_file = os.path.join(dirpath, "gpx", "garmin_connect.gpx")
    return reader._read_file(gpx_file, to_df=True)


@pytest.fixture
def runpandas_activity(dirpath):
    gpx_file = os.path.join(dirpath, "gpx", "garmin_connect.gpx")
    return reader._read_file(gpx_file, to_df=False)


test_data = [
    (
        pytest.lazy_fixture("pandas_activity"),
        "hr",
        0,
        120,
    ),
    (
        pytest.lazy_fixture("pandas_activity"),
        "hr",
        -1,
        130,
    ),
    (
        pytest.lazy_fixture("pandas_activity"),
        "ele",
        0,
        23.6000003814697265625,
    ),
    (
        pytest.lazy_fixture("pandas_activity"),
        "ele",
        -1,
        23.799999237060546875,
    ),
    (
        pytest.lazy_fixture("pandas_activity"),
        "lat",
        0,
        51.43788929097354412078857421875,
    ),
    (
        pytest.lazy_fixture("pandas_activity"),
        "lon",
        0,
        6.617012657225131988525390625,
    ),
    (
        pytest.lazy_fixture("pandas_activity"),
        "cad",
        -1,
        80,
    ),
    (
        pytest.lazy_fixture("pandas_activity"),
        "cad",
        0,
        70,
    ),
    (
        pytest.lazy_fixture("runpandas_activity"),
        "hr",
        0,
        120,
    ),
    (
        pytest.lazy_fixture("runpandas_activity"),
        "hr",
        -1,
        130,
    ),
    (
        pytest.lazy_fixture("runpandas_activity"),
        "alt",
        0,
        23.6000003814697265625,
    ),
    (
        pytest.lazy_fixture("runpandas_activity"),
        "alt",
        -1,
        23.799999237060546875,
    ),
    (
        pytest.lazy_fixture("runpandas_activity"),
        "lat",
        0,
        51.43788929097354412078857421875,
    ),
    (
        pytest.lazy_fixture("runpandas_activity"),
        "lon",
        0,
        6.617012657225131988525390625,
    ),
    (
        pytest.lazy_fixture("runpandas_activity"),
        "cad",
        -1,
        80,
    ),
    (
        pytest.lazy_fixture("runpandas_activity"),
        "cad",
        0,
        70,
    ),
]


@pytest.mark.parametrize("activity,column,index,expected", test_data)
def test_gpx_values(activity, column, index, expected):
    assert activity[column].iloc[index] == expected
    assert activity.index[-1] == Timedelta("0 days 00:00:02")

    if isinstance(activity, types.Activity):
        assert activity.start == Timestamp("2018-02-21 14:30:50+00:00")


def test_read_file_gpx_basic_dataframe(dirpath):
    gpx_file = os.path.join(dirpath, "gpx", "garmin_connect.gpx")
    activity = reader._read_file(gpx_file, to_df=True)
    assert isinstance(activity, DataFrame)
    assert isinstance(activity.index, TimedeltaIndex)

    assert activity.size == 15
    included_data = set(["lat", "lon", "ele", "cad", "hr"])
    assert included_data <= set(activity.columns.to_list())


def test_read_file_gpx_basic_activity(dirpath):
    gpx_file = os.path.join(dirpath, "gpx", "garmin_connect.gpx")
    activity = reader._read_file(gpx_file, to_df=False)
    assert type(activity) is types.Activity
    assert isinstance(activity.index, TimedeltaIndex)
    assert activity.size == 15
    included_data = set(["lat", "lon", "alt", "cad", "hr"])
    assert included_data <= set(activity.columns.to_list())
