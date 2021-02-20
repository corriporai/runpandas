"""
Test module for runpandas acessors
"""

import os
from urllib.request import Request

import pytest
from runpandas import reader
from runpandas.exceptions import RequiredColumnError
from runpandas.types import Activity

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
    gpx_file = os.path.join(dirpath, "tcx", "stopped_example.tcx")
    return reader._read_file(gpx_file, to_df=True)


@pytest.fixture
def runpandas_tcx_activity(dirpath):
    gpx_file = os.path.join(dirpath, "tcx", "stopped_example.tcx")
    return reader._read_file(gpx_file, to_df=False)


def test_metrics_validate(dirpath):
    gpx_file = os.path.join(dirpath, "gpx", "stopped_example.gpx")

    with pytest.raises(AssertionError):
        activity_gpx = reader._read_file(gpx_file, to_df=True)
        activity_gpx.compute.speed()

    activity_gpx = reader._read_file(gpx_file, to_df=False)

    #copy of dataframe for testing the index error
    frame_without_index = activity_gpx.copy()
    frame_without_index = frame_without_index.reset_index()
    with pytest.raises(AttributeError):
        frame_without_index.compute.speed()

    #test the decorator special_column
    activity_without_required_column = activity_gpx.drop(['lat'], axis=1)
    with pytest.raises(RequiredColumnError):
        activity_without_required_column.compute.distance()

    activity_without_required_column = activity_gpx.drop(['alt'], axis=1)
    with pytest.raises(RequiredColumnError):
        activity_without_required_column.compute.distance(correct_distance=True)




test_data = [
    (pytest.lazy_fixture("runpandas_gpx_activity"), "dist", -1, 5.093437453100809),
    (pytest.lazy_fixture("runpandas_gpx_activity"), "dist", 2, 5.11816186976935),
    (pytest.lazy_fixture("runpandas_tcx_activity"), "dist", -1, 5.093437453100809),
    (pytest.lazy_fixture("runpandas_tcx_activity"), "dist", 2, 5.11816186976935),
]

@pytest.mark.parametrize("activity,column,index,expected", test_data)
def test_metrics_distance(activity, column, index, expected):

    if isinstance(activity, Activity):
        activity['dist'] =  activity.compute.distance()
    else:
        activity['distance_meters'] = activity.compute.distance()

    assert activity[column].iloc[index] == expected

test_correct_data = [
    (pytest.lazy_fixture("runpandas_gpx_activity"), "dist", -1, 5.093437453100809),
    (pytest.lazy_fixture("runpandas_gpx_activity"), "dist", 2, 5.11816186976935),
    (pytest.lazy_fixture("runpandas_tcx_activity"), "dist", -1, 5.093444269601765),
    (pytest.lazy_fixture("runpandas_tcx_activity"), "dist", 2, 5.118301239044248),

]

@pytest.mark.parametrize("activity,column,index,expected", test_correct_data)
def test_metrics_corrected_distance(activity, column, index, expected):

    if isinstance(activity, Activity):
        activity['dist'] =  activity.compute.distance(correct_distance=True)
    else:
        activity['distance_meters'] = activity.compute.distance(correct_distance=True)

    assert activity[column].iloc[index] == expected



    #tcx_file = os.path.join(dirpath, "tcx", "stopped_example.tcx")
    #activity_tcx = reader._read_file(tcx_file, to_df=True)
    #frame_tcx = reader._read_file(tcx_file, to_df=False)