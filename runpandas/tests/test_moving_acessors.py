"""
Test module for runpandas acessors
"""

import os
import pytest
from runpandas import reader


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
        frame_without_index.only_moving()

    #dataframe without speed column
    with pytest.raises(AttributeError):
        activity_gpx.only_moving()

    tcx_file = os.path.join(dirpath, "tcx", "stopped_example.tcx")
    activity_tcx = reader._read_file(tcx_file, to_df=True)

    #copy of dataframe for testing the index error
    frame_without_index = activity_tcx.copy()
    frame_without_index = frame_without_index.reset_index()
    with pytest.raises(AttributeError):
        frame_without_index.only_moving()

def test_only_moving_acessor(dirpath):
    gpx_file = os.path.join(dirpath, "gpx", "stopped_example.gpx")
    frame_gpx = reader._read_file(gpx_file, to_df=False)
    frame_gpx['dist'] = frame_gpx.compute.distance()
    #frame_gpx['speed'] = frame_gpx.compute.speed()
    #frame_gpx.only_moving()

    tcx_file = os.path.join(dirpath, "tcx", "stopped_example.tcx")
    activity_tcx = reader._read_file(tcx_file, to_df=True)
    #activity_marked_stopped= activity_tcx.only_moving()
    #frame_tcx = reader._read_file(tcx_file, to_df=False)