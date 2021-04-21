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
)
from runpandas.datasets.schema import ActivityData, FileTypeEnum
from runpandas import read_file
from runpandas.types import Activity

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
