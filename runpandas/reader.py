"""
Module contains reading logic for several formats of training sources
"""

from pandas import DataFrame
from runpandas import _utils as utils

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

    if not utils.file_exists(filename) or not utils.is_valid(filename):
        raise IOError("%s does not exist or it is not a valid file for activities files."
                    "It only supports tcx files." % filename)
    _, ext = utils.splitext_plus(filename)
    module  = _import_module(ext[1:])
    if not to_df:
        return module.read(filename, **kwargs)
    else:
        return DataFrame.from_records(module.gen_records(filename))

def _import_module(mod_name):
    """ Find custom reading module to execute
    """
    mod =  MODULE_CACHE.get(mod_name, None)
    if mod is None:
        try:
            MODULE_CACHE[mod_name] = __import__("runpandas.io.%s" % mod_name,
                fromlist=["runpandas", "io"])
        except ImportError:
            raise ImportError("%s is not a support file type." % mod_name)
        else:
            mod = MODULE_CACHE.get(mod_name)
    return mod