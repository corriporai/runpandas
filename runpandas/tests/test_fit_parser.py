'''
Test module for FIT reader base module
'''

import os
import pytest
from pandas import DataFrame, TimedeltaIndex
from runpandas import reader
from runpandas import exceptions
from runpandas import types

@pytest.fixture
def dirpath(datapath):
    return datapath("io", "data")

