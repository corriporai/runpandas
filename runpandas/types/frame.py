"""
Root pandas accessors for DataFrames. It exposes the ActiviyData as DataFrames

"""
import warnings

import pandas as pd
from pandas.core.frame import DataFrame

class Activity(pd.DataFrame):
    # properties to propagate
    _metadata = ['start']

    def __init__(self, *args, **kwargs):
        cspecs = kwargs.pop("cspecs", None)
        start = kwargs.pop("start", None)

        super(Activity, self).__init__(*args, **kwargs)

        if cspecs is not None:
            self.set_specs(cspecs, inplace=True)
        if start is not  None:
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
                warnings.warn('The specified key %s not found.' % old_key, UserWarning)
                continue

            new = column_cls(old_column)
            df[new.colname] = new
        if not  inplace:
            return df

    @property
    def _constructor(self):
        return self.__class__

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
