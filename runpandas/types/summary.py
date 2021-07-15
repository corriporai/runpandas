"""
    Helper module for evaluation and display of the summary of training sessions.

 """

import numpy as np
import pandas as pd
from runpandas._utils import convert_pace_secmeters2minkms


def _build_summary_statistics(obj):
    """
    Generate session statistics from a given DataFrame.

    Parameters
    ----------
    obj:  The DataFrame to generate basic commute statistics from.

    Returns:
    --------
    A Dictionary containing the following statistics:
    - Total moving time
    - Average speed
    - Max speed
    - Average moving speed
    - Average cadence running
    - Average cadence running moving
    - Max cadence
    - Average heart rate
    - Average heart rate moving
    - Max heart rate
    - Average pace (per 1 km)
    - Average pace moving (per 1 km)
    - Max pace
    - Average temperature
    - Max temperature
    - Min temperature
    - Total distance
    - Total ellapsed time
    """

    start = obj.start

    try:
        moving_time = obj.moving_time
    except AttributeError:
        moving_time = np.nan

    try:
        mean_speed = obj.mean_speed()
        max_speed = obj["speed"].max()
        mean_pace = convert_pace_secmeters2minkms(obj.mean_pace().total_seconds())
        max_pace = convert_pace_secmeters2minkms(
            obj["speed"].to_pace().min().total_seconds()
        )
    except AttributeError:
        mean_speed = np.nan
        max_speed = np.nan
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
        max_cadence = obj["cad"].max()
    except AttributeError:
        mean_cadence = np.nan
        max_cadence = np.nan

    try:
        mean_moving_cadence = obj.mean_cadence(only_moving=True)
    except (AttributeError, KeyError):
        mean_moving_cadence = np.nan

    try:
        mean_heart_rate = obj.mean_heart_rate()
        max_heart_rate = obj["hr"].max()
    except AttributeError:
        mean_heart_rate = np.nan
        max_heart_rate = np.nan

    try:
        mean_moving_heart_rate = obj.mean_heart_rate(only_moving=True)
    except (AttributeError, KeyError):
        mean_moving_heart_rate = np.nan

    try:
        mean_temperature = obj["temp"].mean()
        min_temperature = obj["temp"].min()
        max_temperature = obj["temp"].max()
    except KeyError:
        mean_temperature = np.nan
        min_temperature = np.nan
        max_temperature = np.nan

    total_distance = obj.distance

    ellapsed_time = obj.ellapsed_time

    row = {k: v for k, v in locals().items() if not k.startswith("__") and k != "obj"}

    return row


def _build_session_statistics(obj):
    """
    Generate session statistics from a given DataFrame.

    Parameters
    ----------
    obj:  The DataFrame to generate basic commute statistics from.

    Returns:
    --------
    A ``pandas.Dataframe`` containing the following statistics:
    - Total moving time
    - Average speed
    - Max speed
    - Average moving speed
    - Average cadence running
    - Average cadence running moving
    - Max cadence
    - Average heart rate
    - Average heart rate moving
    - Max heart rate
    - Average pace (per 1 km)
    - Average pace moving (per 1 km)
    - Max pace
    - Average temperature
    - Max temperature
    - Min temperature
    - Total distance
    - Total ellapsed time
    """
    stats = {key: [value] for key, value in _build_summary_statistics(obj).items()}
    return pd.DataFrame(stats).set_index("start")


def _build_activity_statistics(obj):
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
    """
    # special conditions for methods that raise Exceptions
    stats = _build_summary_statistics(obj)

    rows = {
        "Session": "Running: %s" % stats["start"].strftime("%d-%m-%Y %H:%M:%S"),
        "Total distance (meters)": stats["total_distance"],
        "Total ellapsed time": stats["ellapsed_time"],
        "Total moving time": stats["moving_time"],
        "Average speed (km/h)": stats["mean_speed"] * 3.6,
        "Average moving speed (km/h)": stats["mean_moving_speed"] * 3.6,
        "Average pace (per 1 km)": stats["mean_pace"],
        "Average pace moving (per 1 km)": stats["mean_moving_pace"],
        "Average cadence": stats["mean_cadence"],
        "Average moving cadence": stats["mean_moving_cadence"],
        "Average heart rate": stats["mean_heart_rate"],
        "Average moving heart rate": stats["mean_moving_heart_rate"],
        "Average temperature": stats["mean_temperature"],
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
    Returns the pandas Dataframe with the common basic statistics for the
    given activity.

    Parameters
    ----------
    activity:  runpandas.types.Activity. Runpandas Activity to be computed the statistics

    Returns
    -------
        pandas.Dataframe:  A pandas DataFrame containing the summary statistics, which
        inclues estimates of the total distance covered, the total duration,
        the time spent moving, and many others.

    """
    summary_statistics = _build_activity_statistics(activity)
    return summary_statistics.T


def session_summary(session):
    """
    Returns the a pandas Dataframe with the common basic statistics for the
    given activity.

    Parameters
    ----------
    session:  runpandas.types.Activity. Runpandas Activity with pandas.MultiIndex
    to be computed the statistics

    Returns
    -------
    pandas.Dataframe:  A pandas DataFrame containing the summary statistics
    across all th activities, which includes estimates of the total distance covered,
    the total duration, the time spent moving, and many others.

    """
    frames = []
    for index in session.index.unique(level="start"):
        df = session.xs(index, level=0)
        df.start = index
        frames.append(_build_session_statistics(df))

    session_summary = pd.concat(frames, axis=0, verify_integrity=True)
    session_summary.sort_index(inplace=True)
    return session_summary
