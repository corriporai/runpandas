"""
Test module for runpandas acessors
"""

import os

import pytest
import pandas as pd
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


def test_vam_validate(dirpath):
    gpx_file = os.path.join(dirpath, "gpx", "stopped_example.gpx")
    activity_gpx = reader._read_file(gpx_file, to_df=False)
    activity_without_required_column = activity_gpx.drop(["alt"], axis=1)
    assert "alt" not in activity_without_required_column.columns
    with pytest.raises(RequiredColumnError):
        activity_without_required_column.compute.vertical_speed()


def test_gradient_validate(dirpath):
    gpx_file = os.path.join(dirpath, "gpx", "stopped_example.gpx")
    activity_gpx = reader._read_file(gpx_file, to_df=False)
    activity_without_required_column = activity_gpx.drop(["alt"], axis=1)
    assert "alt" not in activity_without_required_column.columns
    with pytest.raises(RequiredColumnError):
        activity_without_required_column.compute.gradient()

    activity_gpx = reader._read_file(gpx_file, to_df=False)
    activity_gpx['distpos'] = activity_gpx.compute.distance()
    assert "dist" not in activity_gpx.columns
    with pytest.raises(RequiredColumnError):
        activity_gpx.compute.gradient()



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

test_vam_gpx_data = [
    (pytest.lazy_fixture("runpandas_gpx_activity"), "vam", -4, 0.02499999999999991),
    (pytest.lazy_fixture("runpandas_gpx_activity"), "vam", -5, 0.0),
]

@pytest.mark.parametrize("activity,column,index,expected", test_vam_gpx_data)
def test_metrics_gpx_vam(activity, column, index, expected):
    activity["vam"] = activity.compute.vertical_speed()
    assert activity[column].iloc[index] == expected


test_vam_tcx_data = [
    (pytest.lazy_fixture("runpandas_tcx_activity"), "vam", -1, -0.004166500000000073),
    (pytest.lazy_fixture("runpandas_tcx_activity"), "vam", 3, 0.018022000000000205),
]
@pytest.mark.parametrize("activity,column,index,expected", test_vam_tcx_data)
def test_metrics_tcx_vam(activity, column, index, expected):
    activity["vam"] = activity.compute.vertical_speed()
    assert activity[column].iloc[index] == expected

test_gradient_gpx_data = [
    (pytest.lazy_fixture("runpandas_gpx_activity"), "grad", -4, 0.006652869371284877),
    (pytest.lazy_fixture("runpandas_gpx_activity"), "grad", -5, 0.0),
]

@pytest.mark.parametrize("activity,column,index,expected", test_gradient_gpx_data)
def test_metrics_gpx_gradient(activity, column, index, expected):
    activity["distpos"] = activity.compute.distance()
    activity["dist"] = activity['distpos'].to_distance()
    activity['grad'] = activity.compute.gradient()
    assert activity[column].iloc[index] == expected

test_gradient_tcx_data = [
    (pytest.lazy_fixture("runpandas_tcx_activity"), "grad", -1, -0.0013069369604063105),
    (pytest.lazy_fixture("runpandas_tcx_activity"), "grad", 3, 0.005967282919472209),
]
@pytest.mark.parametrize("activity,column,index,expected", test_gradient_tcx_data)
def test_metrics_tcx_gradient(activity, column, index, expected):
    activity['grad'] = activity.compute.gradient()
    assert activity[column].iloc[index] == expected


def test_pace_validate(dirpath):
    gpx_file = os.path.join(dirpath, "gpx", "stopped_example.gpx")

    with pytest.raises(RequiredColumnError):
        activity_gpx = reader._read_file(gpx_file, to_df=False)
        assert "speed" not in activity_gpx.columns
        activity_gpx.compute.pace()

test_pace_tcx_data = [
    (pytest.lazy_fixture("runpandas_tcx_activity"), "pace", -1, pd.Timedelta('0 days 00:00:00.423590', unit='s')),
    (pytest.lazy_fixture("runpandas_tcx_activity"), "pace", 3, pd.Timedelta('0 days 00:00:00.449848', unit='s')),
]
@pytest.mark.parametrize("activity,column,index,expected", test_pace_tcx_data)
def test_metrics_tcx_pace(activity, column, index, expected):
    activity["speed"] = activity.compute.speed(from_distances=False)
    activity['pace'] = activity.compute.pace()
    assert activity[column].iloc[index].total_seconds() == pytest.approx(expected.total_seconds(), 0.1)



test_pace_gpx_data = [
    (pytest.lazy_fixture("runpandas_gpx_activity"), "pace", -1, pd.Timedelta('0 days 00:00:00.392662', unit='s')),
    (pytest.lazy_fixture("runpandas_gpx_activity"), "pace", 2, pd.Timedelta('0 days 00:00:00.390765', unit='s')),
]

@pytest.mark.parametrize("activity,column,index,expected", test_pace_gpx_data)
def test_metrics_gpx_pace(activity, column, index, expected):
    activity["distpos"] = activity.compute.distance(correct_distance=True)
    activity["speed"] = activity.compute.speed(from_distances=True)
    activity["pace"] = activity.compute.pace()
    assert activity[column].iloc[index].total_seconds() == pytest.approx(expected.total_seconds())
