"""
Test module for runpandas acessors
"""

import os
import pytest
import pandas as pd
from runpandas import read_event as read_result

pytestmark = pytest.mark.stable


@pytest.fixture
def dirpath(datapath):
    return datapath("io", "data")


@pytest.fixture
def runpandas_race(dirpath):
    result_file = os.path.join(dirpath, "results", "valid_result_usa.csv")
    return read_result(result_file, to_df=False)


@pytest.fixture
def runpandas_10krace(dirpath):
    result_file = os.path.join(dirpath, "results", "result_10k.csv")
    return read_result(result_file, to_df=False)


@pytest.fixture
def pandas_race(dirpath):
    result_file = os.path.join(dirpath, "results", "valid_result_usa.csv")
    return read_result(result_file, to_df=True)


def test_splits_validate(runpandas_race, pandas_race, runpandas_10krace):
    # Assertion error for non race result instances
    with pytest.raises(AssertionError):
        _ = pandas_race.splits.pick_athlete("11")

    # Assertion error for wrong by argument
    with pytest.raises(AssertionError):
        _ = runpandas_race.splits.pick_athlete("11", by="NUMBER")

    # Assertion error for wrong event type
    with pytest.raises(AssertionError):
        _ = runpandas_10krace.splits.pick_athlete("11", by="BIB")


def test_splits_pick_athlete(runpandas_race):
    # Assertion error for wrong by argument
    with pytest.raises(ValueError):
        _ = runpandas_race.splits.pick_athlete("ABC", by="BIB")

    with pytest.raises(ValueError):
        _ = runpandas_race.splits.pick_athlete("23344444", by="POS")

    # Test split data
    splits_data = runpandas_race.splits.pick_athlete("11", by="BIB")

    included_data = set(["time", "distance_meters", "distance_miles"])
    assert included_data == set(splits_data.columns.to_list())

    included_data = set(
        ["0k", "5k", "10k", "15k", "20k", "half", "25k", "30k", "35k", "40k", "nettime"]
    )
    assert included_data == set(splits_data.index.to_list())

    assert splits_data["distance_meters"].iloc[0] == 0
    assert splits_data["distance_miles"].iloc[0] == 0
    assert splits_data["distance_meters"].iloc[-1] == 42195
    assert splits_data["distance_miles"].iloc[-1] == pytest.approx(26.2187, 0.1)

    assert splits_data["time"].iloc[0].total_seconds() == 0
    assert splits_data["time"].iloc[-1].total_seconds() == pytest.approx(
        pd.Timedelta("02:09:37").total_seconds(), rel=0.001
    )
    assert splits_data.shape[0] == 11  # number of lines
