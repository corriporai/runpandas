'''
Test module for reader base module
'''

import os
import pytest
from runpandas import reader
from runpandas import exceptions

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

def test_read_file_tcx_basic_dataframe(dirpath):
        tcx_file = os.path.join(dirpath, "tcx", "basic.tcx")
        reader._read_file(tcx_file)