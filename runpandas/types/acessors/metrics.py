"""
This is a module for extending pandas dataframes with the runpandas toolbox
"""

import pandas as pd
import numpy as np
from haversine import haversine as hv
from haversine import Unit
from runpandas import exceptions
from runpandas._utils import special_column
from runpandas.types import Activity
from runpandas.types import columns


@pd.api.extensions.register_dataframe_accessor("compute")
class MetricsAcessor(object):
    """
    Dataframe Accessor to compute all available metrics from an activity

    Raises
    ------
    AttributeError
        if at least one of the needed columns is missing.

    """

    def __init__(self, activity):
        self._validate(activity)
        self._activity = activity

    @staticmethod
    def _validate(activity):
        assert isinstance(activity, Activity), "Activity is needed for this accessor"

        if not isinstance(activity.index, (pd.DatetimeIndex, pd.TimedeltaIndex)):
            raise AttributeError(
                "An activity needs a DataFrame Index in DateTimeIndex format"
            )

    def __correct_distance(self, distance_series, col_alt="alt"):
        if col_alt not in self._activity.columns:
            raise exceptions.RequiredColumnError(col_alt)

        self._activity["shift_alt"] = self._activity[col_alt].shift(1)
        self._activity["alt_dif"] = self._activity.apply(
            lambda x: x["shift_alt"] - x[col_alt], axis=1
        )
        self._activity["distance_haversine"] = distance_series
        distance_corrected = self._activity.apply(
            lambda x: np.sqrt(x["distance_haversine"] ** 2 + (x["alt_dif"]) ** 2),
            axis=1,
        )
        self._activity.drop(
            ["shift_alt", "alt_dif", "distance_haversine"], axis=1, inplace=True
        )

        return distance_corrected

    @special_column(required_columns=("lat", "lon"), name="distpos")
    def distance(self, correct_distance=False, to_special_column=True, **kwargs):
        """
        Calculates the distance in meters using haversine distance formula on an Activity frame.

        Parameters
        ----------
        correct_distance: bool, optional
            It computes the distance corrected by the altitude. default is False.

        to_special_column: bool, optional
            It converts the distance calculated (`pandas.Series`) to special runpandas
            distance cummulative column (`runpandas.types.columns.DistancePerPosition`).
            Default is True.

        **kwargs: Keyword args to be passed to the `haversine` method

        Returns
        -------
        haversine_dist: pandas.Series or runpandas.types.columns.DistancePerPosition
            A Series of floats representing the distance in meters
            with the same index of the accessed activity object.

        """
        self._activity["point"] = self._activity.apply(
            lambda x: (x["lat"], x["lon"]), axis=1
        )
        self._activity["point_next"] = self._activity["point"].shift(1)
        self._activity.loc[self._activity["point_next"].isna(), "point_next"] = None
        haversine_dist = self._activity.apply(
            lambda x: hv(x["point"], x["point_next"], unit=Unit.METERS)
            if x["point_next"] is not None
            else float("nan"),
            axis=1,
        )
        self._activity.drop(["point_next", "point"], axis=1, inplace=True)

        if correct_distance:
            haversine_dist = self.__correct_distance(haversine_dist)

        if to_special_column:
            haversine_dist = columns.DistancePerPosition(haversine_dist)

        return haversine_dist

    @special_column(required_columns=(), name="speed")
    def speed(self, from_distances=False, to_special_column=True, **kwargs):
        """
        Calculates the speed in meters using an Activity frame.

        Parameters
        ----------
        from_distances: bool, optional
            Should the speeds be calculated from the distance recordings
            instead of taken from the speed recordings directly? Default is False.

        to_special_column: convert the distance calculated (`pandas.Series`)
            to special runpandas distance cummulative column (`runpandas.types.columns.Speed`).
            Default is True.

        **kwargs: Keyword args to be passed to the `haversine` method

        Returns
        -------
        speed: `pandas.Series` or `runpandas.types.columns.Speed`
            A Series of floats representing the speed in meters
            with the same index of the accessed activity object.

        """
        if from_distances:
            if "distpos" not in self._activity.columns:
                raise exceptions.RequiredColumnError("distpos")

            time_diff = (
                self._activity.index.to_series().diff().fillna(self._activity.index[0])
            ) / np.timedelta64(1, "s")
            speed = self._activity["distpos"] / time_diff
        else:
            if "speed" not in self._activity.columns:
                raise exceptions.RequiredColumnError("speed")
            speed = self._activity["speed"]

        if to_special_column:
            speed = columns.Speed(speed)

        return speed
