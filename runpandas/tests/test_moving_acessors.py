"""
Test module for runpandas acessors
"""

import os
import pytest
import numpy as np
from pandas import Timedelta
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
    frame_gpx['distpos'] = frame_gpx.compute.distance(correct_distance=False)
    frame_gpx['speed'] = frame_gpx.compute.speed(from_distances=True)
    frame_gpx_only_moving = frame_gpx.only_moving()
    assert frame_gpx_only_moving[frame_gpx_only_moving['moving']==False].shape[0] == 74
    assert  frame_gpx_only_moving.ellapsed_time == Timedelta("0 days 01:25:27")
    assert  frame_gpx_only_moving.moving_time == Timedelta("0 days 01:14:46")

    tcx_file = os.path.join(dirpath, "tcx", "stopped_example.tcx")
    activity_tcx = reader._read_file(tcx_file, to_df=False)
    frame_tcx_only_moving = activity_tcx.only_moving()
    assert frame_tcx_only_moving[frame_gpx_only_moving.moving  == False].shape[0] == 74
    assert  frame_tcx_only_moving.ellapsed_time == Timedelta("0 days 01:25:27")
    assert  frame_tcx_only_moving.moving_time == Timedelta("0 days 01:23:57")


    fit_file = os.path.join(dirpath, "fit", "garmin-fenix-5-basic.fit")
    fit_file = reader._read_file(fit_file, to_df=False)
    frame_fit_only_moving = fit_file.only_moving()
    assert  frame_fit_only_moving.ellapsed_time == Timedelta("0 days 00:00:57")
    assert  frame_fit_only_moving.moving_time == Timedelta("0 days 00:00:55")

    tcx_file2 = os.path.join(dirpath, "tcx", "basic.tcx")
    frame_tcx_basic = reader._read_file(tcx_file2, to_df=False)
    frame_tcx_basic['distpos'] = frame_tcx_basic.compute.distance(correct_distance=False)
    frame_tcx_basic['speed'] = frame_tcx_basic.compute.speed(from_distances=True)
    frame_tcx2_only_moving = frame_tcx_basic.only_moving()
    assert  frame_tcx2_only_moving.ellapsed_time == Timedelta("0 days 00:33:11")
    assert  frame_tcx2_only_moving.moving_time == Timedelta("0 days 00:33:05")

