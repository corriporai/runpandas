"""Helpful utilities for runpandas modules.
"""
import os

def file_exists(fname):
    """Check if a file exists and is non-empty.
    """
    try:
        return fname and os.path.exists(fname) and os.path.getsize(fname) > 0
    except OSError:
        return False

def splitext_plus(fname):
    """Split on file extensions, allowing for zipped extensions.
    """
    base, ext = os.path.splitext(fname)
    if ext in [".gz", ".bz2", ".zip"]:
        base, ext2 = os.path.splitext(base)
        ext = ext2 + ext
    return base, ext

def is_valid(fname):
    """Check if it is a valid format for activity files.

    Parameters
    ----------
    fname : str
        Path to the file to be read.

    Returns
    -------
    It returns True if the it is a valid format for activities handling.
    """
    _, ext = os.path.splitext(fname)
    return ext in [".tcx"]