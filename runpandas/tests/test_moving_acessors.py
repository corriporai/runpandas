"""
Test module for runpandas acessors
"""

import os
import pytest
from runpandas import reader


pytestmark = pytest.mark.stable


@pytest.fixture
def dirpath(datapath):
    return datapath("io", "data")


def test_metrics_validate(dirpath):
    gpx_file = os.path.join(dirpath, "gpx", "stopped_example.gpx")
    activity_gpx = reader._read_file(gpx_file, to_df=True)

    #copy of dataframe for testing the index error
    frame_without_index = activity_gpx.copy()
    frame_without_index = frame_without_index.reset_index()
    with pytest.raises(AttributeError):
        frame_without_index.only_moving()


    frame_gpx = reader._read_file(gpx_file, to_df=False)

    tcx_file = os.path.join(dirpath, "tcx", "stopped_example.tcx")
    activity_tcx = reader._read_file(tcx_file, to_df=True)
    frame_tcx = reader._read_file(tcx_file, to_df=False)