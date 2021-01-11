from runpandas.reader import _read_file as read_file  # noqa
from runpandas.reader import _read_dir as read_dir  # noqa
from runpandas.io.strava._parser import read_strava  # noqa


from ._version import get_versions

__version__ = get_versions()["version"]
del get_versions

__all__ = ["__version__", "read_file", "read_dir", "read_strava"]
