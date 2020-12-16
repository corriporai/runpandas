from runpandas.reader import _read_file as read_file  # noqa
from runpandas.io.strava import read_strava # noqa

from ._version import get_versions

__version__ = get_versions()["version"]
del get_versions

__all__ = [
    "__version__",
]
