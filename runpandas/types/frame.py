"""
Root pandas accessors for DataFrames. It exposes the ActiviyData as DataFrames

"""

import pandas as pd

class Activity(pd.DataFrame):
    # properties to propagate
    _metadata = ['start']

    @property
    def _constructor(self):
        return self.__class__

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __finalize__(self, other, method=None, **kwargs):
        """Propagate metadata from other to self."""
        for name in self._metadata:
            object.__setattr__(self, name, getattr(other, name, None))
        return self