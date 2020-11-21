from pandas import Series


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


class Cadence(MeasureSeries):
    colname = "cad"
    base_unit = "rpm"


class Distance(MeasureSeries):
    colname = "dist"
    base_unit = "m"


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


class Longitude(LonLat):
    colname = "lon"


class Latitude(LonLat):
    colname = "lat"


class Pace(MeasureSeries):
    colname = "pace"
    base_unit = "sec/m"


class Power(MeasureSeries):
    colname = "pwr"
    base_unit = "watts"


class Speed(MeasureSeries):
    colname = "speed"
    base_unit = "m/s"


class Temperature(MeasureSeries):
    colname = "temp"
    base_unit = "degrees_C"
