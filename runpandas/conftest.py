import os

import pytest


@pytest.fixture
def datapath(request):
    """Get the path to a data file.
    Parameters
    ----------
    path : str
        Path to the file, relative to ``runpandas/tests/``
    Returns
    -------
    path : path including ``runpandas/tests``.
    Raises
    ------
    ValueError
        If the path doesn't exist and the --strict-data-files option is set.
    """
    BASE_PATH = os.path.join(os.path.dirname(__file__), "tests")

    def wrapper(*args):
        path = os.path.join(BASE_PATH, *args)
        if not os.path.exists(path):
            if request.config.getoption("--strict-data-files"):
                msg = "Could not find file {} and --strict-data-files is set."
                raise ValueError(msg.format(path))

            msg = "Could not find {}."
            pytest.skip(msg.format(path))
        return path

    return wrapper
