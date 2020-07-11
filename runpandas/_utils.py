"""Helpful utilities for runpandas modules.
"""
import os
from xml.etree.cElementTree import iterparse
from xml.etree.ElementTree import Element


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

def recursive_text_extract(node):
    return {sans_ns(child.tag): child.text for child in node.iter()
            if child.text is not None and child.text.strip()}

def sans_ns(tag):
    """Remove the namespace prefix from a tag."""
    return tag.split('}')[-1]


def get_nodes(file_path, node_names, *, with_root=False):
    """ Parse XML document and iterate over specific nodes

    Parameters
    ----------
    filepath : str
        Path to the file to be read.
    node_names : str
        List of nodes to be extracted.
    with_root: boolean
        Default to False. If True returns the root node.

    Returns
    -------
    Used as a generator for yielding the nodes.
    """
    context = iter(iterparse(file_path, events=('start', 'end')))
    event, root = next(context)

    if with_root:
        yield with_root

    for event, element in context:
        if event == 'end' and sans_ns(element.tag) in node_names:
            yield element
            root.clear()
