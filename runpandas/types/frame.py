"""
Root pandas accessors for DataFrames. It exposes the ActiviyData as DataFrames

"""
import warnings

import numpy as np
import pandas as pd
import runpandas.reader
from pandas.core.frame import DataFrame
from runpandas.types import columns


class Activity(pd.DataFrame):
    """
    An Activity object is a pandas.DataFrame that provides useful
    methods and has specific columns with special functionalities.
    In addition to the standard DataFrame constructor arguments,
    Activity also accepts the following optional arguments:

    Parameters
    ----------
    cspecs : dict of series (optional)
        Column Specifications (cspecs) of the ``Activity``
    start : str, datetime (optional)
        Start timestamp of the ``Activity``
    """

    # properties to propagate
    _metadata = ["start"]

    def __init__(self, *args, **kwargs):
        cspecs = kwargs.pop("cspecs", None)
        start = kwargs.pop("start", None)

        super().__init__(*args, **kwargs)

        if cspecs is not None:
            self.set_specs(cspecs, inplace=True)
        if start is not None:
            self.start = start

    def set_specs(self, cspecs=None, inplace=False):
        """
        Set the Column Specifications (cspecs) of the ``Activity``.
        Set the specifed column on Activity.

        Parameters
        ----------
        cspecs : dict of series
        inplace : bool, default False
            If True, the cspecs of the Activity will be changed in place
            (while still returning the result) instead of making a copy of
            the Activity.
        """
        if not inplace:
            df = self.copy()
        else:
            df = self
        for old_key, column_cls in cspecs.items():
            try:
                old_column = df.pop(old_key)  # no default
            except KeyError:
                warnings.warn("The specified key %s not found." % old_key, UserWarning)
                continue

            new = column_cls(old_column)
            df[new.colname] = new
        if not inplace:
            return df

    @property
    def _constructor(self):
        return Activity

    def to_pandas(self):
        """
        Returns:
            Casted Pandas Dataframe from Activity
        """
        return DataFrame(self)

    def __finalize__(self, other, method=None, **kwargs):
        """Propagate metadata from other to self."""
        for name in self._metadata:
            object.__setattr__(self, name, getattr(other, name, None))
        return self

    def __getitem__(self, key):
        """
        If the result is a column containing only activity measures, return a
        MeasuredSeries. If it's a DataFrame with a 'Measures' column, return a
        Activity.
        """
        result = super(Activity, self).__getitem__(key)

        if isinstance(key, str) and key in columns.ColumnsRegistrator.REGISTRY:
            result.__class__ = columns.ColumnsRegistrator.REGISTRY[key]
        elif isinstance(result, pd.DataFrame):
            result.__class__ = Activity

        if isinstance(result, columns.Gradient):
            result._set_attrs(
                _rise=self["alt"].diff().values, _run=self["dist"].diff().values
            )

        return result

    @classmethod
    def from_file(cls, file_path, **kwargs):
        """
        Alternate constructor to create a ``Activity`` from a file.

        It is recommended to use :func:`runpandas.reader._read_file` instead.

        Parameters
        ----------
        file_path : str
            File path or file handle to read from. Depending on which kwargs
            are included, the content of filename may vary.
        kwargs : key-word arguments
            These arguments are passed to reader._read_file
        """
        return runpandas.reader._read_file(file_path)

    @property
    def ellapsed_time(self):
        """
        Returns:
            The duration of activity in `pandas.TimedeltaIndex` object.

        Raises:
            AttributeError if dataframe index is not an instance of TimedeltaIndex

        """
        if isinstance(self.index, pd.TimedeltaIndex):
            return self.index[-1]
        raise AttributeError("index is not TimedeltaIndex")

    @property
    def moving_time(self):
        """
        Returns:
            The moving time of activity in `pandas.TimedeltaIndex` object.
            It measures only the periods that you were active based on
            internal calculations.

        Raises:
            AttributeError if dataframe index is not an instance of TimedeltaIndex
            or the `moving` column is not found computed from
            `runpandas.acessors.moving.only_moving` acessor.

        """
        if not isinstance(self.index, pd.TimedeltaIndex):
            raise AttributeError("index is not TimedeltaIndex")
        if "moving" not in self.columns:
            raise AttributeError("moving column not found in activity.")

        total_time = (
            self.index.to_series().diff().fillna(self.index[0])
        ) / np.timedelta64(1, "s")
        merged_df = total_time.to_frame().join(self["moving"].to_frame())
        return pd.Timedelta(
            seconds=total_time.sum()
            - merged_df[~merged_df["moving"].astype(bool)]["time"].sum()
        )

    @property
    def distance(self):
        """
        Returns:
            The total distance of the activity in meters as a float number.
        """
        try:
            return self["dist"].max()
        except KeyError:
            return self["distpos"].sum()

    def mean_speed(self, only_moving=False, smoothing=True):
        """
        It calculates the average speed based on the speed trace.

        Parameters
        ----------
        only_moving : boolean, optional. It considers only the active moviment of the activity.
        Default is False.

        smoothing: boolean, optional. If True, it calculates average speed based on total
        distance divided by total time. Default is True.

        Returns:
        --------
            The average speed in meters/second for the activity.
        """
        if "speed" not in self.columns:
            raise AttributeError("speed column not found in activity.")

        if only_moving:
            total_time = self.moving_time
            activity = self[self["moving"]]
        else:
            total_time = self.ellapsed_time
            activity = self

        if smoothing:
            time_diff = (
                self.index.to_series().diff().fillna(self.index[0])
            ) / np.timedelta64(1, "s")
            total_distance = (activity["speed"] * time_diff).sum()
        else:
            total_distance = activity.distance

        return total_distance / total_time.total_seconds()

    def mean_pace(self, only_moving=False, smoothing=True):
        """
        It calculates the average pace based on the speed trace.

        Parameters
        ----------
        only_moving : boolean, optional. It considers only the active moviment of the activity.
        Default is False.

        smoothing: boolean, optional. If True, it calculates average pace based on total
        distance divided by total time. Default is True.

        Returns:
        --------
            The average pace in sec/m for the activity.
        """
        speed = self.mean_speed(only_moving, smoothing)
        return pd.Timedelta(seconds=1 / speed)

    def mean_heart_rate(self, only_moving=False):
        """
        It calculates the average heart rate based on the heart rate tracked
        by HeartRate Series column.

        Parameters
        ----------
        only_moving : boolean, optional. It considers only the active moviment of the activity.
        Default is False.

        Returns:
        --------
            The average heart zone in bpm for the activity.
        """
        if "hr" not in self.columns:
            raise AttributeError("heart rate column not found in activity.")

        if only_moving:
            activity = self[self["moving"]]
        else:
            activity = self

        return activity["hr"].mean()

    def mean_cadence(self, only_moving=False):
        """
        It calculates the average cadence based on the cadence tracked
        by Cadence Series column.

        Parameters
        ----------
        only_moving : boolean, optional. It considers only the active moviment of the activity.
        Default is False.

        Returns:
        --------
            The average cadence in rotation per minute (rpm) for the activity.
        """
        if "cad" not in self.columns:
            raise AttributeError("Cadence column not found in activity.")

        if only_moving:
            activity = self[self["moving"]]
        else:
            activity = self

        return activity["cad"].mean()

    def summary(self):
        """
        Display the common basic statistics for the activity.

        Returns:
        --------
            pandas.Dataframe:  A pandas DataFrame containing the summary statistics, which
            inclues estimates of the total distance covered, the total duration,
            the time spent moving, and many others.

        """
        return runpandas.types.summary.activity_summary(self)
