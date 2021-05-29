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
            to special runpandas speed column (`runpandas.types.columns.Speed`).
            Default is True.

        **kwargs: Keyword args to be passed to the speed building method

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

    @special_column(required_columns=("alt",), name="vam")
    def vertical_speed(self, to_special_column=True, **kwargs):
        """
        Calculates the vertical climbing speed (VAM) in meters using an Activity frame.

        Parameters
        ----------
        to_special_column: convert the distance calculated (`pandas.Series`)
            to special runpandas VAM column (`runpandas.types.columns.VAM`).
            Default is True.

        **kwargs: Keyword args to be passed to the VAM build method

        Returns
        -------
        vam: `pandas.Series` or `runpandas.types.columns.VAM`
            A Series of floats representing the vertical altitude speed in meters
            with the same index of the accessed activity object.

        """
        time_diff = (
            self._activity.index.to_series().diff().fillna(self._activity.index[0])
        ) / np.timedelta64(1, "s")
        dvert = self._activity["alt"].diff()

        vam = dvert / time_diff
        if to_special_column:
            vam = columns.VAM(vam)

        return vam

    @special_column(required_columns=("alt", "dist"), name="grad")
    def gradient(self, to_special_column=True, **kwargs):
        """
        Calculates the gradient ratio from an Activity frame.

        Parameters
        ----------
        to_special_column: convert the distance calculated (`pandas.Series`)
            to special runpandas Gradient column (`runpandas.types.columns.Gradient`).
            Default is True.

        **kwargs: Keyword args to be passed to the Gradient build method

        Returns
        -------
        grad: `pandas.Series` or `runpandas.types.columns.Gradient`
            A Series of floats representing the vertical altitude speed in meters
            with the same index of the accessed activity object.

        """
        alt = self._activity["alt"].diff()
        dist = self._activity["dist"].diff()

        grad = alt / dist
        if to_special_column:
            grad = columns.Gradient(rise=alt, run=dist)

        return grad

    @special_column(required_columns=("speed",), name="pace")
    def pace(self, to_special_column=True, **kwargs):
        """
        Calculates the pace (the time that it takes to cover distances in your activities).

        Parameters
        ----------
        to_special_column: convert the pace calculated (`pandas.Series`)
            to special runpandas Pace column (`runpandas.types.columns.Pace`).
            Default is True.

        **kwargs: Keyword args to be passed to the Pace build method

        Returns
        -------
        pace: `pandas.Series` or `runpandas.types.columns.Pace`
            A Series of floats representing the pace in meters per second
            with the same index of the accessed activity object.

        """
        speed = self._activity["speed"]

        pace = pd.to_timedelta(1 / speed, unit="s")
        # pace = (1 / speed).apply(pd.Timedelta, args=('s',))

        if to_special_column:
            pace = columns.Pace(pace)

        return pace

    @special_column(required_columns=("hr",))
    def heart_zone(self, bins, labels, **kwargs):
        """
        Returns a `pandas.Series` with the training zone labels for each heart rate record.
        This method uses the pandas.cut() method.
        Nan will be returned for values that are not in any of the bins.

        Parameters
        ----------

        bins: Left and right bounds for each zone.
                An example of valid bins are [0, 100, 140, 160, 999].

        labels: Specifies the labels for the zones.
                Must be the same length as the resulting zones.
                Example of valid labels is ["Z1", "Z2", "Z3", "Z4", "Z5"].

        **kwargs: Keyword args to be passed to the heart_zone build method

        Returns
        -------
        series:  `pandas.Series` with the zone label for each value.
        """
        bins_series = pd.cut(self._activity["hr"], bins=bins, labels=labels)
        return pd.Series(bins_series, index=bins_series.index, name="hr_zone")

    @special_column(required_columns=("hr",), name="time_in_zone")
    def time_in_zone(self, bins, labels, **kwargs):
        """
        Returns a `pandas.Series` with the values counts in timedelta for each
        heart training zone.
        This method uses the pandas.Series.values_count() method.

        Parameters
        ----------

        bins: Left and right bounds for each zone.
                An example of valid bins are [0, 100, 140, 160, 999].

        labels: Specifies the labels for the zones.
                Must be the same length as the resulting zones.
                Example of valid labels is ["Z1", "Z2", "Z3", "Z4", "Z5"].

        **kwargs: Keyword args to be passed to the time_in_zone build method

        Returns
        -------
        series: A `pandas.Series` with the values count in `pandas.Timedelta` for each zones.
        """
        hr_zones = self.heart_zone(bins, labels).to_frame()
        hr_zones["time_diff"] = (
            hr_zones.index.to_series().diff().fillna(hr_zones.index[0])
        ) / np.timedelta64(1, "s")
        return pd.to_timedelta(hr_zones.groupby(["hr_zone"]).time_diff.sum(), unit="s")
