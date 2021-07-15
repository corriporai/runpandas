"""
This is a module for extending pandas activities with session aggregation methods
"""

import pandas as pd
from runpandas.types import Activity
from runpandas.types import summary


@pd.api.extensions.register_dataframe_accessor("session")
class _SessionAcessor(object):
    """
    Dataframe Accessor to compute the aggregated metrics from a MultiIndex
    ``runpandas.types.Activity`` object.

    Raises
    ------
    AttributeError
        if it is not a ``runpandas.types.Activity`` instance or
        not have a ``pd.MultiIndex`` or not have the index levels
        of type ``pd.DateTimeIndex`` or ``pd.TimedeltaIndex``.

    """

    def __init__(self, session):
        self._validate(session)
        self._session = session

    @staticmethod
    def _validate(activity):
        assert isinstance(activity, Activity), "Activity is needed for this accessor"

        if not isinstance(activity.index, pd.MultiIndex) or not set(
            [*map(type, activity.index.levels)]
        ) == set([pd.TimedeltaIndex, pd.DatetimeIndex]):
            raise AttributeError(
                "An activity needs a DataFrame MultiIndex in \
                     (DateTimeIndex, TimedeltaIndex) format."
            )

    def summarize(self):
        """
        Summarize the session of activities by returning a Dataframe
        of the aggregated main statistics.

        Returns
        -------
        pandas.Dataframe: A Dataframe with the summarized statistics for the all the session.
        """
        return summary.session_summary(self._session)

    def count(self):
        """
        Returns the total number of activities in the session.

        Returns
        -------
        int: the total number of activities in the session.

        """
        return self._session.index.levshape[0]

    def distance(self, correct_distance=False, to_special_column=True, **kwargs):
        """
        Compute the distance per position and total distance acummulative
        over all the activities.

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
            `runpandas.Activity`: The runpandas.Activity with the
             new columns dist and distpos computed.

        See Also
        --------
            runpandas.acessors.metrics.distance

        """
        for index in self._session.index.unique(level="start"):
            distpos = self._session.xs(index, level=0).compute.distance(
                correct_distance=correct_distance,
                to_special_column=to_special_column,
                **kwargs
            )
            self._session.loc[
                pd.IndexSlice[index, distpos.index.tolist()], "distpos"
            ] = distpos.values
            dist = distpos.to_distance()
            self._session.loc[
                pd.IndexSlice[index, dist.index.tolist()], "dist"
            ] = dist.values
        return self._session

    def speed(self, from_distances=False, to_special_column=True, **kwargs):
        """
        Compute the speed in meters over all the activities.

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
            `runpandas.Activity`: The runpandas.Activity with the new column speed computed.

        See Also
        --------
            runpandas.acessors.metrics.speed

        """
        for index in self._session.index.unique(level="start"):
            speed = self._session.xs(index, level=0).compute.speed(
                from_distances=from_distances,
                to_special_column=to_special_column,
                **kwargs
            )
            self._session.loc[
                pd.IndexSlice[index, speed.index.tolist()], "speed"
            ] = speed.values
        return self._session

    def vertical_speed(self, to_special_column=True, **kwargs):
        """
        Compute the vertical climbing speed (VAM) in meters over all the activities.

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
            `runpandas.Activity`: The runpandas.Activity with the new
             column vertical altitude speed computed.

        See Also
        --------
            runpandas.acessors.metrics.vertical_speed

        """
        for index in self._session.index.unique(level="start"):
            vam = self._session.xs(index, level=0).compute.vertical_speed(
                to_special_column=to_special_column, **kwargs
            )
            self._session.loc[
                pd.IndexSlice[index, vam.index.tolist()], "vam"
            ] = vam.values
        return self._session

    def gradient(self, to_special_column=True, **kwargs):
        """
        Compute the gradient ratio over all the activities.

        Parameters
        ----------
        to_special_column: convert the distance calculated (`pandas.Series`)
            to special runpandas Gradient column (`runpandas.types.columns.Gradient`).
            Default is True.

        **kwargs: Keyword args to be passed to the Gradient build method

        Returns
        -------
            `runpandas.Activity`: The runpandas.Activity with the new column gradient computed.

        See Also
        --------
            runpandas.acessors.metrics.gradient

        """
        for index in self._session.index.unique(level="start"):
            grad = self._session.xs(index, level=0).compute.gradient(
                to_special_column=to_special_column, **kwargs
            )
            self._session.loc[
                pd.IndexSlice[index, grad.index.tolist()], "grad"
            ] = grad.values
        return self._session

    def pace(self, to_special_column=True, **kwargs):
        """
        Compute the pace (the time that it takes to cover distances in your activities)
        over all the activities.

        Parameters
        ----------
        to_special_column: convert the pace calculated (`pandas.Series`)
            to special runpandas Pace column (`runpandas.types.columns.Pace`).
            Default is True.

        **kwargs: Keyword args to be passed to the Pace build method

        Returns
        -------
            `runpandas.Activity`: The runpandas.Activity with the new column pace computed.

        See Also
        --------
            runpandas.acessors.metrics.pace

        """
        for index in self._session.index.unique(level="start"):
            pace = self._session.xs(index, level=0).compute.pace(
                to_special_column=to_special_column, **kwargs
            )
            self._session.loc[
                pd.IndexSlice[index, pace.index.tolist()], "pace"
            ] = pace.values
        return self._session

    def heart_zone(self, bins, labels, **kwargs):
        """
        Compute the heart zone (with the training zone labels for each heart rate record)
        over all the activities.

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
            `runpandas.Activity`: The runpandas.Activity with the
                new column heart zone labels computed.

        See Also
        --------
            runpandas.acessors.metrics.heart_zone

        """
        for index in self._session.index.unique(level="start"):
            hr_zone = self._session.xs(index, level=0).compute.heart_zone(
                bins=bins, labels=labels, **kwargs
            )
            self._session.loc[
                pd.IndexSlice[index, hr_zone.index.tolist()], "hr_zone"
            ] = hr_zone.values
        return self._session

    def only_moving(self, threshold=0.8):
        """
        Impute the periods of inactivity, as such periods must be
        detected and ignored from the analysis for moving time, heart rate, speed, and
        power-based calculations for all the activities in the session.

        Parameters
        ----------
        threshold: float, default 0.8
            When the speed of a record drops below the threshold speed a 'false' event
            is set to the 'moving'column, and when the speed rises above the
            threshold speed a 'true' event is set to the 'moving' column.

        Returns
        -------
            `runpandas.Activity`: The runpandas.Activity with the column moving computed.

        See Also
        --------
            runpandas.acessors.moving._InactivityAssessor
        """
        for index in self._session.index.unique(level="start"):
            moving_series = self._session.xs(index, level=0).only_moving(
                threshold=threshold
            )["moving"]
            self._session.loc[
                pd.IndexSlice[index, moving_series.index.tolist()], "moving"
            ] = moving_series.values
        return self._session
