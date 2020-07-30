from pandas import Series

class Field(Series):
    _metadata = ['colname', 'base_unit']

    @property
    def _constructor(self):
        return self.__class__

    def __init__(self, data, *args, **kwargs):
        super().__init__(data, *args, **kwargs)
        self._name = self.__class__.colname     # use *class* attribute

    def __finalize__(self, other, method=None, **kwargs):
        """Propagate metadata from other to self."""
        for name in self._metadata:
            object.__setattr__(self, name, getattr(other, name, None))
        return self

class Altitude(Field):
    colname = 'alt'
    base_unit = 'm'

class Cadence(Field):
    colname = 'cad'
    base_unit = 'rpm'

class Distance(Field):
    colname = 'dist'
    base_unit = 'm'

class HeartRate(Field):
    colname = 'hr'
    base_unit = 'bpm'

class LonLat(Field):
    colname = 'lonlat'
    base_unit = 'degrees'

class Longitude(LonLat):
    colname = 'lon'

class Latitude(LonLat):
    colname = 'lat'

class Pace(Field):
    colname = 'pace'
    base_unit = 'sec/m'

class Power(Field):
    colname = 'pwr'
    base_unit = 'watts'

class Speed(Field):
    colname = 'speed'
    base_unit = 'm/s'
