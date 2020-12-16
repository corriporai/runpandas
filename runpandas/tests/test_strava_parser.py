"""
Test module for Strava API reader base module
"""

import os
import json
import pytest
import mock
from pandas import DataFrame, Timedelta, Timestamp
from runpandas import read_strava
from runpandas import types
from stravalib.protocol import ApiV3
from stravalib.client import Client
from stravalib.model import Stream

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
    stream_mock  = MockResponse(streams_file).json()
    entities = {}
    for key, value in stream_mock.items():
        value['type'] =  key
        stream = Stream.deserialize(value)
        entities[stream.type] = stream
    return entities

def test_read_strava_basic_dataframe(dirpath, mocker):
    activity_json = os.path.join(dirpath, "strava", "activity.json")
    streams_json = os.path.join(dirpath, "strava", "streams.json")

    mocker.patch.object(ApiV3, 'get',
    return_value=MockResponse(activity_json).json())

    mocker.patch.object(Client, 'get_activity_streams',
        return_value=mock_get_activity_streams(streams_json))

    activity = read_strava(activity_id=4437021783,
                    access_token='c31f55d5f2f37ed3ba65a2ecb721123d9cb817ee',
                    refresh_token='59c8537628a19d70330e5aca2ec5a558023a2c03',
                    to_df=True)
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
            "grade_smooth"
        ]
    )
    assert included_data <= set(activity.columns.to_list())
    assert activity.size == 15723

'''
def test_read_strava_activity(dirpath, mocker):
    activity = read_strava(activity_id=4437021783,
                    access_token='c31f55d5f2f37ed3ba65a2ecb721123d9cb817ee',
                    refresh_token='59c8537628a19d70330e5aca2ec5a558023a2c03',
                    to_df=False)
    assert type(activity) is types.Activity
    included_data = set(["alt", "cad", "dist", "hr", "lon", 'lat', 'moving', 'velocity_smooth', 'grade_smooth'])
    assert included_data <= set(activity.columns.to_list())
    assert activity.size == 15723
'''
