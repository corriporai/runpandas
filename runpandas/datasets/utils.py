"""Utility functions for loading example datasets"""

import os
from typing import List
from urllib.request import Request, urlopen, urlretrieve
from urllib.parse import urljoin
import yaml
from pydantic import parse_obj_as
from runpandas.datasets.schema import ActivityData, RaceData, EventData
from thefuzz import fuzz

ACTIVITIES_INDEX = (
    "https://raw.githubusercontent.com/"
    "corriporai/runpandas-data/master/activities/index.yml"
)

RACES_INDEX = (
    "https://raw.githubusercontent.com/"
    "corriporai/runpandas-data/master/races/index.yml"
)


def _get_event_index(index=RACES_INDEX):
    """
    Race results available for data analytics.
    Requires an internet connection.
    """
    req = Request(index)
    with urlopen(req) as resp:  # nosec
        content = resp.read()
        raw_index = yaml.safe_load(content)

    loaded_data = parse_obj_as(List[RaceData], raw_index)
    return loaded_data


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


def get_events(identifier, year=None, run_type=None, config=None):
    """
    Return the event results (i.e. races) from the online repository (requires internet).

    ..warning:: A fuzzy match is performed to find the event that best matches the
    given identifier. Fuzzy matching is performed using the summary metadata from
    the event. This is not guaranteed to return the correct result.
    You should therefore always check if the function actually returns the event
    you had wanted.

    Use :func:`_get_event_index` to see a list of available datasets.

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
    result_set : A list of :class:`schema.EventData` instances.

    """

    def __string_search(events, search_name):
        match_result = []
        for event in events:
            # first try to match the identifier with the path
            if os.path.basename(event.path) == search_name:
                match_result.append(event)
        return match_result

    def __identifier_search(events, search_name):
        match_result = []
        # try using the fuzzy match the identifier against the summary
        for event in events:
            ratio = fuzz.token_set_ratio(
                search_name.casefold(), event.summary.casefold()
            )
            if ratio > 90:
                match_result.append(event)
        return match_result

    events = _get_event_index()
    match_result = __string_search(events, identifier) or __identifier_search(
        events, identifier
    )
    result_set = []
    if len(match_result) != 0:
        for match in match_result:
            cache_path = os.path.join(
                _get_cache_path(config), os.path.basename(match.path)
            )
            if not os.path.exists(cache_path):
                os.makedirs(cache_path)
            for edition in match.editions:
                url_path = urljoin(
                    match.path + "/",
                    "{path}_{edition}.csv".format(
                        path=os.path.basename(match.path), edition=edition
                    ),
                )
                event_cache_path = os.path.join(cache_path, os.path.basename(url_path))
                if not os.path.exists(event_cache_path):
                    urlretrieve(url_path, event_cache_path)  # nosec

                edition = EventData(
                    summary=match.summary,
                    path=event_cache_path,
                    run_type=match.run_type,
                    country=match.country,
                    included_data=match.included_data,
                    edition=edition,
                )
                result_set.append(edition)

    if year is not None:
        result_set = filter(lambda event: str(event.edition) == str(year), result_set)
    if run_type is not None:
        result_set = filter(
            lambda event: str(event.run_type) == str(run_type), result_set
        )

    return result_set
