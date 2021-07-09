"""
Test module for runpandas types i.e Sessions
"""


import os
import pytest
from pandas import Timestamp, concat
from runpandas import read_dir, reader
from runpandas.types import columns
from runpandas.exceptions import RequiredColumnError

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


def test_validate_session(multi_frame, dirpath):
    sessions_dir = os.path.join(dirpath, "samples")
    activities = [activity for activity in read_dir(sessions_dir)]

    assert multi_frame.index.levshape[0] == len(activities)
    assert multi_frame.session.count() == multi_frame.index.levshape[0]

    # test validation error (get the activity)
    gpx_file = os.path.join(dirpath, "gpx", "stopped_example.gpx")

    with pytest.raises(AssertionError):  # Activity instance
        activity_gpx = reader._read_file(gpx_file, to_df=True)
        activity_gpx.session.count()

    with pytest.raises(AttributeError):  # index errror
        activity_gpx = reader._read_file(gpx_file, to_df=False)
        activity_gpx.session.count()


def test_count_session(multi_frame, dirpath):
    sessions_dir = os.path.join(dirpath, "samples")
    activities = [activity for activity in read_dir(sessions_dir)]

    assert multi_frame.index.levshape[0] == len(activities)
    assert multi_frame.session.count() == multi_frame.index.levshape[0]


def test_distance_session(multi_frame):
    before_count = multi_frame.session.count()
    before_shape = multi_frame.loc[Timestamp("2020-12-08 09:36:12+00:00")].shape
    multi_frame = multi_frame.session.distance()
    assert "distpos" in multi_frame.columns
    assert "dist" in multi_frame.columns
    assert before_count == multi_frame.session.count()  # same number of sessions.

    after_shape = multi_frame.loc[Timestamp("2020-12-08 09:36:12+00:00")].shape
    assert before_shape[0] == after_shape[0]  # same number of records
    assert before_shape[1] + 1 == after_shape[1]  # number of columns + 1 (distpos)

    assert isinstance(multi_frame["distpos"], columns.DistancePerPosition)


def test_speed_session(multi_frame):
    before_count = multi_frame.session.count()
    before_shape = multi_frame.loc[Timestamp("2020-12-08 09:36:12+00:00")].shape

    multi_frame = multi_frame.session.speed()
    assert "speed" in multi_frame.columns
    assert before_count == multi_frame.session.count()  # same number of sessions.

    after_shape = multi_frame.loc[Timestamp("2020-12-08 09:36:12+00:00")].shape
    assert before_shape[0] == after_shape[0]  # same number of records
    assert before_shape[1] == after_shape[1]  # number of columns (speed)

    with pytest.raises(RequiredColumnError):  # index errror
        multi_frame = multi_frame.session.speed(from_distances=True)

    multi_frame = multi_frame.session.distance()
    multi_frame = multi_frame.session.speed(from_distances=True)

    after_shape = multi_frame.loc[Timestamp("2020-12-08 09:36:12+00:00")].shape

    assert "distpos" in multi_frame.columns
    assert "speed" in multi_frame.columns
    assert before_shape[0] == after_shape[0]  # same number of records
    assert before_shape[1] + 1 == after_shape[1]  # number of columns + 1 (distpos)


def test_vertical_speed_session(multi_frame):
    before_count = multi_frame.session.count()
    before_shape = multi_frame.loc[Timestamp("2020-12-08 09:36:12+00:00")].shape

    multi_frame = multi_frame.session.vertical_speed()
    assert "vam" in multi_frame.columns
    assert before_count == multi_frame.session.count()  # same number of sessions.

    after_shape = multi_frame.loc[Timestamp("2020-12-08 09:36:12+00:00")].shape
    assert before_shape[0] == after_shape[0]  # same number of records
    assert before_shape[1] + 1 == after_shape[1]  # number of columns + 1(vam)


def test_gradient_session(multi_frame):
    before_count = multi_frame.session.count()
    before_shape = multi_frame.loc[Timestamp("2020-12-08 09:36:12+00:00")].shape

    multi_frame = multi_frame.session.gradient()
    assert "grad" in multi_frame.columns
    assert before_count == multi_frame.session.count()  # same number of sessions.

    after_shape = multi_frame.loc[Timestamp("2020-12-08 09:36:12+00:00")].shape
    assert before_shape[0] == after_shape[0]  # same number of records
    assert before_shape[1] + 1 == after_shape[1]  # number of columns + 1(grad)


def test_pace_session(multi_frame):
    before_count = multi_frame.session.count()
    before_shape = multi_frame.loc[Timestamp("2020-12-08 09:36:12+00:00")].shape

    multi_frame = multi_frame.session.pace()
    assert "pace" in multi_frame.columns
    assert before_count == multi_frame.session.count()  # same number of sessions.

    after_shape = multi_frame.loc[Timestamp("2020-12-08 09:36:12+00:00")].shape
    assert before_shape[0] == after_shape[0]  # same number of records
    assert before_shape[1] + 1 == after_shape[1]  # number of columns + 1(pace)

    multi_frame = multi_frame.session.distance()
    multi_frame = multi_frame.session.speed(from_distances=True)

    multi_frame = multi_frame.session.pace()

    after_shape = multi_frame.loc[Timestamp("2020-12-08 09:36:12+00:00")].shape

    assert "distpos" in multi_frame.columns
    assert "pace" in multi_frame.columns

    assert before_shape[0] == after_shape[0]  # same number of records
    assert (
        before_shape[1] + 2 == after_shape[1]
    )  # number of columns + 2 (distpos, pace)

    assert isinstance(multi_frame["pace"], columns.Pace)


def test_only_moving_session(multi_frame):
    before_count = multi_frame.session.count()
    before_shape = multi_frame.loc[Timestamp("2020-12-08 09:36:12+00:00")].shape

    multi_frame = multi_frame.session.only_moving()
    assert "moving" in multi_frame.columns
    assert before_count == multi_frame.session.count()  # same number of sessions.

    after_shape = multi_frame.loc[Timestamp("2020-12-08 09:36:12+00:00")].shape
    assert before_shape[0] == after_shape[0]  # same number of records
    assert before_shape[1] + 1 == after_shape[1]  # number of columns + 1(moving)


def test_heart_zone_session(multi_frame):
    before_count = multi_frame.session.count()
    before_shape = multi_frame.loc[Timestamp("2020-12-08 09:36:12+00:00")].shape

    multi_frame = multi_frame.session.heart_zone(
        bins=[0, 92, 110, 129, 147, 166, 184],
        labels=["Rest", "Z1", "Z2", "Z3", "Z4", "Z5"],
    )
    assert "hr_zone" in multi_frame.columns
    assert before_count == multi_frame.session.count()  # same number of sessions.

    after_shape = multi_frame.loc[Timestamp("2020-12-08 09:36:12+00:00")].shape
    assert before_shape[0] == after_shape[0]  # same number of records
    assert before_shape[1] + 1 == after_shape[1]  # number of columns + 1(hr_zone)
