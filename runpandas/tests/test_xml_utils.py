"""
Tests for XML tools in utils module
"""

import pytest
import io
from runpandas import _utils as utils

pytestmark = pytest.mark.stable


data = """<?xml version="1.0" encoding="UTF-8" ?>
<TrainingCenterDatabase>
<Activities>
<Activity Sport="Running">
<Id>2020-06-28T09:39:21Z</Id>
<Lap StartTime="2020-06-28T09:39:21Z">
<TotalTimeSeconds>552</TotalTimeSeconds>
<DistanceMeters>1007.838196</DistanceMeters>
<Calories>99</Calories>
<AverageHeartRateBpm>
<Value>128</Value>
</AverageHeartRateBpm>
<MaximumHeartRateBpm>
<Value>165</Value>
</MaximumHeartRateBpm>
<Intensity>Active</Intensity>
<TriggerMethod>Manual</TriggerMethod>
<Track>
<Trackpoint>
<Time>2020-06-28T09:39:24Z</Time>
<Position>
<LatitudeDegrees>-8.367331</LatitudeDegrees>
<LongitudeDegrees>-36.576199</LongitudeDegrees>
</Position>
<AltitudeMeters>679.053528</AltitudeMeters>
<DistanceMeters>5320.761719</DistanceMeters>
<HeartRateBpm>
<Value>62</Value>
</HeartRateBpm>
<Extensions>
<TPX xmlns="http://www.garmin.com/xmlschemas/ActivityExtension/v2">
<Speed>0.000000</Speed>
</TPX>
</Extensions>
</Trackpoint>
<Trackpoint>
<Time>2020-06-28T09:39:33Z</Time>
<Position>
<LatitudeDegrees>-8.364550</LatitudeDegrees>
<LongitudeDegrees>-36.578003</LongitudeDegrees>
</Position>
<AltitudeMeters>668.866272</AltitudeMeters>
<DistanceMeters>12.899824</DistanceMeters>
<HeartRateBpm>
<Value>60</Value>
</HeartRateBpm>
<Extensions>
<TPX xmlns="http://www.garmin.com/xmlschemas/ActivityExtension/v2">
<Speed>0.000000</Speed>
</TPX>
</Extensions>
</Trackpoint>
</Track>
</Lap>
</Activity>
</Activities>
</TrainingCenterDatabase>"""


def test_gen_nodes():
    faketcx = io.StringIO(data)

    trackpoints = [
        utils.recursive_text_extract(trkpt)
        for trkpt in utils.get_nodes(faketcx, ("Trackpoint",))
    ]

    assert len(trackpoints) == 2
    t1, t2 = trackpoints
    assert len(t1) == 7 and len(t2) == 7
    assert t1["Speed"] == "0.000000" and t2["Speed"] == "0.000000"
    assert t1["Time"] == "2020-06-28T09:39:24Z"
    assert t2["Time"] == "2020-06-28T09:39:33Z"
    assert t1["HeartRateBpm"] == "62" and t2["HeartRateBpm"] == "60"
