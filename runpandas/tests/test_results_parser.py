"""
Test module for Race Results reader base module
"""

import datetime
import os

import pandas as pd
import pytest
from pandas.testing import assert_series_equal
from runpandas import exceptions
from runpandas.io.result._parser import __extract_metadata
from runpandas import read_event as read_result
from runpandas.types.frame import RaceResult, Event

pytestmark = pytest.mark.stable


@pytest.fixture
def dirpath(datapath):
    return datapath("io", "data")


@pytest.fixture
def pandas_race(dirpath):
    result_file = os.path.join(dirpath, "results", "valid_result_usa.csv")
    return read_result(result_file, to_df=True)


@pytest.fixture
def runpandas_race(dirpath):
    result_file = os.path.join(dirpath, "results", "valid_result_usa.csv")
    return read_result(result_file, to_df=False)


def test_extract_valid_metadata(dirpath):
    result_file = os.path.join(dirpath, "results", "valid_result.csv")
    header = __extract_metadata(result_file)
    assert "Lochness marathon" in header["name"]
    assert datetime.datetime(2003, 10, 4) == header["race_date"]
    assert "42k" in header["run_type"]
    assert "UK" in header["country"]
    assert len(header) == 4


def test_extract_invalid_metadata(dirpath):
    result_file = os.path.join(dirpath, "results", "invalid_result.csv")
    with pytest.raises(exceptions.InvalidHeaderError):
        _ = __extract_metadata(result_file)


def test_extract_missing_header_metadata(dirpath):
    result_file = os.path.join(dirpath, "results", "missing_result2.csv")
    with pytest.raises(exceptions.MissingHeaderError):
        _ = __extract_metadata(result_file)


def test_extract_missing_full_header_metadata(dirpath):
    result_file = os.path.join(dirpath, "results", "missing_result.csv")
    with pytest.raises(exceptions.InvalidHeaderError):
        _ = __extract_metadata(result_file)


def test_extract_empty_full_header_metadata(dirpath):
    result_file = os.path.join(dirpath, "results", "empty_result.csv")
    with pytest.raises(pd.errors.EmptyDataError):
        _ = __extract_metadata(result_file)


def test_read_file_result_basic_dataframe(dirpath):
    result_file = os.path.join(dirpath, "results", "valid_result_usa.csv")
    race = read_result(result_file, to_df=True)
    assert isinstance(race, pd.DataFrame)
    assert race.size == 660250
    included_data = set(
        [
            "position",
            "bib",
            "name",
            "age",
            "sex",
            "city",
            "state",
            "country",
            "citizen",
            "unnamed:9",
            "5k",
            "10k",
            "15k",
            "half",
            "25k",
            "30k",
            "35k",
            "40k",
            "pace",
            "proj_time",
            "nettime",
            "overall",
            "gender",
            "division",
        ]
    )
    assert included_data <= set(race.columns.to_list())

    result_file = os.path.join(dirpath, "results", "valid_result_br.csv")
    race = read_result(result_file, to_df=True)
    assert isinstance(race, pd.DataFrame)
    assert race.size == 31670
    included_data = set(
        [
            "position",
            "bib",
            "name",
            "sex",
            "age",
            "faixa",
            "cl._fx.",
            "equipe",
            "grosstime",
            "nettime",
        ]
    )
    assert included_data <= set(race.columns.to_list())


def test_read_file_result_valid_race_result(dirpath):
    result_file = os.path.join(dirpath, "results", "valid_result_usa.csv")
    race = read_result(result_file, to_df=False)
    assert isinstance(race, RaceResult)
    assert isinstance(race.event, Event)
    assert race.event.event_country == "USA"
    assert race.event.event_name == "boston marathon"
    assert race.event.event_type == "42k"
    assert race.event.event_date == datetime.datetime(2017, 4, 17)
    assert race.shape[0] == 26410  # number of lines
    included_data = set(
        [
            "position",
            "bib",
            "name",
            "age",
            "sex",
            "city",
            "state",
            "country",
            "citizen",
            "unnamed:9",
            "5k",
            "10k",
            "15k",
            "half",
            "25k",
            "30k",
            "35k",
            "40k",
            "pace",
            "proj_time",
            "nettime",
            "overall",
            "gender",
            "division",
        ]
    )
    assert included_data <= set(race.columns.to_list())
    assert (race.position.values == "DNF").sum() == 0  # number of non-finishers

    result_file = os.path.join(dirpath, "results", "valid_result_br.csv")
    race = read_result(result_file, to_df=False)
    assert isinstance(race, RaceResult)
    assert isinstance(race.event, Event)
    assert race.event.event_country == "BR"
    assert race.event.event_name == "Porto Alegre Marathon"
    assert race.event.event_type == "42k"
    assert race.event.event_date == datetime.datetime(2019, 6, 2)
    assert race.shape[0] == 3167  # number of lines
    included_data = set(
        [
            "position",
            "bib",
            "name",
            "sex",
            "age",
            "faixa",
            "cl._fx.",
            "equipe",
            "grosstime",
            "nettime",
        ]
    )
    assert included_data <= set(race.columns.to_list())
    assert (race.position.values == "DNF").sum() == 0  # number of non-finishers


def test_read_file_result_valid_race_result_with_nonfinishers(dirpath):
    result_file = os.path.join(dirpath, "results", "result_with_nonfinishers.csv")
    race = read_result(result_file, to_df=False)
    assert isinstance(race, RaceResult)
    assert isinstance(race.event, Event)
    assert race.event.event_country == "UK"
    assert race.event.event_name == "lochness marathon"
    assert race.event.event_type == "42k"
    assert race.event.event_date == datetime.datetime(2018, 9, 23)
    assert race.shape[0] == 2825  # number of lines

    assert (race.position.values == "DNF").sum() == 15  # number of non-finishers


test_data = [
    (
        pytest.lazy_fixture("pandas_race"),
        "position",
        0,
        "0",
    ),
    (
        pytest.lazy_fixture("pandas_race"),
        "position",
        -1,
        "26409",
    ),
    (
        pytest.lazy_fixture("pandas_race"),
        "age",
        0,
        24,
    ),
    (
        pytest.lazy_fixture("pandas_race"),
        "age",
        -1,
        48,
    ),
    (
        pytest.lazy_fixture("pandas_race"),
        "nettime",
        0,
        pd.Timedelta("0 days 02:09:37"),
    ),
    (
        pytest.lazy_fixture("pandas_race"),
        "sex",
        0,
        "M",
    ),
    (
        pytest.lazy_fixture("pandas_race"),
        "bib",
        -1,
        "25266",
    ),
    (
        pytest.lazy_fixture("pandas_race"),
        "bib",
        0,
        "11",
    ),
    (
        pytest.lazy_fixture("runpandas_race"),
        "position",
        0,
        "0",
    ),
    (
        pytest.lazy_fixture("runpandas_race"),
        "position",
        -1,
        "26409",
    ),
    (
        pytest.lazy_fixture("runpandas_race"),
        "age",
        0,
        24,
    ),
    (
        pytest.lazy_fixture("runpandas_race"),
        "age",
        -1,
        48,
    ),
    (
        pytest.lazy_fixture("runpandas_race"),
        "nettime",
        0,
        pd.Timedelta("0 days 02:09:37"),
    ),
    (
        pytest.lazy_fixture("runpandas_race"),
        "sex",
        0,
        "M",
    ),
    (
        pytest.lazy_fixture("runpandas_race"),
        "nettime",
        -1,
        pd.Timedelta("0 days 07:58:14"),
    ),
    (
        pytest.lazy_fixture("runpandas_race"),
        "half",
        0,
        pd.Timedelta("0 days 01:04:35"),
    ),
]


@pytest.mark.parametrize("race,column,index,expected", test_data)
def test_race_result_values(race, column, index, expected):
    assert race[column].iloc[index] == expected


def test_properties_result_valid_race_result_with_nonfinishers(dirpath):
    result_file = os.path.join(dirpath, "results", "result_with_nonfinishers.csv")
    race = read_result(result_file, to_df=False)

    assert race.total_participants == 2825
    assert race.total_finishers == 2810
    assert race.total_nonfinishers == 15
    assert len(race.participants) == 2825
    assert isinstance(race.participants, list)
    assert isinstance(race.winner, pd.Series)

    expected = pd.Series(
        [
            "1",
            "1",
            "Mohammad",
            "Aburezeq",
            pd.Timedelta("0 days 01:09:21"),
            pd.Timedelta("0 days 02:22:56"),
            pd.Timedelta("0 days 02:22:56"),
            "Mara-MS",
        ],
        index=[
            "position",
            "bib",
            "firstname",
            "lastname",
            "half",
            "grosstime",
            "nettime",
            "category",
        ],
        name=0,
    )
    assert_series_equal(race.winner, expected)
