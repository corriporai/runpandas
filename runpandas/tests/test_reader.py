"""
Test module for reader base module
"""

import os
import pytest
import runpandas
from pandas import DataFrame
from runpandas import reader
from runpandas import exceptions
from runpandas import types

pytestmark = pytest.mark.stable


@pytest.fixture(scope="session")
def invalid_tcx_filename(tmpdir_factory):
    return tmpdir_factory.getbasetemp().join("activity.pwx")


@pytest.fixture(scope="session")
def invalid_result_filename(tmpdir_factory):
    return tmpdir_factory.getbasetemp().join("result.doc")


@pytest.fixture(scope="session")
def temp_dir(tmpdir_factory):
    return tmpdir_factory.mktemp("data")


@pytest.fixture(scope="session")
def valid_tcx_filename(tmpdir_factory):
    return tmpdir_factory.getbasetemp().join("activity.tcx")


@pytest.fixture(scope="session")
def valid_result_filename(tmpdir_factory):
    return tmpdir_factory.getbasetemp().join("result.csv")


@pytest.fixture
def dirpath(datapath):
    return datapath("io", "data")


def test_import_module_exists():
    assert reader._import_module("tcx")


def test_top_level_import():
    assert runpandas.read_file == reader._read_file


def test_imort_module_not_exists():
    with pytest.raises(ImportError):
        reader._import_module("json")


def test_read_file_invalid(invalid_tcx_filename):
    invalid_tcx_filename.write("content")
    with pytest.raises(exceptions.InvalidFileError):
        reader._read_file(invalid_tcx_filename)


def test_read_file_not_exists(valid_tcx_filename):
    with pytest.raises(IOError):
        reader._read_file(valid_tcx_filename)


def test_read_file_malformed_tcx(dirpath):
    tcx_file = os.path.join(dirpath, "tcx", "malformed.tcx")
    with pytest.raises(exceptions.InvalidFileError):
        reader._read_file(tcx_file)


def test_read_file_tcx_basic_dataframe(dirpath):
    tcx_file = os.path.join(dirpath, "tcx", "basic.tcx")
    activity = reader._read_file(tcx_file, to_df=True)
    assert isinstance(activity, DataFrame)
    included_data = set(
        [
            "latitude_degrees",
            "longitude_degrees",
            "altitude_meters",
            "distance_meters",
            "heart_rate_bpm",
        ]
    )
    assert included_data <= set(activity.columns.to_list())
    assert activity.size == 1915


def test_read_file_tcx_basic_activity(dirpath):
    tcx_file = os.path.join(dirpath, "tcx", "basic.tcx")
    activity = reader._read_file(tcx_file, to_df=False)
    assert isinstance(activity, types.Activity)
    included_data = set(["lat", "lon", "alt", "dist", "hr"])
    assert included_data <= set(activity.columns.to_list())
    assert activity.size == 1915


def test_measured_series_activity(dirpath):
    tcx_file = os.path.join(dirpath, "tcx", "basic.tcx")
    activity = reader._read_file(tcx_file, to_df=False)
    assert isinstance(activity, types.Activity)
    assert isinstance(activity.hr, types.columns.HeartRate)
    assert activity.hr.base_unit == "bpm"
    assert activity.hr.colname == "hr"


def test_read_full_dir(dirpath):
    activities_directory = os.path.join(dirpath, "samples")
    ac_iterator = reader._read_dir(activities_directory, False)
    activities = [ac for ac in ac_iterator]
    assert len(activities) == 8
    assert isinstance(activities[0], types.Activity)
    size_data = set([16289, 12229, 6286, 5656, 6489, 5635, 9485, 9471])
    assert size_data == set([ac.size for ac in activities])


def test_empty_read_dir(temp_dir):
    activities = reader._read_dir(temp_dir)
    assert len([ac for ac in activities]) == 0


def test_invalid_dir(dirpath):
    tcx_file = os.path.join(dirpath, "tcx", "basic.tcx")
    with pytest.raises(AssertionError):
        next(reader._read_dir(tcx_file))


def test_read_dir_empty_aggregate(temp_dir):
    session_frame = reader._read_dir_aggregate(temp_dir)
    assert session_frame is None


def test_read_dir_aggregate(dirpath):
    activities_directory = os.path.join(dirpath, "samples")
    session = reader._read_dir_aggregate(activities_directory)
    assert session.session.count() == 8
    assert isinstance(session, types.Activity)
    size_data = set([16289, 12229, 6286, 5656, 6489, 5635, 9485, 9471])
    assert size_data == set(
        [
            session.xs(index, level=0).size
            for index in session.index.unique(level="start")
        ]
    )


def test_read_event_result_invalid(invalid_result_filename):
    invalid_result_filename.write("content")
    with pytest.raises(exceptions.InvalidFileError):
        reader._read_event_result(invalid_result_filename)


def test_read_event_result_not_exists(valid_result_filename):
    with pytest.raises(IOError):
        reader._read_event_result(valid_result_filename)


def test_read_event_result_malformed_result(dirpath):
    result_file = os.path.join(dirpath, "results", "invalid_result.csv")
    with pytest.raises(exceptions.InvalidHeaderError):
        reader._read_event_result(result_file)

    result_file = os.path.join(dirpath, "results", "missing_result2.csv")
    with pytest.raises(exceptions.MissingHeaderError):
        reader._read_event_result(result_file)


def test_read_event_result_basic_dataframe(dirpath):
    result_file = os.path.join(dirpath, "results", "valid_result_usa.csv")
    result_data = reader._read_event_result(result_file, to_df=True)
    assert isinstance(result_data, DataFrame)

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
    assert included_data <= set(result_data.columns.to_list())
    assert (result_data.position.values == "DNF").sum() == 0  # number of non-finishers
    assert result_data.size == 660250


def test_read_event_result_race_result(dirpath):
    result_file = os.path.join(dirpath, "results", "valid_result_usa.csv")
    result_data = reader._read_event_result(result_file, to_df=False)
    assert isinstance(result_data, types.RaceResult)
    assert result_data.event.event_country == "USA"
    assert result_data.event.event_name == "boston marathon"
    assert result_data.shape[0] == 26410  # number of lines

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
    assert included_data <= set(result_data.columns.to_list())
    assert (result_data.position.values == "DNF").sum() == 0  # number of non-finishers


def test_get_events():
    # test match events
    race_events = reader.get_events(identifier="lochness_marathon")
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

    # test empty match events
    empty_events = reader.get_events(identifier="boston marathon")
    assert len(list(empty_events)) == 0

    # test empty match events
    empty_events = reader.get_events(identifier="abc")
    assert len(list(empty_events)) == 0

    # test fuzzy match events (single word)
    fuzzy_events = reader.get_events(identifier="lochness")
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
    ]:
        assert "lochness_marathon_%s.csv" % yr in basename_events

    assert len(race_events) == 19

    # test filtered events with year
    filtered_events = reader.get_events(identifier="lochness_marathon", year="2019")
    result_set = list(filtered_events)
    assert len(result_set) == 1
    assert "lochness_marathon_2019.csv" in os.path.basename(result_set[0].path)
    assert os.path.exists(result_set[0].path)
    assert type(reader._read_event_result(result_set[0].path)) is types.RaceResult

    from runpandas.datasets.schema import RunTypeEnum

    filtered_events = reader.get_events(
        identifier="lochness_marathon", run_type=RunTypeEnum.MARATHON
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
