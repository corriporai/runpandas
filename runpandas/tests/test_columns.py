"""
Test module for runpandas column types (i.e. MeasureSeries)
"""

import os
import pytest
from runpandas import reader

pytestmark = pytest.mark.stable


@pytest.fixture
def dirpath(datapath):
    return datapath("io", "data")


def test_speed_kmh(dirpath):
    tcx_file = os.path.join(dirpath, "tcx", "stopped_example.tcx")
    activity_tcx = reader._read_file(tcx_file, to_df=False)
    # test conversion method m/s to km/h
    assert (activity_tcx["speed"].kph[-1]) == 8.498772
