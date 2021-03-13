"""
Test module for runpandas acessors
"""

import os

import pytest
from runpandas import reader
from runpandas.exceptions import RequiredColumnError
from runpandas.types import columns

pytestmark = pytest.mark.stable


@pytest.fixture
def dirpath(datapath):
    return datapath("io", "data")


@pytest.fixture
def pandas_gpx_activity(dirpath):
    gpx_file = os.path.join(dirpath, "gpx", "stopped_example.gpx")
    return reader._read_file(gpx_file, to_df=True)


@pytest.fixture
def runpandas_gpx_activity(dirpath):
    gpx_file = os.path.join(dirpath, "gpx", "stopped_example.gpx")
    return reader._read_file(gpx_file, to_df=False)


@pytest.fixture
def pandas_tcx_activity(dirpath):
    tcx_file = os.path.join(dirpath, "tcx", "stopped_example.tcx")
    return reader._read_file(tcx_file, to_df=True)


@pytest.fixture
def runpandas_tcx_activity(dirpath):
    tcx_file = os.path.join(dirpath, "tcx", "stopped_example.tcx")
    return reader._read_file(tcx_file, to_df=False)


def test_metrics_validate(dirpath):
    gpx_file = os.path.join(dirpath, "gpx", "stopped_example.gpx")

    with pytest.raises(AssertionError):
        activity_gpx = reader._read_file(gpx_file, to_df=True)
        activity_gpx.compute.speed()

    activity_gpx = reader._read_file(gpx_file, to_df=False)

    # copy of dataframe for testing the index error
    frame_without_index = activity_gpx.copy()
    frame_without_index = frame_without_index.reset_index()
    with pytest.raises(AttributeError):
        frame_without_index.compute.speed()

    # test the decorator special_column
    activity_without_required_column = activity_gpx.drop(["lat"], axis=1)
    with pytest.raises(RequiredColumnError):
        activity_without_required_column.compute.distance()

    activity_without_required_column = activity_gpx.drop(["alt"], axis=1)
    with pytest.raises(RequiredColumnError):
        activity_without_required_column.compute.distance(
            correct_distance=True, to_special_column=False
        )


test_distance_pos_data = [
    (pytest.lazy_fixture("runpandas_gpx_activity"), "distpos", -1, 5.093437453100809),
    (pytest.lazy_fixture("runpandas_gpx_activity"), "distpos", 2, 5.11816186976935),
    (pytest.lazy_fixture("runpandas_tcx_activity"), "distpos", -1, 5.093437453100809),
    (pytest.lazy_fixture("runpandas_tcx_activity"), "distpos", 2, 5.11816186976935),
]


@pytest.mark.parametrize("activity,column,index,expected", test_distance_pos_data)
def test_metrics_distance(activity, column, index, expected):
    activity["distpos"] = activity.compute.distance(to_special_column=False)
    assert activity[column].iloc[index] == expected


test_correct_distance_pos_data = [
    (pytest.lazy_fixture("runpandas_gpx_activity"), "distpos", -1, 5.093437453100809),
    (pytest.lazy_fixture("runpandas_gpx_activity"), "distpos", 2, 5.11816186976935),
    (pytest.lazy_fixture("runpandas_tcx_activity"), "distpos", -1, 5.093444269601765),
    (pytest.lazy_fixture("runpandas_tcx_activity"), "distpos", 2, 5.118301239044248),
]


@pytest.mark.parametrize(
    "activity,column,index,expected", test_correct_distance_pos_data
)
def test_metrics_corrected_distance(activity, column, index, expected):
    activity["distpos"] = activity.compute.distance(
        correct_distance=True, to_special_column=False
    )
    assert activity[column].iloc[index] == expected


test_full_distpos_data = [
    (pytest.lazy_fixture("runpandas_gpx_activity"), "distpos", -1, 5.093437453100809),
    (pytest.lazy_fixture("runpandas_gpx_activity"), "distpos", 2, 5.11816186976935),
    (pytest.lazy_fixture("runpandas_tcx_activity"), "distpos", -1, 5.093437453100809),
    (pytest.lazy_fixture("runpandas_tcx_activity"), "distpos", 2, 5.11816186976935),
]


@pytest.mark.parametrize("activity,column,index,expected", test_full_distpos_data)
def test_metrics_distance_per_position(activity, column, index, expected):
    activity["distpos"] = activity.compute.distance(to_special_column=True)
    assert isinstance(activity["distpos"], columns.DistancePerPosition)
    assert activity[column].iloc[index] == expected


test_speed_data = [
    (pytest.lazy_fixture("runpandas_gpx_activity"), "speed", -1, 5.093437453100809),
    (pytest.lazy_fixture("runpandas_gpx_activity"), "speed", 2, 5.11816186976935),
    (pytest.lazy_fixture("runpandas_tcx_activity"), "speed", -1, 5.093437453100809),
    (pytest.lazy_fixture("runpandas_tcx_activity"), "speed", 2, 5.11816186976935),
]


def test_speed_validate(dirpath):
    gpx_file = os.path.join(dirpath, "gpx", "stopped_example.gpx")

    with pytest.raises(RequiredColumnError):
        activity_gpx = reader._read_file(gpx_file, to_df=False)
        assert "dist_pos" not in activity_gpx.columns
        activity_gpx.compute.speed(from_distances=True)

    with pytest.raises(RequiredColumnError):
        activity_gpx = reader._read_file(gpx_file, to_df=False)
        assert "speed" not in activity_gpx.columns
        activity_gpx.compute.speed(from_distances=False)

    with pytest.raises(RequiredColumnError):
        activity_gpx = reader._read_file(gpx_file, to_df=False)
        assert "speed" not in activity_gpx.columns
        activity_gpx.compute.speed(from_distances=False)


test_speed_gpx_data = [
    (pytest.lazy_fixture("runpandas_gpx_activity"), "speed", -1, 2.5467187265504045),
    (pytest.lazy_fixture("runpandas_gpx_activity"), "speed", 2, 2.559080934884675),
]


@pytest.mark.parametrize("activity,column,index,expected", test_speed_gpx_data)
def test_metrics_from_distances_speed(activity, column, index, expected):
    activity["distpos"] = activity.compute.distance(correct_distance=True)
    activity["speed"] = activity.compute.speed(from_distances=True)
    assert activity[column].iloc[index] == expected


test_speed_tcx_data = [
    (pytest.lazy_fixture("runpandas_tcx_activity"), "speed", -1, 2.36077),
    (pytest.lazy_fixture("runpandas_tcx_activity"), "speed", 3, 2.222973),
]


@pytest.mark.parametrize("activity,column,index,expected", test_speed_tcx_data)
def test_metrics_from_recording_speed(activity, column, index, expected):
    activity["speed"] = activity.compute.speed(from_distances=False)
    assert activity[column].iloc[index] == expected
