"""
Root pandas accessors for DataFrames. It exposes the ActiviyData as DataFrames

"""
import warnings

import pandas as pd
from pandas.core.frame import DataFrame
import runpandas.reader
from runpandas.types import columns


class Activity(pd.DataFrame):
    """
    An Activity object is a pandas.DataFrame that provides useful
    methods and has specific columns with special functionalities.
    In addition to the standard DataFrame constructor arguments,
    GeoDataFrame also accepts the following optional arguments:

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

        return result

    @classmethod
    def from_file(cls, file_path, **kwargs):
        """
        Alternate constructor to create a ``Activity`` from a file.

        Parameters
        ----------
        file : str
            File path or file handle to read from. Depending on which kwargs
            are included, the content of filename may vary.
        kwargs : key-word arguments
        """
        return runpandas.reader._read_file(file_path)
