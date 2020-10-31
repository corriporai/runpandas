from ._version import get_versions
from runpandas.reader import _read_file as read_file  # noqa

__version__ = get_versions()["version"]
del get_versions

__all__ = [
    "__version__",
]
