"""
Tools for parsing Garmin TCX files.
"""
import pandas as pd
from pandas import TimedeltaIndex
from runpandas import _utils as utils
from runpandas import exceptions
from runpandas.types import Activity
from runpandas.types import columns

COLUMNS_SCHEMA = {
    "altitude_meters": columns.Altitude,
    "cadence": columns.Cadence,
    "distance_meters": columns.Distance,
    "heart_rate_bpm": columns.HeartRate,
    "longitude_degrees": columns.Longitude,
    "latitude_degrees": columns.Latitude,
    "speed": columns.Speed,
    "watts": columns.Power,
}

# According to Garmin, all times are stored in UTC.
DATETIME_FMT = "%Y-%m-%dT%H:%M:%SZ"
# Despite what the schema says, there are files out
# in the wild with fractional seconds...
DATETIME_FMT_WITH_FRAC = "%Y-%m-%dT%H:%M:%S.%fZ"


def gen_records(file_path):
    nodes = utils.get_nodes(file_path, ("Trackpoint",), with_root=True)
    root = next(nodes)
    if utils.sans_ns(root.tag) != "TrainingCenterDatabase":
        raise exceptions.InvalidFileError("tcx")

    trackpoints = nodes
    for trkpt in trackpoints:
        yield utils.recursive_text_extract(trkpt)


def read(file_path, to_df=False, **kwargs):
    """
    This method loads a TCX file into a Pandas DataFrame or runpandas Activity.
    Column names are translated to runpandas terminology
    (e.g. "HeartRate" > "heart_rate").
    Datetimes indexes are replaced by time offsets.
    All NaN rows are removed.

    Parameters
    ----------
        filename : str, The path to a training file.
        to_df : bool, optional
             Return a obj:`runpandas.Activity` if `to_df=True`, otherwise
             a :obj:`pandas.DataFrame` will be returned. Defaults to False.
        **kwargs :
        Keyword args to be passed to the `read` method accordingly to the
        file format.
    Returns
    -------
    Return a obj:`runpandas.Activity` if `to_df=True`, otherwise
             a :obj:`pandas.DataFrame` will be returned.
    """
    data = pd.DataFrame.from_records(gen_records(file_path))
    times = data.pop("Time")  # should always be there
    data = data.astype("float64", copy=False)  # try and make numeric
    data.columns = map(utils.camelcase_to_snakecase, data.columns)

    try:
        timestamps = pd.to_datetime(times, format=DATETIME_FMT, utc=True)
    except ValueError:
        # bad format, try with fractional seconds
        timestamps = pd.to_datetime(times, format=DATETIME_FMT_WITH_FRAC, utc=True)

    timeoffsets = timestamps - timestamps[0]
    timestamp_index = TimedeltaIndex(timeoffsets, unit="s", name="time")
    data.index = timestamp_index
    data.dropna(axis=1, how="all", inplace=True)

    if to_df:
        return data
    else:
        return Activity(data, cspecs=COLUMNS_SCHEMA, start=timestamps[0])
