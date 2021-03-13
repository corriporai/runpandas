"""
Test module for runpandas frame types (i.e. Activity)
"""


import os
import pytest
from pandas import Timedelta
from runpandas import reader

pytestmark = pytest.mark.stable


@pytest.fixture
def dirpath(datapath):
    return datapath("io", "data")


def test_ellapsed_time_frame(dirpath):

    gpx_file = os.path.join(dirpath, "gpx", "stopped_example.gpx")
    frame_gpx = reader._read_file(gpx_file, to_df=False)
    reset_gpx_file = frame_gpx.reset_index()
    with pytest.raises(AttributeError):
        _ = reset_gpx_file.ellapsed_time

    gpx_file = os.path.join(dirpath, "gpx", "stopped_example.gpx")
    frame_gpx = reader._read_file(gpx_file, to_df=False)
    assert frame_gpx.ellapsed_time == Timedelta("0 days 01:25:27")

    tcx_file = os.path.join(dirpath, "tcx", "basic.tcx")
    frame_tcx = reader._read_file(tcx_file, to_df=False)
    assert frame_tcx.ellapsed_time == Timedelta("0 days 00:33:11")

    fit_file = os.path.join(dirpath, "fit", "garmin-fenix-5-basic.fit")
    frame_fit = reader._read_file(fit_file, to_df=False)
    assert frame_fit.ellapsed_time == Timedelta("0 days 00:00:57")


def test_moving_time_frame(dirpath):
    gpx_file = os.path.join(dirpath, "gpx", "stopped_example.gpx")
    frame_gpx = reader._read_file(gpx_file, to_df=False)
    reset_gpx_file = frame_gpx.reset_index()
    with pytest.raises(AttributeError):
        _ = reset_gpx_file.moving_time

    gpx_file = os.path.join(dirpath, "gpx", "stopped_example.gpx")
    frame_without_moving = reader._read_file(gpx_file, to_df=False)
    with pytest.raises(AttributeError):
        _ = frame_without_moving.moving_time

    gpx_file = os.path.join(dirpath, "gpx", "stopped_example.gpx")
    frame_gpx = reader._read_file(gpx_file, to_df=False)
    frame_gpx["distpos"] = frame_gpx.compute.distance(correct_distance=False)
    frame_gpx["speed"] = frame_gpx.compute.speed(from_distances=True)
    frame_gpx_only_moving = frame_gpx.only_moving()
    assert frame_gpx_only_moving.moving_time == Timedelta("0 days 01:14:46")

    tcx_file = os.path.join(dirpath, "tcx", "basic.tcx")
    frame_tcx = reader._read_file(tcx_file, to_df=False)
    frame_tcx["distpos"] = frame_tcx.compute.distance(correct_distance=False)
    frame_tcx["speed"] = frame_tcx.compute.speed(from_distances=True)
    frame_tcx = frame_tcx.only_moving()
    assert frame_tcx.moving_time == Timedelta("0 days 00:33:05")

    fit_file = os.path.join(dirpath, "fit", "garmin-fenix-5-basic.fit")
    frame_fit = reader._read_file(fit_file, to_df=False)
    frame_fit_only_moving = frame_fit.only_moving()
    assert frame_fit_only_moving.moving_time == Timedelta("0 days 00:00:55")


def test_distance_frame(dirpath):

    gpx_file = os.path.join(dirpath, "gpx", "stopped_example.gpx")
    frame_no_distance = reader._read_file(gpx_file, to_df=False)
    with pytest.raises(KeyError):
        _ = frame_no_distance.distance

    frame_gpx = reader._read_file(gpx_file, to_df=False)
    frame_gpx["distpos"] = frame_gpx.compute.distance(correct_distance=False)
    assert round(frame_gpx.distance, 2) == 12594.65

    tcx_file = os.path.join(dirpath, "tcx", "basic.tcx")
    frame_tcx = reader._read_file(tcx_file, to_df=False)
    assert round(frame_tcx.distance, 2) == 4686.31

    fit_file = os.path.join(dirpath, "fit", "garmin-fenix-5-basic.fit")
    frame_fit = reader._read_file(fit_file, to_df=False)
    assert round(frame_fit.distance, 2) == 157.56

    tcx_file = os.path.join(dirpath, "tcx", "stopped_example.tcx")
    activity_tcx = reader._read_file(tcx_file, to_df=False)
    assert round(activity_tcx.distance, 2) == 12007.99
