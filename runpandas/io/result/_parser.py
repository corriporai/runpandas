"""
Tools for parsing csv Race Result files.
"""
from datetime import datetime
import pandas as pd
from runpandas import _utils as utils
from runpandas import exceptions
from runpandas.types.frame import RaceResult, Event

COL_TYPES = {
    "position": {"alias": ["position", "coloc"], "apply": lambda x, errors: str(x)},
    "bib": {"alias": ["bib", "num"], "apply": lambda x, errors: str(x)},
    "name": {"alias": ["name", "nome"], "apply": lambda x, errors: str(x)},
    "age": {"alias": ["age", "idade"], "apply": lambda x, errors: int(x)},
    "sex": {"alias": ["sexo", "sex", "m/f"], "apply": lambda x, errors: str(x)},
    "nettime": {
        "alias": ["official_time", "chiptime", "liquido"],
        "apply": pd.to_timedelta,
    },
    "grosstime": {"alias": ["tempo", "guntime"], "apply": pd.to_timedelta},
    "half": {"alias": ["halftime", "half"], "apply": pd.to_timedelta},
    "5k": {"alias": ["5_k"], "apply": pd.to_timedelta},
    "10k": {"alias": ["10_k"], "apply": pd.to_timedelta},
    "15k": {"alias": ["15_k"], "apply": pd.to_timedelta},
    "20k": {"alias": ["20_k"], "apply": pd.to_timedelta},
    "25k": {"alias": ["25_k"], "apply": pd.to_timedelta},
    "30k": {"alias": ["30_k"], "apply": pd.to_timedelta},
    "35k": {"alias": ["35_k"], "apply": pd.to_timedelta},
    "40k": {"alias": ["40_k"], "apply": pd.to_timedelta},
    "pace": {"alias": ["pace"], "apply": pd.to_timedelta},
}


def __extract_metadata(file_path):
    """
    Extract the metadata from the result file and returns the race metadata.

    Parameters
    ----------
        file_path : str, The path to a race result file.

    Returns
    -------
    Return a obj:`runpandas.RaceResult` if `to_df=False`, otherwise
             a :obj:`pandas.DataFrame` will be returned.
    """
    data = pd.read_csv(file_path, index_col=0, nrows=0).columns.tolist()
    parsed_metadata = {}

    try:
        parsed_metadata["name"] = data[0]
        parsed_metadata["race_date"] = datetime.strptime(data[1], "%d/%m/%Y")
        parsed_metadata["run_type"] = data[2]
        parsed_metadata["country"] = data[3]
    except IndexError:
        raise exceptions.MissingHeaderError(file_path)
    except ValueError:
        raise exceptions.InvalidHeaderError(file_path)

    return parsed_metadata


def read(file_path, to_df=False, **kwargs):
    """
    This method loads a race result file into a Pandas DataFrame or runpandas Race Result.
    Column names are translated to runpandas terminology
    (e.g. "bib number" > "bib_number").

    Parameters
    ----------
        filename : str, The path to a race result file.
        to_df : bool, optional
             Return a obj:`runpandas.RaceResult` if `to_df=False`, otherwise
             a :obj:`pandas.DataFrame` will be returned. Defaults to False.
        **kwargs :
        Keyword args to be passed to the `read` method accordingly to the
        file format.
    Returns
    -------
    Return a obj:`runpandas.RaceResult` if `to_df=False`, otherwise
             a :obj:`pandas.DataFrame` will be returned.
    """

    metadata = __extract_metadata(file_path)

    data = pd.read_csv(file_path, skiprows=1, **kwargs)

    data.columns = map(utils.camelcase_to_snakecase, data.columns)
    data.columns = data.columns.str.replace(" ", "")

    to_rename = {}
    # transform data to specific dtypes
    for col, _type in COL_TYPES.items():
        for alias in COL_TYPES[col]["alias"]:
            if alias in data.columns:
                to_rename[alias] = col
                data[alias] = data[alias].apply(
                    COL_TYPES[col]["apply"], errors="coerce"
                )

    if to_rename:
        data.rename(columns=to_rename, inplace=True)

    data.dropna(axis=1, how="all", inplace=True)

    if to_df:
        return data

    event = Event(
        event_name=metadata["name"],
        event_type=metadata["run_type"],
        event_country=metadata["country"],
        event_date=metadata["race_date"],
    )

    return RaceResult(data, event=event)
