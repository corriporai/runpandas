from runpandas.reader import _read_file as read_file  # noqa
from runpandas.reader import _read_dir as read_dir  # noqa
from runpandas.reader import _read_dir_aggregate as read_dir_aggregate  # noqa
from runpandas.io.strava._parser import read_strava  # noqa
from runpandas.io.strava._client import StravaClient  # noqa
from runpandas.io.nikerun._parser import read_nikerun  # noqa
from runpandas.io.nikerun._parser import read_dir_nikerun  # noqa
from runpandas.datasets.utils import activity_examples  # noqa
from runpandas.datasets.schema import FileTypeEnum  # noqa

from ._version import get_versions

__version__ = get_versions()["version"]
del get_versions

__all__ = [
    "__version__",
    "read_file",
    "read_dir",
    "read_dir_aggregate",
    "read_strava",
    "StravaClient",
    "read_nikerun",
    "read_dir_nikerun",
    "activity_examples",
]
