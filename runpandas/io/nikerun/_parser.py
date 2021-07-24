"""
Tools for parsing Nike Run JSON files.
"""
import os
import datetime
import json
from pathlib import Path
import numpy as np
import pandas as pd
from pandas import TimedeltaIndex
from runpandas import _utils as utils
from runpandas import exceptions
from runpandas.types import Activity, columns

# According to Garmin, all times are stored in UTC.
DATETIME_FMT = "%Y-%m-%dT%H:%M:%SZ"

COLUMNS_SCHEMA = {
    "elevation": columns.Altitude,
    "heart_rate": columns.HeartRate,
    "longitude": columns.Longitude,
    "latitude": columns.Latitude,
}


def __is_nikerun_valid(file_path):
    """Check if it is a valid format for activity files.

    Parameters
    ----------
    file_path : str
        Path to the file to be read.

    Returns
    -------
    It returns True if the it is a valid format for activities handling.
    """
    _, ext = os.path.splitext(file_path)
    if ext not in [".json"]:
        return False

    with open(file_path) as json_file:
        activity = json.load(json_file)
        if not activity.get("metrics"):
            return False

        metrics = [
            metric["type"]
            for metric in activity["metrics"]
            if metric["type"] in ["latitude", "longitude"]
        ]
        if len(metrics) != 2:
            return False

    return True


def __update_single_metrics(epochs, data):
    counter = 0
    data_values = [np.nan] * len(epochs)
    for idx, epoch in enumerate(epochs):
        while epoch >= data[counter]["end_epoch_ms"]:
            if counter == len(data) - 1:
                break
            data_values[idx] = data[counter]["value"]
            counter += 1

    return data_values


def __update_acummulative_metrics(epochs, data):
    counter = 0
    data_values = [np.nan] * len(epochs)
    for idx, epoch in enumerate(epochs):
        data_cumm = []
        while epoch >= data[counter]["end_epoch_ms"]:
            if counter == len(data) - 1:
                break
            data_cumm.append(data[counter]["value"])
            counter += 1
        if len(data_cumm) > 0:
            data_values[idx] = sum(data_cumm)

    return data_values


def __nikerun_streams(metrics):
    streams = dict()
    stream_types = dict()
    final_streams = dict()
    for metric in metrics:
        type_metric = metric["type"]
        unit = metric["unit"]
        streams[type_metric] = metric["values"]
        stream_types[type_metric] = unit

    # get latitude and longitude, build them and corresponding timestamp values
    latitude_data, longitude_data = streams["latitude"], streams["longitude"]
    latitude_values, longitude_values, epoch_ms, epoch_datetime = [], [], [], []
    for lat, lon in zip(latitude_data, longitude_data):
        if lat["start_epoch_ms"] != lon["start_epoch_ms"]:
            raise ValueError("\tThe latitude and longitude data is out of order")
        latitude_values.append(lat["value"])
        longitude_values.append(lon["value"])
        epoch_ms.append(lat["start_epoch_ms"])
        epoch_datetime.append(
            datetime.datetime.utcfromtimestamp(lat["start_epoch_ms"] / 1000)
        )

    final_streams["latitude"] = latitude_values
    final_streams["longitude"] = longitude_values
    final_streams["time"] = epoch_datetime

    final_streams["elevation"] = __update_single_metrics(epoch_ms, streams["elevation"])
    if "heart_rate" in streams:
        final_streams["heart_rate"] = __update_single_metrics(
            epoch_ms, streams["heart_rate"]
        )

    if "calories" in streams:
        final_streams["calories"] = __update_acummulative_metrics(
            epoch_ms, streams["calories"]
        )
    if "steps" in streams:
        final_streams["steps"] = __update_acummulative_metrics(
            epoch_ms, streams["steps"]
        )
    if "nikefuel" in streams:
        final_streams["nikefuel"] = __update_acummulative_metrics(
            epoch_ms, streams["nikefuel"]
        )

    return final_streams


def gen_records(file_path):
    with open(file_path) as json_file:
        activity = json.load(json_file)
        streams = __nikerun_streams(activity.get("metrics"))
        return streams


def read_nikerun(file_path, to_df=False, **kwargs):
    """
    This method loads a NikeRun API response in JSON file into a Pandas DataFrame
    or runpandas Activity.
    Column names are translated to runpandas terminology
    (e.g. "HeartRate" > "heart_rate").
    Datetimes indexes are replaced by time offsets.
    All NaN rows are removed.

    Parameters
    ----------
        file_path : str, The path to a training file.
        to_df : bool, optional
             Return a obj:`runpandas.Activity` if `to_df=True`,
              otherwise a :obj:`pandas.DataFrame` will be returned.
              Defaults to False.
        **kwargs :
        Keyword args to be passed to the `read` method
              accordingly to the file format.
    Returns
    -------
    Return a obj:`runpandas.Activity` if `to_df=True`, otherwise
             a :obj:`pandas.DataFrame` will be returned.
    """
    if not utils.file_exists(file_path):
        raise IOError("%s does not exist" % file_path)
    if not __is_nikerun_valid(file_path):
        raise exceptions.InvalidFileError(
            "File {file_path} with invalid filetype.".format(**locals())
        )

    data = pd.DataFrame.from_records(gen_records(file_path))
    times = data.pop("time")  # should always be there
    data = data.astype("float64", copy=False)  # try and make numeric
    data.columns = map(utils.camelcase_to_snakecase, data.columns)
    timestamps = pd.to_datetime(times, format=DATETIME_FMT, utc=True)

    timeoffsets = timestamps - timestamps[0]
    timestamp_index = TimedeltaIndex(timeoffsets, unit="s", name="time")
    data.index = timestamp_index
    data.dropna(axis=1, how="all", inplace=True)

    if to_df:
        return data

    return Activity(data, cspecs=COLUMNS_SCHEMA, start=timestamps[0])


def read_dir_nikerun(dirname, **kwargs):
    """
    Read all NikeRun JSON container files from a supplied directory
    as `runpandas.Activity` dataframes, and aggregate them
    to the same session as a `pandas.MultiIndex` activity dataframe.

    Parameters
    ----------
        dirname : str, The path to a directory with training files.
             Return a obj:`runpandas.Activity` if `to_df=True`, otherwise
             a :obj:`pandas.DataFrame` will be returned. Defaults to False.
        **kwargs : Keyword args to be passed to the `read_dir` method

    Returns
    -------
    Return a  :obj:`runpandas.Activity` split into sessions based
    on the `pandas.MultiIndex` with the date/time of the activity
    as first level and the second the timestamps for each record.
    """
    activities = []
    activity_keys = []

    path_dir = Path(dirname)

    assert path_dir.is_dir()

    for path_file in path_dir.iterdir():
        if path_file.is_dir():
            continue

        activity = read_nikerun(path_file, to_df=False, **kwargs)
        activities.append(activity)
        activity_keys.append(activity.start)
    if len(activities) > 0:
        multi_frame = pd.concat(
            activities, keys=activity_keys, names=["start", "time"], axis=0
        )
        return multi_frame

    return None
