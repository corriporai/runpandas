"""
Test module for Strava Client Authentication module
"""
import os
import json
import pytest
from unittest.mock import PropertyMock
from runpandas.io.strava._client import StravaClient, HTTPResponder


@pytest.fixture
def dirpath(datapath):
    return datapath("io", "data")


@pytest.fixture(scope="session")
def valid_token_file(tmpdir_factory):
    return tmpdir_factory.getbasetemp().join("token.json")


def test_stravaclient_with_enviroment_variables(dirpath):
    os.environ["STRAVA_CLIENT_SECRET"] = str("STRAVA_CLIENT_SECRET")
    os.environ["STRAVA_CLIENT_ID"] = str("STRAVA_ID")
    refresh_token = "REFRESHTOKEN"
    client = StravaClient(refresh_token=refresh_token)

    assert client.client_secret == "STRAVA_CLIENT_SECRET"
    assert client.client_id == "STRAVA_ID"
    assert client.token_file is None


def test_stravaclient_with_arguments(dirpath):
    os.environ["STRAVA_CLIENT_SECRET"] = str("STRAVA_CLIENT_SECRET")
    os.environ["STRAVA_CLIENT_ID"] = str("STRAVA_ID")
    refresh_token = "REFRESHTOKEN"
    client = StravaClient(
        refresh_token=refresh_token,
        client_id="STRAVA_ID",
        client_secret="STRAVA_CLIENT_SECRET",
    )

    assert client.client_secret == "STRAVA_CLIENT_SECRET"
    assert client.client_id == "STRAVA_ID"
    assert client.token_file is None

    # if token file is empty, so it can't write on it.
    assert client.save_token_to_file({"test": "test"}) is None


def test_stravaclient_rw_token_file(dirpath, valid_token_file):
    # create a token valid file
    file_handler = open(valid_token_file, "w")
    file_handler.write(
        '{"access_token": "2334444",  "refresh_token": "235555", \
             "expires_at": 1658341120.318284}'
    )
    file_handler.close()

    client = StravaClient(
        client_id="STRAVA_ID",
        client_secret="STRAVA_CLIENT_SECRET",
        token_file=valid_token_file,
    )

    assert client.access_token == "2334444"
    assert client.refresh_token == "235555"
    assert client.token_expires_at == 1658341120.318284

    assert client.client_secret == "STRAVA_CLIENT_SECRET"
    assert client.client_id == "STRAVA_ID"

    token = {
        "access_token": "222",
        "refresh_token": "111",
        "expires_at": 1658341120.318284,
    }
    client.save_token_to_file(token)
    with open(valid_token_file) as f:
        assert json.loads(f.read()) == json.loads(
            '{"access_token": "222",  "refresh_token": "111", "expires_at": 1658341120.318284}'
        )


def test_stravaclient_authenticate(dirpath, valid_token_file, mocker):
    mocker.patch("webbrowser.open")
    mocker.patch.object(HTTPResponder, "handle_request", return_value=None)
    mocker.patch.object(
        StravaClient,
        "exchange_code_for_token",
        return_value={
            "access_token": "1",
            "refresh_token": "1",
            "expires_at": 1658450893,
        },
    )
    mocker.patch.object(
        HTTPResponder, "access_token", new_callable=PropertyMock, return_value="123"
    )

    os.environ["STRAVA_CLIENT_SECRET"] = str("STRAVA_CLIENT_SECRET")
    os.environ["STRAVA_CLIENT_ID"] = str("STRAVA_ID")
    refresh_token = "REFRESHTOKEN"
    client = StravaClient(
        refresh_token=refresh_token,
        client_id="STRAVA_ID",
        client_secret="STRAVA_CLIENT_SECRET",
        token_file=valid_token_file,
    )
    client.authenticate_web()
    with open(valid_token_file) as f:
        returned = json.load(f)
        assert returned["access_token"] == "1"
        assert returned["refresh_token"] == "1"
        assert returned["expires_at"] == 1658450893
