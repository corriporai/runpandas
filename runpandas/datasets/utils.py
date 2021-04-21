"""Utility functions for loading example datasets"""

import os
import yaml
from typing import List

from urllib.request import urlopen, urlretrieve, Request
from pydantic import parse_obj_as
from runpandas.datasets.schema import ActivityData

ACTIVITIES_INDEX = (
    "https://raw.githubusercontent.com/"
    "corriporai/runpandas-data/master/activities/index.yml"
)


def _get_activity_index(index=ACTIVITIES_INDEX):
    """Report available example activities.
    Requires an internet connection.
    """
    req = Request(index)
    with urlopen(req) as resp:  # nosec
        content = resp.read()
        raw_index = yaml.safe_load(content)

    loaded_data = parse_obj_as(List[ActivityData], raw_index)

    return loaded_data


def _get_config_data(config_path=None):
    if config_path is None:
        config_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "config.yaml"
        )
    with open(config_path, "r") as f:
        config = yaml.safe_load(f.read())
    return config


def _get_cache_path(config=None):
    """Return a path to the cache directory for example datasets.
    This directory is then used by :func:`load_activity`.
    If the ``config`` file is not specified, it tries to read the target dir
    from the ``config.yaml` file.
    """
    op = os.path
    config = _get_config_data(config)
    data_home = op.abspath(op.expanduser(op.expandvars(config["path"]["root"])))

    if not os.path.exists(data_home):
        os.makedirs(data_home)
    return data_home


def activity_examples(path=None, file_type=None, config=None, **kwargs):
    """Load an example activity from the online repository (requires internet).

    This function provides quick access to a small number of example datasets
    that are useful for documenting runpandas or generating reproducible examples
    for tests. It is not necessary for normal usage.

    Use :func:`_get_activity_index` to see a list of available datasets.

    Parameters
    ----------
    name : str, optional
        Name of the dataset (``path`` on
        https://github.com/corriporai/runpandas-data/activities/).
    file_type: str
        Iterates over all files with the given file type and return them.
    config : yaml file, optional
        The directory in which to cache data; see :func:`get_cache_path`.
    kwargs : keys and values, optional
        Additional keyword arguments are passed to passed through to
        :func:`runpandas.read_file`.
    Returns
    -------
    loaded_data : a single or a list of :class:`schema.ActivityData` instances.

    """
    activities = _get_activity_index()
    if path is not None:
        for activity in activities:
            if os.path.basename(activity.path) == path:
                cache_path = os.path.join(
                    _get_cache_path(config), os.path.basename(path)
                )
                if not os.path.exists(cache_path):
                    urlretrieve(activity.path, cache_path)  # nosec
                activity.path = cache_path
                return activity
        raise ValueError(f"'{path}' is not one of the example datasets.")

    if file_type is not None:
        activities = filter(
            lambda file: file.file_type == file_type, activity_examples()
        )

    return activities
