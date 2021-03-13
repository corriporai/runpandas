"""
Test module for runpandas acessors
"""

import os
import json
import pytest
from pandas import Timedelta
from stravalib.protocol import ApiV3
from stravalib.client import Client
from stravalib.model import Stream
from runpandas import reader
from runpandas import read_strava

pytestmark = pytest.mark.stable


@pytest.fixture
def dirpath(datapath):
    return datapath("io", "data")


class MockResponse:
    def __init__(self, json_file):
        with open(json_file) as json_handler:
            self.json_data = json.load(json_handler)

    def json(self):
        return self.json_data


def mock_get_activity_streams(streams_file):
    """
    @TODO: I needed to mock the behavior the `stravalib.client.get_activity_streams`,
    it isn't the best alternative for mock the request from strava by passing a json file.
    """

    stream_mock = MockResponse(streams_file).json()
    entities = {}
    for key, value in stream_mock.items():
        value["type"] = key
        stream = Stream.deserialize(value)
        entities[stream.type] = stream
    return entities


def test_metrics_validate(dirpath):
    gpx_file = os.path.join(dirpath, "gpx", "stopped_example.gpx")
    activity_gpx = reader._read_file(gpx_file, to_df=True)

    # copy of dataframe for testing the index error
    frame_without_index = activity_gpx.copy()
    frame_without_index = frame_without_index.reset_index()
    with pytest.raises(AttributeError):
        frame_without_index.only_moving()

    # dataframe without speed column
    with pytest.raises(AttributeError):
        activity_gpx.only_moving()

    tcx_file = os.path.join(dirpath, "tcx", "stopped_example.tcx")
    activity_tcx = reader._read_file(tcx_file, to_df=True)

    # copy of dataframe for testing the index error
    frame_without_index = activity_tcx.copy()
    frame_without_index = frame_without_index.reset_index()
    with pytest.raises(AttributeError):
        frame_without_index.only_moving()


def test_only_moving_acessor(dirpath, mocker):
    gpx_file = os.path.join(dirpath, "gpx", "stopped_example.gpx")
    frame_gpx = reader._read_file(gpx_file, to_df=False)
    frame_gpx["distpos"] = frame_gpx.compute.distance(correct_distance=False)
    frame_gpx["speed"] = frame_gpx.compute.speed(from_distances=True)
    frame_gpx_only_moving = frame_gpx.only_moving()
    assert frame_gpx_only_moving[~frame_gpx_only_moving["moving"]].shape[0] == 74
    assert frame_gpx_only_moving.ellapsed_time == Timedelta("0 days 01:25:27")
    assert frame_gpx_only_moving.moving_time == Timedelta("0 days 01:14:46")

    tcx_file = os.path.join(dirpath, "tcx", "stopped_example.tcx")
    activity_tcx = reader._read_file(tcx_file, to_df=False)
    frame_tcx_only_moving = activity_tcx.only_moving()
    assert frame_tcx_only_moving[~frame_gpx_only_moving.moving].shape[0] == 74
    assert frame_tcx_only_moving.ellapsed_time == Timedelta("0 days 01:25:27")
    assert frame_tcx_only_moving.moving_time == Timedelta("0 days 01:23:57")

    fit_file = os.path.join(dirpath, "fit", "garmin-fenix-5-basic.fit")
    fit_file = reader._read_file(fit_file, to_df=False)
    frame_fit_only_moving = fit_file.only_moving()
    assert frame_fit_only_moving.ellapsed_time == Timedelta("0 days 00:00:57")
    assert frame_fit_only_moving.moving_time == Timedelta("0 days 00:00:55")

    tcx_file2 = os.path.join(dirpath, "tcx", "basic.tcx")
    frame_tcx_basic = reader._read_file(tcx_file2, to_df=False)
    frame_tcx_basic["distpos"] = frame_tcx_basic.compute.distance(
        correct_distance=False
    )
    frame_tcx_basic["speed"] = frame_tcx_basic.compute.speed(from_distances=True)
    frame_tcx2_only_moving = frame_tcx_basic.only_moving()
    assert frame_tcx2_only_moving.ellapsed_time == Timedelta("0 days 00:33:11")
    assert frame_tcx2_only_moving.moving_time == Timedelta("0 days 00:33:05")

    activity_json = os.path.join(dirpath, "strava", "activity.json")
    streams_json = os.path.join(dirpath, "strava", "streams.json")

    mocker.patch.object(ApiV3, "get", return_value=MockResponse(activity_json).json())

    mocker.patch.object(
        Client,
        "get_activity_streams",
        return_value=mock_get_activity_streams(streams_json),
    )

    # we don't use access token here, since we will mock the stravalib json response
    activity_strava = read_strava(
        activity_id=4437021783,
        access_token=None,
        refresh_token=None,
        to_df=False,
    )

    assert activity_strava.ellapsed_time == Timedelta("0 days 01:25:45")
    assert activity_strava.moving_time == Timedelta("0 days 01:19:41")
