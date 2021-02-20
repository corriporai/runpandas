"""
Test module for runpandas acessors
"""

import os
from urllib.request import Request

import pytest
from runpandas import reader
from runpandas.exceptions import RequiredColumnError

pytestmark = pytest.mark.stable


@pytest.fixture
def dirpath(datapath):
    return datapath("io", "data")


def test_metrics_validate(dirpath):
    gpx_file = os.path.join(dirpath, "gpx", "stopped_example.gpx")
    activity_gpx = reader._read_file(gpx_file, to_df=True)

    #copy of dataframe for testing the index error
    frame_without_index = activity_gpx.copy()
    frame_without_index = frame_without_index.reset_index()
    with pytest.raises(AttributeError):
        frame_without_index.compute.speed()

    #test the decorator special_column
    activity_without_required_column = activity_gpx.drop(['lat'], axis=1)
    with pytest.raises(RequiredColumnError):
        activity_without_required_column.compute.distance()

def test_metrics_distance(dirpath):
    gpx_file = os.path.join(dirpath, "gpx", "stopped_example.gpx")
    activity_gpx = reader._read_file(gpx_file, to_df=True)

    activity_gpx['dist'] = activity_gpx.compute.distance()

    #frame_gpx = reader._read_file(gpx_file, to_df=False)

    #tcx_file = os.path.join(dirpath, "tcx", "stopped_example.tcx")
    #activity_tcx = reader._read_file(tcx_file, to_df=True)
    #frame_tcx = reader._read_file(tcx_file, to_df=False)