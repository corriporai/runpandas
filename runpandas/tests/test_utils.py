"""
Tests for utils module
"""
import os
import pytest
from runpandas import _utils as utils

pytestmark = pytest.mark.stable


@pytest.fixture(scope="session")
def valid_tcx_filename(tmpdir_factory):
    return tmpdir_factory.getbasetemp().join("activity.tcx")


@pytest.fixture(scope="session")
def invalid_tcx_filename(tmpdir_factory):
    return tmpdir_factory.getbasetemp().join("activity.tcx.gz")


def test_file_exists(valid_tcx_filename):
    f = open(valid_tcx_filename, "w")
    f.write("test")
    f.close()  # open and close to toucj
    assert utils.file_exists(valid_tcx_filename)


def test_file_not_exists(invalid_tcx_filename):
    assert not utils.file_exists(invalid_tcx_filename)


def test_splitext_plus(valid_tcx_filename):
    prefix, sufix = utils.splitext_plus(valid_tcx_filename)
    assert os.path.basename(prefix) == "activity"
    assert sufix == ".tcx"


def test_splitext_plus_with_zip(invalid_tcx_filename):
    prefix, sufix = utils.splitext_plus(invalid_tcx_filename)
    assert os.path.basename(prefix) == "activity"
    assert sufix == ".tcx.gz"


def is_valid(valid_tcx_filename):
    assert utils.is_valid(valid_tcx_filename)
    assert not utils.is_valid("invalid_tcx_filename")


def is_valid_nok(invalid_tcx_filename):
    assert not utils.is_valid(invalid_tcx_filename)


def test_camecase_to_snakecase():
    assert utils.camelcase_to_snakecase("LatitudeDegrees") == "latitude_degrees"
    assert utils.camelcase_to_snakecase("Time") == "time"
