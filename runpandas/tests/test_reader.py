'''
Test module for reader base module
'''

import os
import pytest
import runpandas
from pandas import DataFrame
from runpandas import reader
from runpandas import exceptions
from runpandas import types

@pytest.fixture(scope="session")
def invalid_tcx_filename(tmpdir_factory):
    return tmpdir_factory.getbasetemp().join("activity.pwx")

@pytest.fixture(scope="session")
def valid_tcx_filename(tmpdir_factory):
    return tmpdir_factory.getbasetemp().join("activity.tcx")

@pytest.fixture
def dirpath(datapath):
    return datapath("io", "data")

def test_import_module_exists():
    assert reader._import_module('tcx')

def test_top_level_import():
    assert runpandas.read_file == reader._read_file

def test_imort_module_not_exists():
    with pytest.raises(ImportError):
        reader._import_module('json')

def test_read_file_invalid(invalid_tcx_filename):
        invalid_tcx_filename.write('content')
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
        included_data = set(['latitude_degrees', 'longitude_degrees', 'altitude_meters', 'distance_meters', 'heart_rate_bpm'])
        assert included_data <= set(activity.columns.to_list())
        assert  activity.size == 1920

'''
def test_read_file_tcx_basic_activity(dirpath):
        tcx_file = os.path.join(dirpath, "tcx", "basic.tcx")
        activity = reader._read_file(tcx_file, to_df=False)
        assert type(activity) is types.Activity
        assert activity.size == 1920
'''
