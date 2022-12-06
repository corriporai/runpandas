"""
Test module for utilities from the datasets package
"""

import os
import shutil
import pytest
from runpandas.datasets.utils import (
    _get_config_data,
    _get_cache_path,
    _get_activity_index,
    activity_examples,
    _get_event_index,
    get_events,
)
from runpandas.datasets.schema import (
    ActivityData,
    FileTypeEnum,
    RunTypeEnum,
    RaceData,
    EventData,
)
from runpandas import read_file
from runpandas import read_event as read_result
from runpandas.types import Activity
from runpandas.types.frame import RaceResult

pytestmark = pytest.mark.stable


@pytest.fixture
def dirpath(datapath):
    return datapath("datasets")


def test_config_data(dirpath):
    # test default config data
    config = _get_config_data()
    assert "runpandas_data" in config["path"]["root"]

    # test custom config data
    test_config_file = os.path.join(dirpath, "config.test.yaml")

    config = _get_config_data(test_config_file)
    assert "test_runpandas_data" in config["path"]["root"]


def test_get_cache_path(dirpath):
    # first create
    test_config_file = os.path.join(dirpath, "config.test.yaml")
    directory = _get_cache_path(test_config_file)
    assert os.path.exists(directory)

    # test after created
    directory = _get_cache_path(test_config_file)
    assert os.path.exists(directory)
    shutil.rmtree(directory)


def test_get_activity_index():
    index = _get_activity_index()
    assert len(index) > 0
    assert type(index[0]) is ActivityData
    assert "polarm400.tcx" in [os.path.basename(item.path) for item in index]


def test_activity_examples(dirpath):
    # test filtered activities examples
    tcx_examples = activity_examples(file_type=FileTypeEnum.TCX)
    assert "polarm400.tcx" in [os.path.basename(item.path) for item in tcx_examples]

    # test empty actitivies examples
    empty_examples = activity_examples(file_type="PWX")
    assert len(list(empty_examples)) == 0

    # test not found file
    with pytest.raises(ValueError):
        _ = activity_examples(path="test.tcx")

    # test not cached file
    test_config_file = os.path.join(dirpath, "config.test.yaml")
    example_activity = activity_examples(path="polarm400.tcx", config=test_config_file)
    assert "polarm400.tcx" in example_activity.path
    assert os.path.exists(example_activity.path)
    assert type(read_file(example_activity.path)) is Activity

    # test cached file
    example_activity = activity_examples(path="polarm400.tcx", config=test_config_file)
    assert "polarm400.tcx" in os.path.basename(example_activity.path)
    assert os.path.exists(example_activity.path)
    assert type(read_file(example_activity.path)) is Activity

    # test fit file
    example_activity = activity_examples(
        path="Garmin_Fenix_6S_Pro-Running.fit", config=test_config_file
    )
    assert "Garmin_Fenix_6S_Pro-Running.fit" in os.path.basename(example_activity.path)
    assert os.path.exists(example_activity.path)
    assert type(read_file(example_activity.path)) is Activity

    directory = _get_cache_path(test_config_file)
    shutil.rmtree(directory)


def test_get_get_event_index():
    index = _get_event_index()
    assert len(index) > 0
    assert type(index[0]) is RaceData
    assert "lochness_marathon" in [os.path.basename(item.path) for item in index]


def test_load_race_data():
    race_events = get_events(identifier="lochness_marathon", year=2021)
    result_set = list(race_events)
    assert type(result_set[0].load()) is RaceResult


def test_get_events(dirpath):
    # test match events
    race_events = get_events(identifier="lochness_marathon")
    basename_events = [os.path.basename(item.path) for item in race_events]
    for yr in [
        "2003",
        "2004",
        "2005",
        "2006",
        "2007",
        "2008",
        "2009",
        "2010",
        "2011",
        "2012",
        "2013",
        "2014",
        "2015",
        "2016",
        "2017",
        "2018",
        "2019",
        "2021",
        "2022",
    ]:
        assert "lochness_marathon_%s.csv" % yr in basename_events

    assert len(race_events) == 19
    assert all(isinstance(race, EventData) for race in race_events)

    # test empty match events
    empty_events = get_events(identifier="boston marathon")
    assert len(list(empty_events)) == 0

    # test empty match events
    empty_events = get_events(identifier="abc")
    assert len(list(empty_events)) == 0

    # test fuzzy match events (single word)
    fuzzy_events = get_events(identifier="lochness")
    basename_events = [os.path.basename(item.path) for item in fuzzy_events]
    for yr in [
        "2003",
        "2004",
        "2005",
        "2006",
        "2007",
        "2008",
        "2009",
        "2010",
        "2011",
        "2012",
        "2013",
        "2014",
        "2015",
        "2016",
        "2017",
        "2018",
        "2019",
        "2021",
        "2022",
    ]:
        assert "lochness_marathon_%s.csv" % yr in basename_events

    assert len(race_events) == 19
    assert all(isinstance(race, EventData) for race in fuzzy_events)

    # test fuzzy match events (compound word)
    fuzzy_events = get_events(identifier="lochness uk")
    basename_events = [os.path.basename(item.path) for item in fuzzy_events]
    for yr in [
        "2003",
        "2004",
        "2005",
        "2006",
        "2007",
        "2008",
        "2009",
        "2010",
        "2011",
        "2012",
        "2013",
        "2014",
        "2015",
        "2016",
        "2017",
        "2018",
        "2019",
        "2021",
        "2022",
    ]:
        assert "lochness_marathon_%s.csv" % yr in basename_events

    assert len(fuzzy_events) == 19
    assert all(isinstance(race, EventData) for race in fuzzy_events)

    # test not cached event
    test_config_file = os.path.join(dirpath, "config.test.yaml")
    race_events = get_events(identifier="lochness_marathon", config=test_config_file)
    basename_events = [os.path.basename(item.path) for item in race_events]
    for yr in [
        "2003",
        "2004",
        "2005",
        "2006",
        "2007",
        "2008",
        "2009",
        "2010",
        "2011",
        "2012",
        "2013",
        "2014",
        "2015",
        "2016",
        "2017",
        "2018",
        "2019",
        "2021",
        "2022",
    ]:
        assert "lochness_marathon_%s.csv" % yr in basename_events
    for race in race_events:
        assert os.path.exists(race.path)
        assert type(read_result(race.path)) is RaceResult
        assert (
            "<Event: name=UK Lochness Marathon Results from 2022 to 2003."
            in race.__repr__()
        )
    # test cached event
    race_events = get_events(identifier="lochness_marathon", config=test_config_file)
    basename_events = [os.path.basename(item.path) for item in race_events]
    for yr in [
        "2003",
        "2004",
        "2005",
        "2006",
        "2007",
        "2008",
        "2009",
        "2010",
        "2011",
        "2012",
        "2013",
        "2014",
        "2015",
        "2016",
        "2017",
        "2018",
        "2019",
        "2021",
        "2022",
    ]:
        assert "lochness_marathon_%s.csv" % yr in basename_events
    for race in race_events:
        assert os.path.exists(race.path)
        assert type(read_result(race.path)) is RaceResult
        assert (
            "<Event: name=UK Lochness Marathon Results from 2022 to 2003."
            in race.__repr__()
        )

    # test filtered events with year
    filtered_events = get_events(
        identifier="lochness_marathon", config=test_config_file, year="2019"
    )
    result_set = list(filtered_events)
    assert len(result_set) == 1
    assert "lochness_marathon_2019.csv" in os.path.basename(result_set[0].path)
    assert os.path.exists(result_set[0].path)
    assert type(read_result(result_set[0].path)) is RaceResult
    assert (
        "<Event: name=UK Lochness Marathon Results from 2022 to 2003.,"
        + " country=UK, edition=2019>"
        in result_set[0].__repr__()
    )

    # test filtered events with race_type
    filtered_events = get_events(
        identifier="lochness_marathon",
        config=test_config_file,
        run_type=RunTypeEnum.HALF_MARATHON,
    )
    result_set = list(filtered_events)
    assert len(result_set) == 0

    filtered_events = get_events(
        identifier="lochness_marathon",
        config=test_config_file,
        run_type=RunTypeEnum.MARATHON,
    )
    result_set = list(filtered_events)
    assert len(result_set) == 19
    basename_events = [os.path.basename(item.path) for item in result_set]
    for yr in [
        "2003",
        "2004",
        "2005",
        "2006",
        "2007",
        "2008",
        "2009",
        "2010",
        "2011",
        "2012",
        "2013",
        "2014",
        "2015",
        "2016",
        "2017",
        "2018",
        "2019",
        "2021",
        "2022",
    ]:
        assert "lochness_marathon_%s.csv" % yr in basename_events

    directory = _get_cache_path(test_config_file)
    shutil.rmtree(directory)
