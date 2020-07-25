'''
Tools for parsing Garmin TCX files.
'''
import pandas as pd
from runpandas import _utils as utils
from runpandas import exceptions
from runpandas.types import Activity

def gen_records(file_path):
    nodes = utils.get_nodes(file_path, ('Trackpoint',), with_root=True)
    root = next(nodes)
    if utils.sans_ns(root.tag) != 'TrainingCenterDatabase':
        raise exceptions.InvalidFileError('tcx')

    trackpoints = nodes
    for trkpt in trackpoints:
        yield utils.recursive_text_extract(trkpt)

def read(file_path):
    data = Activity.from_records(gen_records(file_path))
    #print (next(gen_records(file_path)))
    #data = pd.DataFrame.from_records()
    return data