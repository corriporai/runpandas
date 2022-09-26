"""Schema Models for loading example datasets"""

from enum import Enum
from pathlib import Path
from typing import List

from pydantic import BaseModel, validator


class MetricsEnum(Enum):
    latitude = "latitude"
    longitude = "longitude"
    speed = "speed"
    power = "power"
    elevation = "elevation"
    cadence = "cadence"
    heartrate = "heartrate"
    temperature = "temperature"
    distance = "distance"


class Sensor(BaseModel):
    name: str
    data_types: List[MetricsEnum]


class FileTypeEnum(str, Enum):
    FIT = "FIT"
    TCX = "TCX"
    GPX = "GPX"


class ActivityData(BaseModel):

    summary: str = None
    path: Path
    file_type: FileTypeEnum
    recording_device: str
    sensors: List[Sensor] = None
    included_data: List[MetricsEnum]
    laps: int = None
    sessions: int = None

    @validator("path")
    @classmethod
    def make_cached_path(cls, v):
        path = (
            "https://raw.githubusercontent.com/"
            "corriporai/runpandas-data/master/activities/{}"
        )
        return path.format(v)


class RunTypeEnum(str, Enum):
    MARATHON = "marathon"
    HALF_MARATHON = "half"
    TEN_KM = "10km"
    FIVE_KM = "5km"
    ULTRA = "ultra"


class RaceAttributeEnum(Enum):
    position = "position"
    bib = "bib"
    firstname = "firstname"
    lastname = "lastname"
    category = "category"
    nettime = "nettime"
    grosstime = "grosstime"
    sex = "sex"


class EventData(BaseModel):
    summary: str = None
    path: Path
    run_type: RunTypeEnum
    country: str
    included_data: List[RaceAttributeEnum]
    edition: str

    def load(self):
        from runpandas.io.result._parser import read

        return read(self.path)


class RaceData(BaseModel):

    summary: str = None
    path: Path
    run_type: RunTypeEnum
    country: str
    included_data: List[RaceAttributeEnum]
    editions: List[str] = None
    sessions: int = None

    @validator("path")
    @classmethod
    def make_cached_path(cls, v):
        path = (
            "https://raw.githubusercontent.com/"
            "corriporai/runpandas-data/master/races/{}"
        )
        return path.format(v)
