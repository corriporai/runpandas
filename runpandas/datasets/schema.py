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
    position_gender = "position_gender"
    country = "country"
    gender = "gender"
    division = "division"
    club = "club"
    starttime = "starttime"
    start_raw_time = "start_raw_time"
    time_5K = "5K_time"
    time_10K = "10K_time"
    time_15K = "15K_time"
    time_20K = "20K_time"
    half_time = "half_time"
    time_25K = "25K_time"
    time_30K = "30K_time"
    time_35K = "35K_time"
    time_40K = "40K_time"


class EventData(BaseModel):
    summary: str = None
    path: Path
    run_type: RunTypeEnum
    country: str
    included_data: List[RaceAttributeEnum]
    edition: str

    def __repr__(self):
        return "<Event: name=%s, country=%s, edition=%s>" % (
            self.summary.strip(),
            self.country,
            self.edition,
        )

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
