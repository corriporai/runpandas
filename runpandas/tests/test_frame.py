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


def test_mean_speed_frame(dirpath):
    gpx_file = os.path.join(dirpath, "gpx", "stopped_example.gpx")
    frame_no_speed = reader._read_file(gpx_file, to_df=False)
    with pytest.raises(AttributeError):
        _ = frame_no_speed.mean_speed()

    frame_gpx = reader._read_file(gpx_file, to_df=False)
    frame_gpx["distpos"] = frame_gpx.compute.distance(correct_distance=False)
    frame_gpx["speed"] = frame_gpx.compute.speed(from_distances=True)
    frame_gpx_only_moving = frame_gpx.only_moving()

    #Calculate the mean speed with only moving  and smoothing using speed (m/s)
    assert (frame_gpx_only_moving.mean_speed(only_moving=True, smoothing=True)) == 2.7966895287728653
    #Calculate the mean speed with only moving  and no smoothing (total distance)
    assert (frame_gpx_only_moving.mean_speed(only_moving=True, smoothing=False)) == 2.7966895287728653

    #Calculate the mean speed with all data  and no smoothing (total distance)
    assert (frame_gpx_only_moving.mean_speed(only_moving=False, smoothing=False)) == 2.4565339871605874
    #Calculate the mean speed with all data  and smoothing (total distance)
    assert (frame_gpx_only_moving.mean_speed(only_moving=False, smoothing=True)) == 2.4565339871605874


def test_mean_heartrate_frame(dirpath):
    gpx_file = os.path.join(dirpath, "gpx", "stopped_example.gpx")
    frame = reader._read_file(gpx_file, to_df=False)
    frame_no_hr = frame.drop(['hr'], axis=1)
    with pytest.raises(AttributeError):
        _ = frame_no_hr.mean_heart_rate()


    frame_gpx = reader._read_file(gpx_file, to_df=False)
    frame_gpx["distpos"] = frame_gpx.compute.distance(correct_distance=False)
    frame_gpx["speed"] = frame_gpx.compute.speed(from_distances=True)

    frame_gpx_only_moving = frame_gpx.only_moving()

    assert (frame_gpx_only_moving.mean_heart_rate(only_moving=False)) == 151.22097819681792
    assert (frame_gpx_only_moving.mean_heart_rate(only_moving=True)) == 151.90203327171903


def test_mean_cadence_frame(dirpath):
    gpx_file = os.path.join(dirpath, "gpx", "stopped_example.gpx")
    frame = reader._read_file(gpx_file, to_df=False)
    frame_no_cadence = frame.drop(['cad'], axis=1)
    with pytest.raises(AttributeError):
        _ = frame_no_cadence.mean_cadence()


    frame_gpx = reader._read_file(gpx_file, to_df=False)
    frame_gpx["distpos"] = frame_gpx.compute.distance(correct_distance=False)
    frame_gpx["speed"] = frame_gpx.compute.speed(from_distances=True)

    frame_gpx_only_moving = frame_gpx.only_moving()

    assert (frame_gpx_only_moving.mean_cadence(only_moving=False)) == 84.99764289923394
    assert (frame_gpx_only_moving.mean_cadence(only_moving=True)) == 85.96118299445472


def test_mean_pace_frame(dirpath):
    gpx_file = os.path.join(dirpath, "gpx", "stopped_example.gpx")
    frame = reader._read_file(gpx_file, to_df=False)
    with pytest.raises(AttributeError):
        _ = frame.mean_pace()


    frame_gpx = reader._read_file(gpx_file, to_df=False)
    frame_gpx["distpos"] = frame_gpx.compute.distance(correct_distance=False)
    frame_gpx["speed"] = frame_gpx.compute.speed(from_distances=True)

    frame_gpx_only_moving = frame_gpx.only_moving()

    #Calculate the mean pace with only moving  and smoothing using speed (m/s)
    assert (frame_gpx_only_moving.mean_pace(only_moving=True, smoothing=True)) == Timedelta('0 days 00:00:00.357566')
    #Calculate the mean pace with only moving  and no smoothing (total distance)
    assert (frame_gpx_only_moving.mean_pace(only_moving=True, smoothing=False)) == Timedelta('0 days 00:00:00.357566')

    #Calculate the mean pace with all data  and no smoothing (total distance)
    assert (frame_gpx_only_moving.mean_pace(only_moving=False, smoothing=False)) == Timedelta('0 days 00:00:00.407078')
    #Calculate the mean pace with all data  and smoothing (total distance)
    assert (frame_gpx_only_moving.mean_pace(only_moving=False, smoothing=True)) == Timedelta('0 days 00:00:00.407078')
