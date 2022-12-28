"""
This is a module for extending pandas race results with splits methods
"""


import pandas as pd
from runpandas.types import RaceResult


@pd.api.extensions.register_dataframe_accessor("splits")
class _RaceSplitsAcessor(object):
    """
    Dataframe Accessor to fetch the race splits available from the athletes'
    results.
    """

    SPLITS = ["5k", "10k", "15k", "20k", "half", "25k", "30k", "35k", "40k", "nettime"]

    def __init__(self, race_result):
        self._race_result = None
        if isinstance(race_result, RaceResult):
            self._validate(race_result)
            self._race_result = race_result

    @staticmethod
    def _validate(race_result):
        assert isinstance(
            race_result, RaceResult
        ), "RaceResult is needed for this accessor"

    def pick_athlete(self, identifier, by="BIB"):
        """Return all splits of a specific athlete in RaceResult
        based on the athelete's BIB number or based on the race position.

        Parameters
        ----------

        identifier: Athtlete bib identification or race final position.

        by: Use identifier as bib identification (BIB) or race position (POS). Default is BIB.

        Returns
        -------
        `pandas.Dataframe`: A pandas dataframe containing the athlete race splits
                                (partial times and distances covered)
        """
        _RaceSplitsAcessor._validate(self._race_result)
        assert by in ("BIB", "POS"), "by parameter must be BIB or POS."
        assert self._race_result.event.event_type in (
            "42k"
        ), "Until now, it only supports marathon splits race data."
        by_translated = "bib" if by == "BIB" else "position"

        # create ranking columns

        # filter the race data given the identifier
        race_data = self._race_result[self._race_result[by_translated] == identifier]

        if race_data.empty:
            raise ValueError(
                "Identifier %s %s not found in the RaceResult set."
                % (by_translated, identifier)
            )

        # filter only the split columns
        race_data = race_data.loc[:, race_data.columns.isin(_RaceSplitsAcessor.SPLITS)]
        # Add 0km
        race_data["0k"] = pd.to_timedelta("0:00:00")
        # Transpose table
        race_data = race_data.T
        race_data = race_data.rename(columns={0: "time"})
        race_data.index.names = ["split"]
        # Add distance in meters
        distance_frame = pd.DataFrame.from_dict(
            {
                "0k": 0,
                "5k": 5000,
                "10k": 10000,
                "15k": 15000,
                "20k": 20000,
                "25k": 25000,
                "30k": 30000,
                "35k": 35000,
                "40k": 40000,
                "nettime": 42195,
                "half": 21097,
            },
            orient="index",
            columns=["distance_meters"],
        )
        race_data = race_data.join(distance_frame)

        race_data["distance_miles"] = (
            race_data["distance_meters"].apply(lambda x: x * 0.000621371).round(4)
        )

        # Set the correct index and order it.
        full_index = ["0k"] + _RaceSplitsAcessor.SPLITS
        reorder_index = [idx for idx in full_index if idx in race_data.index.tolist()]
        race_data = race_data.reindex(reorder_index)

        return race_data
