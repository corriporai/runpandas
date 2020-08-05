'''
Tools for parsing Garmin TCX files.
'''
import pandas as pd
from pandas import TimedeltaIndex
from runpandas import _utils as utils
from runpandas import exceptions
from runpandas.types import Activity
from runpandas.types import columns

COLUMNS_SCHEMA = {
    'atemp': columns.Temperature,
    'cad': columns.Cadence,
    'ele': columns.Cadence,
    'lon': columns.Longitude,
    'lat': columns.Latitude,
    'hr': columns.HeartRate,
}

# According to Garmin, all times are stored in UTC.
DATETIME_FMT = '%Y-%m-%dT%H:%M:%SZ'
# Despite what the schema says, there are files out
# in the wild with fractional seconds...
DATETIME_FMT_WITH_FRAC = '%Y-%m-%dT%H:%M:%S.%fZ'

def gen_records(file_path):
    nodes = utils.get_nodes(file_path, ('Trackpoint',), with_root=True)
    root = next(nodes)
    if utils.sans_ns(root.tag) != 'TrainingCenterDatabase':
        raise exceptions.InvalidFileError('tcx')

    trackpoints = nodes
    for trkpt in trackpoints:
        yield utils.recursive_text_extract(trkpt)

def read(file_path):
    data = pd.DataFrame.from_records(gen_records(file_path))
    times = data.pop('Time')                    # should always be there
    data = data.astype('float64', copy=False)   # try and make numeric
    data.columns = map(utils.camelcase_to_snakecase, data.columns)
    try:
        timestamps = pd.to_datetime(times, format=DATETIME_FMT, utc=True)
    except ValueError:  # bad format, try with fractional seconds
        timestamps = pd.to_datetime(times, format=DATETIME_FMT_WITH_FRAC, utc=True)

    timeoffsets = timestamps - timestamps[0]
    timestamp_index = TimedeltaIndex(timeoffsets, unit='s', name='time')

    return Activity(data, cspecs=COLUMNS_SCHEMA, start=timestamps[0], index=[timestamp_index])