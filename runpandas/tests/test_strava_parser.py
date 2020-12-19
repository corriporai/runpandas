"""
Test module for Strava API reader base module
"""

import os
import json
import pytest
from pandas import DataFrame, Timedelta, Timestamp
from runpandas import read_strava
from runpandas import types
from stravalib.protocol import ApiV3
from stravalib.client import Client
from stravalib.model import Stream

pytestmark = pytest.mark.stable


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


@pytest.fixture
def dirpath(datapath):
    return datapath("io", "data")


@pytest.fixture
def strava_activity(dirpath, mocker):
    activity_json = os.path.join(dirpath, "strava", "activity.json")
    streams_json = os.path.join(dirpath, "strava", "streams.json")

    mocker.patch.object(ApiV3, "get", return_value=MockResponse(activity_json).json())

    mocker.patch.object(
        Client,
        "get_activity_streams",
        return_value=mock_get_activity_streams(streams_json),
    )
    # we don't use access token here, since we will mock the stravalib json response
    activity = read_strava(
        activity_id=4437021783,
        access_token="youraccesstoken",
        refresh_token="yourrefreshtoken",
        to_df=False,
    )
    return activity


@pytest.fixture
def strava_dataframe(dirpath, mocker):
    activity_json = os.path.join(dirpath, "strava", "activity.json")
    streams_json = os.path.join(dirpath, "strava", "streams.json")

    mocker.patch.object(ApiV3, "get", return_value=MockResponse(activity_json).json())

    mocker.patch.object(
        Client,
        "get_activity_streams",
        return_value=mock_get_activity_streams(streams_json),
    )
    # we don't use access token here, since we will mock the stravalib json response
    activity = read_strava(
        activity_id=4437021783,
        access_token="youraccesstoken",
        refresh_token="yourrefreshtoken",
        to_df=True,
    )
    return activity


def test_read_strava_basic_dataframe(dirpath, mocker):
    activity_json = os.path.join(dirpath, "strava", "activity.json")
    streams_json = os.path.join(dirpath, "strava", "streams.json")

    mocker.patch.object(ApiV3, "get", return_value=MockResponse(activity_json).json())

    mocker.patch.object(
        Client,
        "get_activity_streams",
        return_value=mock_get_activity_streams(streams_json),
    )
    # we don't use access token here, since we will mock the stravalib json response
    activity = read_strava(
        activity_id=4437021783,
        access_token="youraccesstoken",
        refresh_token="yourrefreshtoken",
        to_df=True,
    )
    assert isinstance(activity, DataFrame)
    included_data = set(
        [
            "latitude",
            "longitude",
            "altitude",
            "distance",
            "velocity_smooth",
            "heartrate",
            "cadence",
            "moving",
            "grade_smooth",
        ]
    )
    assert included_data <= set(activity.columns.to_list())
    assert activity.size == 15723


def test_read_strava_activity(dirpath, mocker):
    activity_json = os.path.join(dirpath, "strava", "activity.json")
    streams_json = os.path.join(dirpath, "strava", "streams.json")

    mocker.patch.object(ApiV3, "get", return_value=MockResponse(activity_json).json())

    mocker.patch.object(
        Client,
        "get_activity_streams",
        return_value=mock_get_activity_streams(streams_json),
    )

    # we don't use access token here, since we will mock the stravalib json response
    activity = read_strava(
        activity_id=4437021783,
        access_token="youraccesstoken",
        refresh_token="yourrefreshtoken",
        to_df=False,
    )
    assert type(activity) is types.Activity
    included_data = set(
        [
            "alt",
            "cad",
            "dist",
            "hr",
            "lon",
            "lat",
            "moving",
            "velocity_smooth",
            "grade_smooth",
        ]
    )
    assert included_data <= set(activity.columns.to_list())
    assert activity.size == 15723


test_data = [
    (pytest.lazy_fixture("strava_activity"), "alt", 0, 6.4),
    (pytest.lazy_fixture("strava_activity"), "alt", -1, 6.6),
    (pytest.lazy_fixture("strava_activity"), "cad", 0, 79),
    (pytest.lazy_fixture("strava_activity"), "cad", -1, 86),
    (pytest.lazy_fixture("strava_activity"), "dist", 0, 0.0),
    (pytest.lazy_fixture("strava_activity"), "dist", -1, 12019.7),
    (pytest.lazy_fixture("strava_activity"), "hr", 0, 111),
    (pytest.lazy_fixture("strava_activity"), "hr", -1, 160),
    (pytest.lazy_fixture("strava_activity"), "lat", 0, -8.016994),
    (pytest.lazy_fixture("strava_activity"), "lon", 0, -34.847439),
    (pytest.lazy_fixture("strava_activity"), "lat", -1, -8.016821),
    (pytest.lazy_fixture("strava_activity"), "lon", -1, -34.84716),
    (pytest.lazy_fixture("strava_activity"), "moving", 0, False),
    (pytest.lazy_fixture("strava_activity"), "moving", -1, True),
    (pytest.lazy_fixture("strava_activity"), "velocity_smooth", 0, 0.0),
    (pytest.lazy_fixture("strava_activity"), "velocity_smooth", -1, 3.2),
    (pytest.lazy_fixture("strava_activity"), "grade_smooth", 0, 1.1),
    (pytest.lazy_fixture("strava_activity"), "grade_smooth", -1, -0.6),
    (pytest.lazy_fixture("strava_dataframe"), "altitude", 0, 6.4),
    (pytest.lazy_fixture("strava_dataframe"), "altitude", -1, 6.6),
    (pytest.lazy_fixture("strava_dataframe"), "cadence", 0, 79),
    (pytest.lazy_fixture("strava_dataframe"), "cadence", -1, 86),
    (pytest.lazy_fixture("strava_dataframe"), "distance", 0, 0.0),
    (pytest.lazy_fixture("strava_dataframe"), "distance", -1, 12019.7),
    (pytest.lazy_fixture("strava_dataframe"), "heartrate", 0, 111),
    (pytest.lazy_fixture("strava_dataframe"), "heartrate", -1, 160),
    (pytest.lazy_fixture("strava_dataframe"), "latitude", 0, -8.016994),
    (pytest.lazy_fixture("strava_dataframe"), "longitude", 0, -34.847439),
    (pytest.lazy_fixture("strava_dataframe"), "latitude", -1, -8.016821),
    (pytest.lazy_fixture("strava_dataframe"), "longitude", -1, -34.84716),
    (pytest.lazy_fixture("strava_dataframe"), "moving", 0, False),
    (pytest.lazy_fixture("strava_dataframe"), "moving", -1, True),
    (pytest.lazy_fixture("strava_dataframe"), "velocity_smooth", 0, 0.0),
    (pytest.lazy_fixture("strava_dataframe"), "velocity_smooth", -1, 3.2),
    (pytest.lazy_fixture("strava_dataframe"), "grade_smooth", 0, 1.1),
    (pytest.lazy_fixture("strava_dataframe"), "grade_smooth", -1, -0.6),
]


@pytest.mark.parametrize("activity,column,index,expected", test_data)
def test_strava_values(activity, column, index, expected):
    assert activity[column].iloc[index] == expected
    assert activity.index[-1] == Timedelta("0 days 01:25:45")

    if isinstance(activity, types.Activity):
        assert activity.start == Timestamp("2020-12-06 06:36:27")
