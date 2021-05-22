import numpy as np
from pandas import Series, to_timedelta
from runpandas._utils import series_property


class ColumnsRegistrator(type):
    """
    We keep a mapping of column used names to classes.
    """

    REGISTRY = {}

    def __new__(metacls, name, bases, namespace):
        new_cls = super().__new__(metacls, name, bases, namespace)
        # We register each concrete class
        if name != "MeasureSeries":
            metacls.REGISTRY[new_cls.colname] = new_cls

        return new_cls


class MeasureSeries(Series, metaclass=ColumnsRegistrator):
    _metadata = ["colname", "base_unit"]

    #
    # Implement pandas methods
    #

    @property
    def _constructor(self):
        return self.__class__

    @property
    def _constructor_expanddim(self):
        from runpandas.types import Activity

        return Activity

    def __init__(self, data, *args, **kwargs):
        super().__init__(data, *args, **kwargs)
        self._name = self.__class__.colname  # use *class* attribute

    def __finalize__(self, other, method=None, **kwargs):
        """Propagate metadata from other to self."""
        for name in self._metadata:
            object.__setattr__(self, name, getattr(other, name, None))
        return self


class Altitude(MeasureSeries):
    colname = "alt"
    base_unit = "m"

    @property
    def ascent(self):
        """
        Returns the ascent altitudes during the activity.
        """
        deltas = self.diff()
        return Altitude(np.where(deltas > 0, deltas, 0), index=self.index)

    @property
    def descent(self):
        """
        Returns the descent altitudes during the activity.
        """
        deltas = self.diff()
        return Altitude(np.where(deltas < 0, deltas, 0), index=self.index)

    @series_property
    def ft(self):
        """
        Returns the altitude from metres to feet
        """
        return self * 3.28084


class Cadence(MeasureSeries):
    colname = "cad"
    base_unit = "rpm"


class DistancePerPosition(MeasureSeries):
    colname = "distpos"
    base_unit = "m"

    def to_distance(self):
        """
        Returns the cummulative distance
        """
        return Distance._from_discrete(self)

    @series_property
    def km(self):
        """Returns the distance converted from metres to kilometres"""
        return self / 1000

    @series_property
    def miles(self):
        """Returns the distance converted from metres to miles"""
        return self / 1000 * 0.621371


class Distance(MeasureSeries):
    colname = "dist"
    base_unit = "m"

    @classmethod
    def _from_discrete(cls, data, *args, **kwargs):
        return cls(data.cumsum(), *args, **kwargs)

    @series_property
    def km(self):
        """Returns the distance converted from metres to kilometres"""
        return self / 1000

    @series_property
    def miles(self):
        """Returns the distance converted from metres to miles"""
        return self / 1000 * 0.621371


class HeartRate(MeasureSeries):
    colname = "hr"
    base_unit = "bpm"


class LonLat(MeasureSeries):
    colname = "lonlat"
    base_unit = "degrees"

    @classmethod
    def _from_semicircles_to_degrees(cls, data, *args, **kwargs):
        # https://github.com/kuperov/fit/blob/master/R/fit.R
        deg = (data * 180 / 2 ** 31 + 180) % 360 - 180
        return cls(deg, *args, **kwargs)

    @series_property
    def radians(self):
        """Returns the coordinates from degrees to radians"""
        return np.radians(self)


class Longitude(LonLat):
    colname = "lon"


class Latitude(LonLat):
    colname = "lat"


class Pace(MeasureSeries):
    colname = "pace"
    base_unit = "sec/m"

    @series_property
    def min_per_km(self):
        """
        Returns the pace converted from sec/m to min/km
        """
        return self * 1000

    @series_property
    def min_per_mile(self):
        """
        Returns the pace converted from sec/m to min/mile
        """
        return self * 1000 / 1.61


class Power(MeasureSeries):
    colname = "pwr"
    base_unit = "watts"


class Speed(MeasureSeries):
    colname = "speed"
    base_unit = "m/s"

    def to_pace(self):
        pace = to_timedelta(1 / self, unit="s")
        return Pace(pace)

    @series_property
    def kph(self):
        """
        Returns the speed converted from m/s to km/h
        """
        return self * 60 ** 2 / 1000

    @property
    def mph(self):
        """
        Returns the speed converted from m/s to miles/h
        """
        # self.kph is already a Series
        return self.kph / 1.61


class Temperature(MeasureSeries):
    colname = "temp"
    base_unit = "degrees_C"


class VAM(MeasureSeries):
    colname = "vam"
    base_unit = "m/s"


class Gradient(MeasureSeries):
    colname = "grad"
    base_unit = "fraction"

    _metadata = ["_rise", "_run"] + MeasureSeries._metadata

    def __init__(self, *args, rise=None, run=None, **kwargs):
        if rise is not None and run is not None:
            super().__init__(rise / run, *args, **kwargs)
            self._rise, self._run = rise.values, run.values
        else:
            super().__init__(*args, **kwargs)
            self._rise, self._run = None, None

    # support method to metadata setup
    def _set_attrs(self, **kwargs):
        for attr in self._metadata:
            if attr in kwargs:
                self.__setattr__(attr, kwargs.get(attr))

    @series_property
    def pct(self):
        """It converts the fraction to percent (%)"""
        return self * 100

    @series_property
    def radians(self):
        """It converts fraction to radians"""
        return np.arctan2(self._rise, self._run)

    @series_property
    def degrees(self):
        """It converts fraction to degrees"""
        return np.rad2deg(np.arctan2(self._rise, self._run))
