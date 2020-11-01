"""
Test module for TCX reader base module
"""

import os
import pytest
from pandas import DataFrame, Timedelta, Timestamp
from runpandas import reader
from runpandas import types

pytestmark = pytest.mark.stable


@pytest.fixture
def dirpath(datapath):
    return datapath("io", "data")


@pytest.fixture
def pandas_activity(dirpath):
    tcx_file = os.path.join(dirpath, "tcx", "basic.tcx")
    return reader._read_file(tcx_file, to_df=True)


@pytest.fixture
def runpandas_activity(dirpath):
    tcx_file = os.path.join(dirpath, "tcx", "basic.tcx")
    return reader._read_file(tcx_file, to_df=False)


test_data = [
    (pytest.lazy_fixture("pandas_activity"), "heart_rate_bpm", 0, 62),
    (pytest.lazy_fixture("pandas_activity"), "heart_rate_bpm", -1, 180),
    (pytest.lazy_fixture("pandas_activity"), "altitude_meters", 0, 178.942626953),
    (pytest.lazy_fixture("pandas_activity"), "altitude_meters", -1, 166.4453125),
    (pytest.lazy_fixture("pandas_activity"), "latitude_degrees", 0, 35.951880198),
    (pytest.lazy_fixture("pandas_activity"), "longitude_degrees", 0, -79.0931872185),
    (pytest.lazy_fixture("pandas_activity"), "distance_meters", -1, 4686.31103516),
    (pytest.lazy_fixture("pandas_activity"), "distance_meters", 0, 0.0),
    (pytest.lazy_fixture("runpandas_activity"), "hr", 0, 62),
    (pytest.lazy_fixture("runpandas_activity"), "hr", -1, 180),
    (pytest.lazy_fixture("runpandas_activity"), "alt", 0, 178.942626953),
    (pytest.lazy_fixture("runpandas_activity"), "alt", -1, 166.4453125),
    (pytest.lazy_fixture("runpandas_activity"), "lat", 0, 35.951880198),
    (pytest.lazy_fixture("runpandas_activity"), "lon", 0, -79.0931872185),
    (pytest.lazy_fixture("runpandas_activity"), "dist", -1, 4686.31103516),
    (pytest.lazy_fixture("runpandas_activity"), "dist", 0, 0.0),
]


@pytest.mark.parametrize("activity,column,index,expected", test_data)
def test_tcx_values(activity, column, index, expected):
    assert activity[column].iloc[index] == expected
    assert activity.index[-1] == Timedelta("0 days 00:33:11")

    if isinstance(activity, types.Activity):
        assert activity.start == Timestamp("2012-12-26 21:29:53+00:00")


def test_read_file_tcx_basic_dataframe(dirpath):
    tcx_file = os.path.join(dirpath, "tcx", "basic.tcx")
    activity = reader._read_file(tcx_file, to_df=True)
    assert isinstance(activity, DataFrame)
    included_data = set(
        [
            "latitude_degrees",
            "longitude_degrees",
            "altitude_meters",
            "distance_meters",
            "heart_rate_bpm",
        ]
    )
    assert included_data <= set(activity.columns.to_list())
    assert activity.size == 1915


def test_read_file_tcx_basic_activity(dirpath):
    tcx_file = os.path.join(dirpath, "tcx", "basic.tcx")
    activity = reader._read_file(tcx_file, to_df=False)
    assert type(activity) is types.Activity
    included_data = set(["lat", "lon", "alt", "dist", "hr"])
    assert included_data <= set(activity.columns.to_list())
    assert activity.size == 1915
