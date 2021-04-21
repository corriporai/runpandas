"""Schema Models for loading example datasets"""

from typing import List
from enum import Enum
from pathlib import Path
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
