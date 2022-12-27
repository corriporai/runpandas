"""
Module contains reading logic for several formats of training sources
"""

from pathlib import Path
import pandas as pd
from runpandas import datasets
from runpandas import _utils as utils
from runpandas import exceptions

MODULE_CACHE = {}


def _read_file(filename, to_df=False, **kwargs):
    """
    Parameters
    ----------
        filename : str, The path to a training file.
        to_df : bool, optional
             Return a obj:`runpandas.Activity` if `to_df=True`, otherwise
             a :obj:`pandas.DataFrame` will be returned. Defaults to False.
        **kwargs :
        Keyword args to be passed to the `read` method accordingly to the
        file format.

    Returns
    -------
    Return a obj:`runpandas.Activity` if `to_df=True`, otherwise
             a :obj:`pandas.DataFrame` will be returned.

    """

    if not utils.file_exists(filename):
        raise IOError("%s does not exist" % filename)
    if not utils.is_valid(filename):
        raise exceptions.InvalidFileError(
            "File {filename} with invalid filetype.".format(**locals())
        )
    _, ext = utils.splitext_plus(filename)
    module = _import_module(ext[1:])
    return module.read(filename, to_df, **kwargs)


def _import_module(mod_name):
    """Find custom reading module to execute"""
    mod = MODULE_CACHE.get(mod_name, None)
    if mod is None:
        try:
            MODULE_CACHE[mod_name] = __import__(
                "runpandas.io.%s" % mod_name, fromlist=["runpandas", "io"]
            )
        except ImportError:
            raise ImportError("%s is not a support file type." % mod_name)
        else:
            mod = MODULE_CACHE.get(mod_name)
    return mod


def _read_dir(dirname, to_df=False, **kwargs):
    """

    Parameters
    ----------
        dirname : str, The path to a directory with training files.
        to_df : bool, optional
             Return a obj:`runpandas.Activity` if `to_df=True`, otherwise
             a :obj:`pandas.DataFrame` will be returned. Defaults to False.
        **kwargs : Keyword args to be passed to the `read_dir` method

    Returns
    -------
    Return a list of obj:`runpandas.Activity` if `to_df=True`, otherwise
             a :obj:`pandas.DataFrame` will be returned.

    """
    path_dir = Path(dirname)

    assert path_dir.is_dir()

    for path_file in path_dir.iterdir():
        if path_file.is_dir():
            continue

        yield _read_file(filename=path_file, to_df=to_df, kwargs=kwargs)


def _read_dir_aggregate(dirname, **kwargs):
    """
    Read all supported container files from a supplied directory
    as `runpandas.Activity` dataframes, and aggregate them
    to the same session as a `pandas.MultiIndex` activity dataframe.

    Parameters
    ----------
        dirname : str, The path to a directory with training files.
             Return a obj:`runpandas.Activity` if `to_df=True`, otherwise
             a :obj:`pandas.DataFrame` will be returned. Defaults to False.
        **kwargs : Keyword args to be passed to the `read_dir` method

    Returns
    -------
    Return a  :obj:`runpandas.Activity` split into sessions based
    on the `pandas.MultiIndex` with the date/time of the activity
    as first level and the second the timestamps for each record.
    """
    activities = []
    activity_keys = []
    for activity in _read_dir(dirname=dirname, to_df=False, **kwargs):
        activities.append(activity)
        activity_keys.append(activity.start)
    if len(activities) > 0:
        multi_frame = pd.concat(
            activities, keys=activity_keys, names=["start", "time"], axis=0
        )
        return multi_frame

    return None


def _read_event_result(filename, to_df=False, **kwargs):
    """
    Parameters
    ----------
        filename : str, The path to a result file.
        to_df : bool, optional
             Return a obj:`runpandas.RaceResult` if `to_df=False`, otherwise
             a :obj:`pandas.DataFrame` will be returned. Defaults to False.
        **kwargs : Keyword args to be passed to the `read` method accordingly \
            to the file format.

    Returns
    -------
    Return a obj:`runpandas.RaceResult` if `to_df=False`, otherwise
             a :obj:`pandas.DataFrame` will be returned.

    """
    if not utils.file_exists(filename):
        raise IOError("%s does not exist" % filename)

    _, ext = utils.splitext_plus(filename)
    if ext not in [".csv"]:
        raise exceptions.InvalidFileError(
            "File {filename} with invalid filetype.".format(**locals())
        )
    module = _import_module("result")
    return module.read(filename, to_df, **kwargs)


def get_events(identifier, year=None, run_type=None, config=None):
    """
    Returns event results based on year or event name identifier.
    The result will be a list of :obj:`runpandas.RaceResult` instances that macthes
    the given criteria.

    Parameters
    ----------
    identifier : str
        Name of the event or any identifier related to it.
    year: str, optional
        Iterates over all the events with identificer match and
        with the given year and return them.
    run_type: str, optional
        Iterates over all the events with identificer match and
        with the given run type and return them.
    config : yaml file, optional
        The directory in which to cache data; see :func:`get_cache_path`.

    Returns
    -------
    Return a list of :obj:`runpandas.RaceResult` based on the identifier,
    run typer or year criteria.
    """
    events = datasets.utils.get_events(identifier, year, run_type, config)
    return events
