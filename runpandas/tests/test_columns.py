"""
Test module for runpandas column types (i.e. MeasureSeries)
"""

import os
import pytest
import pandas as pd
from runpandas import reader
from runpandas.types import Activity, columns

pytestmark = pytest.mark.stable


@pytest.fixture
def dirpath(datapath):
    return datapath("io", "data")


def test_altitude_feet(dirpath):
    tcx_file = os.path.join(dirpath, "tcx", "basic.tcx")
    activity_tcx = reader._read_file(tcx_file, to_df=False)
    assert (activity_tcx["alt"].ft[-5]) == 558.6963742234277


def test_altitude_ascent_descent(dirpath):
    tcx_file = os.path.join(dirpath, "tcx", "basic.tcx")
    activity_tcx = reader._read_file(tcx_file, to_df=False)
    # test ascent and descent altitudes
    assert (activity_tcx["alt"].ascent[-5]) == 0.4805908200000033
    assert (activity_tcx["alt"].ascent[-1]) == 0.0
    assert (activity_tcx["alt"].descent[-1]) == -1.4420166019999954
    assert (activity_tcx["alt"].descent[-5]) == 0.0


def test_distance_miles(dirpath):
    gpx_file = os.path.join(dirpath, "gpx", "stopped_example.gpx")
    activity_gpx = reader._read_file(gpx_file, to_df=False)
    activity_gpx["distpos"] = activity_gpx.compute.distance()
    # test distpos conversion (meters to miles)
    assert (activity_gpx["distpos"].miles[-1]) == 0.0031649143236707027
    # test distance conversion (meters to miles)
    distance = activity_gpx["distpos"].to_distance()
    assert (distance.miles[-1]) == 7.825950111157077


def test_distance_km(dirpath):
    gpx_file = os.path.join(dirpath, "gpx", "stopped_example.gpx")
    activity_gpx = reader._read_file(gpx_file, to_df=False)
    activity_gpx["distpos"] = activity_gpx.compute.distance()
    # test distpos conversion (meters to miles)
    assert (activity_gpx["distpos"].km[-1]) == 0.005093437453100809
    # test distance conversion (meters to miles)
    distance = activity_gpx["distpos"].to_distance()
    assert (distance.km[-1]) == 12.594649752172337


def test_speed_kmh(dirpath):
    tcx_file = os.path.join(dirpath, "tcx", "stopped_example.tcx")
    activity_tcx = reader._read_file(tcx_file, to_df=False)
    # test conversion method m/s to km/h
    assert (activity_tcx["speed"].kph[-1]) == 8.498772


def test_speed_mph(dirpath):
    tcx_file = os.path.join(dirpath, "tcx", "stopped_example.tcx")
    activity_tcx = reader._read_file(tcx_file, to_df=False)
    # test conversion method m/s to miles/h
    assert (activity_tcx["speed"].mph[-1]) == 5.278740372670808


def test_speed_topace(dirpath):
    gpx_file = os.path.join(dirpath, "gpx", "stopped_example.gpx")
    activity_gpx = reader._read_file(gpx_file, to_df=False)
    activity_gpx["distpos"] = activity_gpx.compute.distance(correct_distance=True)
    activity_gpx["speed"] = activity_gpx.compute.speed(from_distances=True)
    expected = pd.Timedelta("0 days 00:00:00.392662")
    assert activity_gpx["speed"].to_pace()[-1].total_seconds() == pytest.approx(
        expected.total_seconds()
    )


def test_distpos_distance(dirpath):
    gpx_file = os.path.join(dirpath, "gpx", "stopped_example.gpx")
    activity_gpx = reader._read_file(gpx_file, to_df=False)
    activity_gpx["distpos"] = activity_gpx.compute.distance()
    # test distpos to distance
    assert (activity_gpx["distpos"].to_distance()[-1]) == 12594.649752172338


def test_gradient_pct(dirpath):
    tcx_file = os.path.join(dirpath, "tcx", "basic.tcx")
    activity_tcx = reader._read_file(tcx_file, to_df=False)
    activity_tcx["grad"] = activity_tcx.compute.gradient()
    assert (activity_tcx["grad"].pct[-1]) == -9.78415717232968


def test_gradient_radians(dirpath):
    tcx_file = os.path.join(dirpath, "tcx", "basic.tcx")
    activity_tcx = reader._read_file(tcx_file, to_df=False)
    activity_tcx["grad"] = activity_tcx.compute.gradient()
    assert (activity_tcx["grad"].radians[-1]) == -0.0975311412476771


def test_gradient_degrees(dirpath):
    tcx_file = os.path.join(dirpath, "tcx", "basic.tcx")
    activity_tcx = reader._read_file(tcx_file, to_df=False)
    activity_tcx["grad"] = activity_tcx.compute.gradient()
    assert (activity_tcx["grad"].degrees[-1]) == -5.588122764586196


def test_latlon_radians(dirpath):
    tcx_file = os.path.join(dirpath, "tcx", "basic.tcx")
    activity_tcx = reader._read_file(tcx_file, to_df=False)
    assert (activity_tcx["lat"].radians[-1]) == pytest.approx(0.6274799778819853, 0.01)
    assert (activity_tcx["lon"].radians[-1]) == -1.3804335163227985


def test_pace_min_km(dirpath):
    tcx_file = os.path.join(dirpath, "tcx", "stopped_example.tcx")
    activity_tcx = reader._read_file(tcx_file, to_df=False)
    activity_tcx["speed"] = activity_tcx.compute.speed()
    activity_tcx["pace"] = activity_tcx.compute.pace()
    assert (activity_tcx["pace"].min_per_km[-1]) == pd.Timedelta(
        "0 days 00:07:03.590608"
    )


def test_pace_min_mile(dirpath):
    tcx_file = os.path.join(dirpath, "tcx", "stopped_example.tcx")
    activity_tcx = reader._read_file(tcx_file, to_df=False)
    activity_tcx["speed"] = activity_tcx.compute.speed()
    activity_tcx["pace"] = activity_tcx.compute.pace()
    assert (activity_tcx["pace"].min_per_mile[-1].total_seconds()) == pytest.approx(
        pd.Timedelta("0 days 00:04:23.099756").total_seconds()
    )


def test_constructor(dirpath):
    tcx_file = os.path.join(dirpath, "tcx", "stopped_example.tcx")
    activity_tcx = reader._read_file(tcx_file, to_df=False)
    activity_tcx["speed"] = activity_tcx.compute.speed()
    # test custom constructor_expanddim series
    speed_frame = activity_tcx["speed"].to_frame()
    assert type(speed_frame) is Activity
    assert isinstance(speed_frame.speed, columns.Speed)
    assert list(speed_frame.columns) == ["speed"]
