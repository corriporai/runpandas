"""
Test module for summary statistics module
"""
import os
import pytest
import numpy as np
from pandas import Timedelta, Series, concat, isna
from runpandas import reader, read_dir
from pandas.testing import assert_series_equal


pytestmark = pytest.mark.stable


@pytest.fixture
def dirpath(datapath):
    return datapath("io", "data")


@pytest.fixture
def multi_frame(dirpath):
    sessions_dir = os.path.join(dirpath, "samples")
    activities = [activity for activity in read_dir(sessions_dir)]
    keys = [act.start for act in activities]
    multi_frame = concat(activities, keys=keys, names=["start", "time"], axis=0)
    return multi_frame


@pytest.fixture
def simple_activity(dirpath):
    tcx_file = os.path.join(dirpath, "samples", "2020-12-02T06_08_29-300_Running.tcx")
    frame_tcx = reader._read_file(tcx_file, to_df=False)
    return frame_tcx


def test_activity_summary_with_missing_values(dirpath):
    tcx_file = os.path.join(dirpath, "tcx", "basic.tcx")
    frame_tcx = reader._read_file(tcx_file, to_df=False)
    result = frame_tcx.summary()

    expected = Series(
        [
            "Running: 26-12-2012 21:29:53",
            4686.31,
            Timedelta("0 days 00:33:11"),
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            156.653,
            np.nan,
            np.nan,
        ],
        index=[
            "Session",
            "Total distance (meters)",
            "Total ellapsed time",
            "Total moving time",
            "Average speed (km/h)",
            "Average moving speed (km/h)",
            "Average pace (per 1 km)",
            "Average pace moving (per 1 km)",
            "Average cadence",
            "Average moving cadence",
            "Average heart rate",
            "Average moving heart rate",
            "Average temperature",
        ],
    )
    assert_series_equal(result, expected)


def test_activity_summary_missing_moving(dirpath):
    tcx_file = os.path.join(dirpath, "tcx", "basic.tcx")
    frame_tcx = reader._read_file(tcx_file, to_df=False)
    frame_tcx["distpos"] = frame_tcx.compute.distance(correct_distance=False)
    frame_tcx["speed"] = frame_tcx.compute.speed(from_distances=True)

    # removing hr to simulate the missing values
    frame_tcx.drop("hr", axis=1, inplace=True)

    result = frame_tcx.summary()

    expected = Series(
        [
            "Running: 26-12-2012 21:29:53",
            4686.31,
            Timedelta("0 days 00:33:11"),
            np.nan,
            8.476556294170631,
            np.nan,
            Timedelta("0 days 00:07:04"),
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
        ],
        index=[
            "Session",
            "Total distance (meters)",
            "Total ellapsed time",
            "Total moving time",
            "Average speed (km/h)",
            "Average moving speed (km/h)",
            "Average pace (per 1 km)",
            "Average pace moving (per 1 km)",
            "Average cadence",
            "Average moving cadence",
            "Average heart rate",
            "Average moving heart rate",
            "Average temperature",
        ],
    )
    assert_series_equal(result, expected)


def test_activity_full_summary(dirpath):
    fit_file = os.path.join(dirpath, "fit", "run.fit")
    frame_fit = reader._read_file(fit_file, to_df=False)
    frame_only_moving_fit = frame_fit.only_moving()
    result = frame_only_moving_fit.summary()
    expected = Series(
        [
            "Running: 14-09-2019 15:22:05",
            5839.77,
            Timedelta("0 days 00:52:47"),
            Timedelta("0 days 00:52:21"),
            6.521134575307862,
            6.564336962750716,
            Timedelta("0 days 00:09:12"),
            Timedelta("0 days 00:09:08"),
            63.963394342762065,
            64.0092050209205,
            129.72129783693845,
            129.7623430962343,
            26.905158069883527,
        ],
        index=[
            "Session",
            "Total distance (meters)",
            "Total ellapsed time",
            "Total moving time",
            "Average speed (km/h)",
            "Average moving speed (km/h)",
            "Average pace (per 1 km)",
            "Average pace moving (per 1 km)",
            "Average cadence",
            "Average moving cadence",
            "Average heart rate",
            "Average moving heart rate",
            "Average temperature",
        ],
    )
    assert_series_equal(result, expected)


def test_summary_session(multi_frame, simple_activity):
    multi_frame = multi_frame.session.only_moving()
    summary_frame = multi_frame.session.summarize()
    assert (
        multi_frame.session.count() == summary_frame.shape[0]
    )  # same number of records (activities)

    # check the  first activity summary
    simple_activity_moving = simple_activity.only_moving()
    summary_single_activity = simple_activity_moving.summary()
    # get the same summary from the summary frame
    summary_session_activity = summary_frame.loc[simple_activity.start]
    # compare the results
    assert summary_single_activity.loc["Total distance (meters)"] == pytest.approx(
        summary_session_activity.loc["total_distance"]
    )
    assert summary_single_activity.loc["Total ellapsed time"] == (
        summary_session_activity.loc["ellapsed_time"]
    )
    assert summary_single_activity.loc["Total moving time"] == (
        summary_session_activity.loc["moving_time"]
    )
    assert summary_single_activity.loc["Average speed (km/h)"] == pytest.approx(
        summary_session_activity.loc["mean_speed"] * 3.6
    )
    assert summary_single_activity.loc["Average moving speed (km/h)"] == pytest.approx(
        summary_session_activity.loc["mean_moving_speed"] * 3.6
    )
    assert summary_single_activity.loc["Average pace (per 1 km)"] == (
        summary_session_activity.loc["mean_pace"]
    )
    assert isna(summary_single_activity.loc["Average cadence"])
    assert isna(summary_session_activity.loc["mean_cadence"])
    assert summary_single_activity.loc["Average heart rate"] == pytest.approx(
        summary_session_activity.loc["mean_heart_rate"]
    )
    assert isna(summary_single_activity.loc["Average temperature"])
    assert isna(summary_session_activity.loc["mean_temperature"])
