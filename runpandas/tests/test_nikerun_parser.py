"""
Test module for NikeRun reader base module
"""

import os
import pytest
from pandas import DataFrame, Timedelta, TimedeltaIndex, Timestamp
from runpandas import read_nikerun, read_dir_nikerun
from runpandas import types
from runpandas import exceptions

pytestmark = pytest.mark.stable


@pytest.fixture(scope="session")
def temp_dir(tmpdir_factory):
    return tmpdir_factory.mktemp("data")


@pytest.fixture(scope="session")
def valid_nikerun_filename(tmpdir_factory):
    return tmpdir_factory.getbasetemp().join("activity.json")


@pytest.fixture
def dirpath(datapath):
    return datapath("io", "data")


@pytest.fixture
def pandas_activity(dirpath):
    json_file = os.path.join(dirpath, "nikerun", "sample_nikerun.json")
    return read_nikerun(json_file, to_df=True)


@pytest.fixture
def runpandas_activity(dirpath):
    json_file = os.path.join(dirpath, "nikerun", "sample_nikerun.json")
    return read_nikerun(json_file, to_df=False)


def test_read_file_not_exists(valid_nikerun_filename):
    with pytest.raises(IOError):
        read_nikerun(valid_nikerun_filename)


def test_read_file_invalid_nikerun_file(dirpath):
    json_file = os.path.join(dirpath, "gpx", "run.gpx")
    with pytest.raises(exceptions.InvalidFileError):
        read_nikerun(json_file)


def test_read_file_malformed_nikerun_file(dirpath):
    json_file = os.path.join(dirpath, "nikerun", "malformed_metrics.json")
    with pytest.raises(exceptions.InvalidFileError):
        read_nikerun(json_file)


def test_read_file_malformed_lat_lon_nikerun_file(dirpath):
    json_file = os.path.join(dirpath, "nikerun", "malformed_lat_lon.json")
    with pytest.raises(exceptions.InvalidFileError):
        read_nikerun(json_file)


def test_read_file_malformed_lat_nikerun_file(dirpath):
    json_file = os.path.join(dirpath, "nikerun", "malformed_lat.json")
    with pytest.raises(exceptions.InvalidFileError):
        read_nikerun(json_file)


def test_read_file_outofsync_nikerun_file(dirpath):
    json_file = os.path.join(dirpath, "nikerun", "outofsync.json")
    with pytest.raises(ValueError):
        read_nikerun(json_file)


def test_read_file_nikerun_basic_dataframe(dirpath):
    json_file = os.path.join(dirpath, "nikerun", "sample_nikerun.json")
    activity = read_nikerun(json_file, to_df=True)
    assert isinstance(activity, DataFrame)
    assert isinstance(activity.index, TimedeltaIndex)

    assert activity.size == 2828
    included_data = set(
        [
            "latitude",
            "longitude",
            "elevation",
            "calories",
            "heart_rate",
            "nikefuel",
            "steps",
        ]
    )
    assert included_data <= set(activity.columns.to_list())


def test_read_file_nikerun_basic_activity(dirpath):
    json_file = os.path.join(dirpath, "nikerun", "sample_nikerun.json")
    activity = read_nikerun(json_file, to_df=False)
    assert isinstance(activity, types.Activity)
    assert isinstance(activity.index, TimedeltaIndex)
    assert activity.size == 2828
    included_data = set(["lat", "lon", "alt", "hr", "calories", "nikefuel", "steps"])
    assert included_data <= set(activity.columns.to_list())


test_data = [
    (
        pytest.lazy_fixture("pandas_activity"),
        "latitude",
        0,
        -8.04584830816796,
    ),
    (
        pytest.lazy_fixture("pandas_activity"),
        "longitude",
        0,
        -34.895496899134905,
    ),
    (
        pytest.lazy_fixture("runpandas_activity"),
        "lat",
        0,
        -8.04584830816796,
    ),
    (
        pytest.lazy_fixture("runpandas_activity"),
        "lon",
        0,
        -34.895496899134905,
    ),
]


@pytest.mark.parametrize("activity,column,index,expected", test_data)
def test_nikerun_values(activity, column, index, expected):
    assert activity[column].iloc[index] == expected
    assert activity.index[-1].floor(freq="S") == Timedelta("0 days 00:23:08").floor(
        freq="S"
    )

    if isinstance(activity, types.Activity):
        assert activity.start == Timestamp("2020-08-07 09:15:14+00:00")


def test_empty_read_dir(temp_dir):
    activities = read_dir_nikerun(temp_dir)
    assert activities is None


def test_invalid_dir(dirpath):
    tcx_file = os.path.join(dirpath, "tcx", "basic.tcx")
    with pytest.raises(AssertionError):
        read_dir_nikerun(tcx_file)


def test_read_dir_full_nikerun(dirpath):
    activities_directory = os.path.join(dirpath, "nikerun", "samples")
    session = read_dir_nikerun(activities_directory)
    assert session.session.count() == 5
    assert isinstance(session, types.Activity)
    size_data = set([2828, 3227, 4515, 6244, 9002])
    assert size_data == set(
        [
            session.xs(index, level=0).size
            for index in session.index.unique(level="start")
        ]
    )


def test_read_file_missing_data_nikerun_basic_activity(dirpath):
    json_file = os.path.join(dirpath, "nikerun", "missing_columns_nikerun.json")
    activity = read_nikerun(json_file, to_df=False)
    assert isinstance(activity, types.Activity)
    assert isinstance(activity.index, TimedeltaIndex)
    assert activity.size == 1212
    included_data = set(["lat", "lon", "alt"])
    assert included_data <= set(activity.columns.to_list())
