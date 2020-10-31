"""
Tools for parsing FIT files.
"""

import pandas as pd
from pandas import TimedeltaIndex
from fitparse import FitFile
from runpandas import _utils as utils
from runpandas.types import Activity
from runpandas.types import columns

COLUMNS_SCHEMA = {
    "distance": columns.Distance,
    "cadence": columns.Cadence,
    "altitude": columns.Altitude,
    "heart_rate": columns.HeartRate,
    "position_long": columns.Longitude._from_semicircles_to_degrees,
    "position_lat": columns.Latitude._from_semicircles_to_degrees,
    "power": columns.Power,
    "speed": columns.Speed,
    "temperature": columns.Temperature,
}


def message_filter(message, keep=("record", "lap", "event")):
    return message.mesg_type is not None and message.mesg_type.name in keep


def gen_records(file_path):
    """Generator function for iterating over *.fit file messages.
    Parameters
    ----------
    file_path : str
        Path to the ANT/Garmin fit file.

    Yields
    ------
        Parsed messages from `file_path`.
    """
    fit_file = FitFile(file_path)

    messages = filter(message_filter, fit_file.get_messages())
    lap = 0
    session = -1

    for record in messages:
        if record.mesg_type.name == "record":
            message = record.get_values()
            message["lap"] = lap
            message["session"] = session
            yield message
        elif record.mesg_type.name == "lap":
            lap += 1
        elif record.mesg_type.name == "event":
            if record.get_value("event_type") == "start":
                # This happens whens an activity is
                # (manually or automatically) paused or
                # stopped and the resumed
                session += 1
        else:
            raise ValueError(
                "Unknown message fit type {0}.".format(record.mesg_type.name)
            )


def read(file_path, to_df=False, **kwargs):
    """
    This method loads a FIT file into a Pandas DataFrame or runpandas Activity.
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
    start = None
    timeoffsets = None

    data = pd.DataFrame.from_records(gen_records(file_path))

    data.columns = map(utils.camelcase_to_snakecase, data.columns)

    if "timestamp" in data:
        timestamps = data.pop("timestamp")
        timestamps = pd.to_datetime(timestamps, utc=True)

        timeoffsets = timestamps - timestamps[0]
        timestamp_index = TimedeltaIndex(timeoffsets, unit="s", name="time")
        data.index = timestamp_index
        start = timestamps[0]

    data.dropna(axis=1, how="all", inplace=True)

    if to_df:
        return data
    else:
        return Activity(data, cspecs=COLUMNS_SCHEMA, start=start)
