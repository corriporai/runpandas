"""
Tools for pulling and parsing stream data from Strava.
"""

from datetime import timedelta
import pandas as pd
from pandas import TimedeltaIndex
from runpandas import _utils as utils
from runpandas.types import Activity
from runpandas.types import columns
from stravalib.client import Client


COLUMNS_SCHEMA = {
    "altitude": columns.Altitude,
    "cadence": columns.Cadence,
    "distance": columns.Distance,
    "heartrate": columns.HeartRate,
    "longitude": columns.Longitude,
    "latitude": columns.Latitude,
    "watts": columns.Power,
}

STREAM_TYPES = [
    "time",
    "latlng",
    "distance",
    "altitude",
    "velocity_smooth",
    "heartrate",
    "cadence",
    "watts",
    "temp",
    "moving",
    "grade_smooth",
]


def gen_records(streams):
    raw_data = dict()
    for key, value in streams.items():
        if key == "latlng":
            latitude, longitude = list(zip(*value.data))
            raw_data["latitude"] = latitude
            raw_data["longitude"] = longitude
        else:
            raw_data[key] = value.data
    return raw_data


def read_strava(
    activity_id,
    access_token,
    refresh_token=None,
    client_id=None,
    client_secret=None,
    to_df=False,
    **kwargs
):
    """
    This method loads the activity data from Strava into a Pandas DataFrame or
    runpandas Activity.
    Column names are translated to runpandas terminology
    (e.g. "heartrate" > "heart_rate").
    Datetimes indexes are replaced by time offsets.
    All NaN rows are removed.

    Attention: Two API requests are made to the Strava webservice: 1 to
               retrieve activity metadata, 1 to retrieve the raw data ("streams").

    Parameters
    ----------
        activity_id : str, The id of the activity
        access_token: str, The Strava access token
        refresh_token: str, The Strava refresh token, optional
        client_id: int, The Strava client id used for token refresh, optional
        client_secret: str, The strava client secret used for token refresh, optional
        to_df : bool, optional
             Return a obj:`runpandas.Activity` if `to_df=True`, otherwise
             a :obj:`pandas.DataFrame` will be returned. Defaults to False.
        **kwargs :
        Keyword args to be passed to the `read_strava`
    Returns
    -------
    Return a obj:`runpandas.Activity` if `to_df=True`, otherwise
             a :obj:`pandas.DataFrame` will be returned.
    """

    client = Client()
    client.access_token = access_token
    client.refresh_token = refresh_token

    activity = client.get_activity(activity_id)

    start_datetime = activity.start_date_local
    print(start_datetime)
    streams = client.get_activity_streams(
        activity_id=activity_id, types=STREAM_TYPES, series_type="time"
    )

    data = pd.DataFrame(gen_records(streams))

    times = data.pop("time")
    data.columns = map(utils.camelcase_to_snakecase, data.columns)

    def time_to_datetime(time):
        return start_datetime + timedelta(seconds=time)

    timestamps = times.apply(time_to_datetime)
    timeoffsets = timestamps - timestamps[0]
    timestamp_index = TimedeltaIndex(timeoffsets, unit="s", name="time")
    data.index = timestamp_index
    data.dropna(axis=1, how="all", inplace=True)

    if to_df:
        return data
    else:
        return Activity(data, cspecs=COLUMNS_SCHEMA, start=timestamps[0])
