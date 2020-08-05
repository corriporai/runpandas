'''
Tools for parsing Garmin GPX files.
'''
import pandas as pd
from pandas import TimedeltaIndex
from runpandas import _utils as utils
from runpandas import exceptions
from runpandas.types import Activity
from runpandas.types import columns


def gen_records(file_path):
    nodes = gen_nodes(file_path, ('tkrpt'), with_root=True)

    root = next(nodes)
    if utils.sans_ns(root.tag) != 'gpx':
            raise exceptions.InvalidFileError('gpx')

    #trackpoints = nodes
    #for trkpt in trackpoints:
    #    yield utils.recursive_text_extract(trkpt)