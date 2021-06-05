"""
    Helper module for evaluation and display of the summary of training sessions.

 """

import numpy as np
import pandas as pd
from runpandas._utils import convert_pace_secmeters2minkms


def _build_summary_statistics(obj):
    """
    Generate basic statistics from a given pandas Series.

    Parameters
    ----------
    obj:  The DataFrame to generate basic commute statistics from.

    Returns:
    --------

    A Series containing the following statistics:
    - Session times
    - Total distance
    - Total ellapsed time
    - Total moving time
    - Total and average elevation gain
    - Average speed
    - Average moving speed
    - Average pace (per 1 km)
    - Average pace moving (per 1 km)
    - Average cadence running
    - Average cadence running moving
    - Average heart rate
    - Average heart rate moving
    - Average temperature
    - Total elevation gain
    """
    # special conditions for methods that raise Exception
    try:
        moving_time = obj.moving_time
    except AttributeError:
        moving_time = np.nan

    try:
        mean_speed = obj.mean_speed()
        mean_pace = convert_pace_secmeters2minkms(obj.mean_pace().total_seconds())
    except AttributeError:
        mean_speed = np.nan
        mean_pace = np.nan

    try:
        mean_moving_speed = obj.mean_speed(only_moving=True)
        mean_moving_pace = convert_pace_secmeters2minkms(
            obj.mean_pace(only_moving=True).total_seconds()
        )
    except (AttributeError, KeyError):
        mean_moving_speed = np.nan
        mean_moving_pace = np.nan

    try:
        mean_cadence = obj.mean_cadence()
    except AttributeError:
        mean_cadence = np.nan

    try:
        mean_moving_cadence = obj.mean_cadence(only_moving=True)
    except (AttributeError, KeyError):
        mean_moving_cadence = np.nan

    try:
        mean_heart_rate = obj.mean_heart_rate()
    except AttributeError:
        mean_heart_rate = np.nan

    try:
        mean_moving_heart_rate = obj.mean_heart_rate(only_moving=True)
    except (AttributeError, KeyError):
        mean_moving_heart_rate = np.nan

    try:
        mean_temperature = obj["temp"].mean()
    except KeyError:
        mean_temperature = np.nan

    rows = {
        "Session": "Running: %s" % obj.start.strftime("%d-%m-%Y %H:%M:%S"),
        "Total distance (meters)": obj.distance,
        "Total ellapsed time": obj.ellapsed_time,
        "Total moving time": moving_time,
        "Average speed (km/h)": mean_speed * 3.6,
        "Average moving speed (km/h)": mean_moving_speed * 3.6,
        "Average pace (per 1 km)": mean_pace,
        "Average pace moving (per 1 km)": mean_moving_pace,
        "Average cadence": mean_cadence,
        "Average moving cadence": mean_moving_cadence,
        "Average heart rate": mean_heart_rate,
        "Average moving heart rate": mean_moving_heart_rate,
        "Average temperature": mean_temperature,
    }

    series = pd.Series(
        rows,
        index=[
            "Session",
            "Total distance (meters)",
            "Total ellapsed time",
            "Total moving time",
            "Average speed (km/h)",
            "Average moving speed (km/h)",
            "Average pace (per 1 km)",
            "Average pace moving (per 1 km)",
            "Average cadence",
            "Average moving cadence",
            "Average heart rate",
            "Average moving heart rate",
            "Average temperature",
        ],
    )

    return series


def activity_summary(activity):
    """
    Returns the a pandas Dataframe with the common basic statistics for the
    given activity.

    Parameters
    ----------
    activity:  runpandas.types.Activity
    Runpandas Activity to be computed the statistics

    Returns:
    --------
        pandas.Dataframe:  A pandas DataFrame containing the summary statistics, which
        inclues estimates of the total distance covered, the total duration,
        the time spent moving, and many others.

    """
    summary_statistics = _build_summary_statistics(activity)
    return summary_statistics.T
