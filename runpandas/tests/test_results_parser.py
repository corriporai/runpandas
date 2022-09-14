"""
Test module for Race Results reader base module
"""

import datetime
import os

import pandas as pd
import pytest
from pandas.core.frame import DataFrame
from runpandas import exceptions, types
from runpandas.io.result._parser import __extract_metadata
from runpandas.io.result._parser import read as read_result
from runpandas.types.frame import RaceResult, Event

pytestmark = pytest.mark.stable


@pytest.fixture
def dirpath(datapath):
    return datapath("io", "data")


def pandas_activity(dirpath):
    result_file = os.path.join(dirpath, "results", "valid_result_usa.csv")
    return read_result(result_file, to_df=True)


@pytest.mark.results
def test_extract_valid_metadata(dirpath):
    result_file = os.path.join(dirpath, "results", "valid_result.csv")
    header = __extract_metadata(result_file)
    assert 'lochness marathon' in header['name']
    assert datetime.datetime(2003,4, 10) == header['race_date']
    assert '42k' in header['run_type']
    assert 'UK' in header['country']
    assert len(header) == 4

@pytest.mark.results
def test_extract_invalid_metadata(dirpath):
    result_file = os.path.join(dirpath, "results", "invalid_result.csv")
    with pytest.raises(exceptions.InvalidHeaderError):
        header = __extract_metadata(result_file)

@pytest.mark.results
def test_extract_missing_header_metadata(dirpath):
    result_file = os.path.join(dirpath, "results", "missing_result2.csv")
    with pytest.raises(exceptions.MissingHeaderError):
        header = __extract_metadata(result_file)

@pytest.mark.results
def test_extract_missing_full_header_metadata(dirpath):
    result_file = os.path.join(dirpath, "results", "missing_result.csv")
    with pytest.raises(exceptions.InvalidHeaderError):
        header = __extract_metadata(result_file)

@pytest.mark.results
def test_extract_missing_full_header_metadata(dirpath):
    result_file = os.path.join(dirpath, "results", "empty_result.csv")
    with pytest.raises(pd.errors.EmptyDataError):
        header = __extract_metadata(result_file)

@pytest.mark.results
def test_read_file_result_basic_dataframe(dirpath):
    result_file = os.path.join(dirpath, "results", "valid_result_usa.csv")
    race = read_result(result_file, to_df=True)
    assert isinstance(race, pd.DataFrame)
    assert race.size == 660250
    included_data = set(["position", "bib", "name", "age", "sex", "city", "state", "country", "citizen", "unnamed:9", "5k", "10k", "15k", "half", "25k", "30k", "35k", "40k", "pace", "proj_time", "nettime", "overall", "gender", "division"])
    assert included_data <= set(race.columns.to_list())

    result_file = os.path.join(dirpath, "results", "valid_result_br.csv")
    race = read_result(result_file, to_df=True)
    assert isinstance(race, pd.DataFrame)
    assert race.size == 31670
    included_data = set(["position", "bib", "name", "sex", "age", "faixa", "cl._fx.", "equipe", "grosstime", "nettime"])
    assert included_data <= set(race.columns.to_list())


@pytest.mark.results
def test_read_file_result_valid_race_result(dirpath):
    result_file = os.path.join(dirpath, "results", "valid_result_usa.csv")
    race = read_result(result_file, to_df=False)
    assert isinstance(race, RaceResult)
    assert isinstance(race.event, Event)
    assert race.event.event_country == 'USA'
    assert race.event.event_name == 'boston marathon'
    assert race.event.event_type == '42k'
    assert race.event.event_date == datetime.datetime(2017, 4, 17)
    assert race.shape[0] == 26410  ##number of lines

    included_data = set(["position", "bib", "name", "age", "sex", "city", "state", "country", "citizen", "unnamed:9", "5k", "10k", "15k", "half", "25k", "30k", "35k", "40k", "pace", "proj_time", "nettime", "overall", "gender", "division"])
    assert included_data <= set(race.columns.to_list())

    result_file = os.path.join(dirpath, "results", "valid_result_br.csv")
    race = read_result(result_file, to_df=False)
    assert isinstance(race, RaceResult)
    assert isinstance(race.event, Event)
    assert race.event.event_country == 'BR'
    assert race.event.event_name == 'Porto Alegre Marathon'
    assert race.event.event_type == '42k'
    assert race.event.event_date == datetime.datetime(2019, 6, 2)
    assert race.shape[0] == 3167  ##number of lines
    included_data = set(["position", "bib", "name", "sex", "age", "faixa", "cl._fx.", "equipe", "grosstime", "nettime"])
    assert included_data <= set(race.columns.to_list())