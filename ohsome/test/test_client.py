#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for ohsome client"""
import datetime as dt
import logging
import os

import geopandas as gpd
import pandas as pd
import pytest

import ohsome
from ohsome.constants import OHSOME_VERSION

script_path = os.path.dirname(os.path.realpath(__file__))
logger = logging.getLogger(__name__)


# def test_userdefined_url():
#     """
#     Test whether request can be sent to alternative url
#     :return:
#     """
#     base_api_url = "https://api.ohsome.org/v0.9/"
#     bboxes = "8.7137,49.4096,8.717,49.4119"
#     time = "2018-01-01"
#     fltr = "name=Krautturm and type:way"
#
#     client = ohsome.OhsomeClient(base_api_url=base_api_url)
#     response = client.elements.count.post(bboxes=bboxes, time=time, filter=fltr)
#     result = response.as_dataframe()
#
#     assert isinstance(result, pd.DataFrame)


def test_get_metadata(custom_client):
    """Test get metadata."""
    res = custom_client.metadata
    logger.info(res)
    res = custom_client.base_api_url
    logger.info(res)


def test_start_and_end_timestamp(custom_client):
    """
    Get start timestamp
    :return:
    """
    assert custom_client.start_timestamp == "2007-10-08T00:00:00Z"
    assert isinstance(custom_client.end_timestamp, str)


def test_api_version(custom_client):
    """
    Get ohsome API version
    :return:
    """
    assert isinstance(custom_client.api_version, str)


def test_user_agent(custom_client):
    """
    Checks user agent set by ohsome-py
    :return:
    """
    client = custom_client
    resp = client._session().get(client._url)
    print(resp.request.headers)
    used_user_agent = resp.request.headers["user-agent"].split("/")
    assert used_user_agent[0] == "ohsome-py"
    assert used_user_agent[1] == OHSOME_VERSION


def test_check_time_parameter_list(custom_client):
    """
    Checks whether time provided as list of strings is converted correctly
    :return:
    """
    time = pd.date_range("2018-01-01", periods=3, freq="D")
    time = list(time.strftime("%Y-%m-%dT%H:%M:%S").tolist())
    bcircles = gpd.read_file(f"{script_path}/data/points.geojson")
    fltr = "amenity=restaurant and type:way"

    client = custom_client
    client.elements.count.post(bcircles=bcircles, time=time, filter=fltr)


def test_check_time_parameter_datetimeindex(custom_client):
    """
    Checks whether time provided as pandas.DateTimeIndex is converted correctly
    :return:
    """
    time = pd.date_range("2018-01-01", periods=3, freq="D")
    bcircles = gpd.read_file(f"{script_path}/data/points.geojson")
    fltr = "amenity=restaurant and type:way"

    client = custom_client
    client.elements.count.post(bcircles=bcircles, time=time, filter=fltr)


def test_check_time_parameter_series(custom_client):
    """
    Checks whether time provided as pandas.DateTimeIndex is converted correctly
    :return:
    """
    time = pd.Series(["2018-01-01", "2018-01-02"])
    bcircles = gpd.read_file(f"{script_path}/data/points.geojson")
    fltr = "amenity=restaurant and type:way"

    client = custom_client
    client.elements.count.post(bcircles=bcircles, time=time, filter=fltr)


def test_check_time_parameter_datetime(custom_client):
    """
    Checks whether time provided as pandas.Series is converted correctly
    :return:
    """
    bcircles = gpd.read_file(f"{script_path}/data/points.geojson")
    fltr = "amenity=restaurant and type:way"
    client = custom_client

    time = [
        dt.datetime.strptime("2018-01-01", "%Y-%m-%d"),
        dt.datetime.strptime("2018-01-02", "%Y-%m-%d"),
    ]
    response = client.elements.count.post(bcircles=bcircles, time=time, filter=fltr)
    result = response.as_dataframe()
    assert len(result) == 2


def test_end_timestamp_as_time_input(custom_client):
    """
    Test whether the end_timestamp value can be used as input to a query as time
    :return:
    """
    bcircles = gpd.read_file(f"{script_path}/data/points.geojson")
    fltr = "amenity=restaurant and type:way"
    client = custom_client

    time = client.end_timestamp
    response = client.elements.count.post(bcircles=bcircles, time=time, filter=fltr)
    result = response.as_dataframe()
    assert len(result) == 1


def test_format_bcircles_dataframe(custom_client):
    """
    Test whether a DataFrame object given as 'bcircles' is formatted correctly.
    :return:
    """
    bcircles = pd.DataFrame(
        {
            "id": [1, 2],
            "lon": [8.695, 8.696],
            "lat": [49.41, 49.41],
            "radius": [500, 500],
        }
    )
    time = "2018-01-01"
    fltr = "amenity=restaurant and type:way"

    client = custom_client
    client.elements.count.groupByBoundary.post(
        bcircles=bcircles, time=time, filter=fltr
    )


def test_format_bcircles_list(custom_client):
    """
    Test whether a DataFrame object given as 'bcircles' is formatted correctly.
    :return:
    """
    time = "2018-01-01"
    fltr = "amenity=restaurant and type:node"
    client = custom_client

    bcircles = [[8.695, 49.41, 200], [8.696, 49.41, 200]]
    client.elements.count.post(bcircles=bcircles, time=time, filter=fltr)

    bcircles = {1: [8.695, 49.41, 200], 2: [8.696, 49.41, 200]}
    client.elements.count.groupByBoundary.post(
        bcircles=bcircles, time=time, filter=fltr
    )

    bcircles = ["1:8.695, 49.41, 200", "2:8.696, 49.41, 200"]
    client.elements.count.post(bcircles=bcircles, time=time, filter=fltr)

    bcircles = "1:8.695, 49.41, 200"
    client.elements.count.post(bcircles=bcircles, time=time, filter=fltr)


def test_format_bcircles_geodataframe(custom_client):
    """
    Test whether a GeoDataFrame object given as 'bcircles' is formatted correctly.
    :return:
    """
    bcircles = gpd.read_file(f"{script_path}/data/points.geojson")
    time = "2014-01-01/2017-01-01/P1Y"
    fltr = "amenity=restaurant and type:way"

    client = custom_client
    client.elements.count.groupByBoundary.post(
        bcircles=bcircles, time=time, filter=fltr
    )


def test_format_bcircles_geodataframe_geometry_error(custom_client):
    """
    Test whether a GeoDataFrame object given as 'bcircles' is formatted correctly.
    :return:
    """
    bcircles = gpd.read_file(f"{script_path}/data/polygons.geojson")
    time = "2018-01-01"
    fltr = "amenity=restaurant and type:way"

    client = custom_client
    with pytest.raises(ohsome.OhsomeException) as e_info:
        client.elements.count.groupByBoundary.post(
            bcircles=bcircles, time=time, filter=fltr
        )
    assert (
        "The geometry of the 'bcircles' GeoDataFrame may only include 'Point' geometry types."
        in e_info.value.message
    )
    del client


def test_format_bpolys(custom_client):
    """
    Test whether a GeoDataFrame obejct is formatted correctly for ohsome api.
    :return:
    """
    bpolys = gpd.read_file(f"{script_path}/data/polygons.geojson")
    time = "2018-01-01"
    fltr = "amenity=restaurant and type:node"

    client = custom_client
    client.elements.count.post(bpolys=bpolys, time=time, filter=fltr)


def test_format_bboxes_dataframe(custom_client):
    """
    Tests whether input parameter given as a pandas.DataFrame is formatted correctly to a string
    :return:
    """
    data = gpd.read_file(f"{script_path}/data/polygons.geojson")
    bboxes = data.bounds
    time = "2010-01-01"
    fltr = "amenity=restaurant and type:node"

    client = custom_client
    client.elements.count.post(bboxes=bboxes, time=time, filter=fltr)


def test_format_bboxes_dataframe_missing_columns(custom_client):
    """
    Tests whether input parameter given as a pandas.DataFrame is formatted correctly to a string
    :return:
    """
    data = gpd.read_file(f"{script_path}/data/polygons.geojson")
    bboxes = data.bounds
    bboxes.drop(columns="minx", inplace=True)
    time = "2010-01-01"
    fltr = "amenity=restaurant and type:node"

    client = custom_client
    with pytest.raises(ohsome.OhsomeException) as e_info:
        client.elements.count.post(bboxes=bboxes, time=time, filter=fltr)
    if "occurred at index 0" in e_info.value.message:
        # Python 3.6 does some weird stuff with the output. So it differs a bit.
        assert (
            "Column ('minx', 'occurred at index 0') is missing in the dataframe provided as 'bboxes'."
            in e_info.value.message
        )
    else:
        assert (
            "Column 'minx' is missing in the dataframe provided as 'bboxes'."
            in e_info.value.message
        )


def test_format_bboxes_geodataframe(custom_client):
    """
    Tests whether input parameter given as a pandas.DataFrame is formatted correctly to a string
    :return:
    """
    data = gpd.read_file(f"{script_path}/data/polygons.geojson")
    time = "2010-01-01/2011-01-01/P1Y"
    fltr = "amenity=restaurant and type:node"

    client = custom_client
    with pytest.raises(ohsome.OhsomeException) as e_info:
        client.elements.count.post(bboxes=data, time=time, filter=fltr)
    if "occurred at index 0" in e_info.value.message:
        # Python 3.6 does some weird stuff with the output. So it differs a bit.
        assert (
            "Column ('minx', 'occurred at index 0') is missing in the dataframe provided as 'bboxes'."
            in e_info.value.message
        )
    else:
        assert (
            "Use the 'bpolys' parameter to specify the boundaries using a "
            "geopandas.GeoDataFrame." in e_info.value.message
        )


def test_format_bboxes_list(custom_client):
    """
    Tests whether parameter bboxes given as a list is formatted correctly
    :return:
    """
    time = "2010-01-01"
    fltr = "amenity=restaurant and type:node"

    client = custom_client

    bboxes = [
        [8.67066, 49.41423, 8.68177, 49.4204],
        [8.67066, 49.41423, 8.68177, 49.4204],
    ]
    client.elements.count.post(bboxes=bboxes, time=time, filter=fltr)

    bboxes = {
        "1": [8.67066, 49.41423, 8.68177, 49.4204],
        "2": [8.67066, 49.41423, 8.68177, 49.4204],
    }
    client.elements.count.post(bboxes=bboxes, time=time, filter=fltr)

    bboxes = [8.67066, 49.41423, 8.68177, 49.4204]
    client.elements.count.post(bboxes=bboxes, time=time, filter=fltr)

    bboxes = [
        "8.67066, 49.41423, 8.68177, 49.4204",
        "8.67066, 49.41423, 8.68177, 49.4204",
    ]
    client.elements.count.post(bboxes=bboxes, time=time, filter=fltr)

    bboxes = "8.67066, 49.41423, 8.68177, 49.4204"
    client.elements.count.post(bboxes=bboxes, time=time, filter=fltr)


def test_post_with_endpoint_string(custom_client):
    """
    Tests whether a request can be sent of by providing the endpoint url as a string to post()
    :return:
    """
    bboxes = "8.7137,49.4096,8.717,49.4119"
    time = "2015-01-01,2016-01-01"
    filter = "name=Krautturm and type:way"

    endpoint = "contributions/latest/bbox"
    client = custom_client
    response = client.post(endpoint=endpoint, bboxes=bboxes, time=time, filter=filter)
    result = response.as_dataframe()
    assert isinstance(result, gpd.GeoDataFrame)
    assert len(result) == 1

    # Test query with leading and ending slashes
    endpoint = "/contributions/latest/bbox/"
    client = custom_client
    response = client.post(endpoint=endpoint, bboxes=bboxes, time=time, filter=filter)
    result = response.as_dataframe()

    assert isinstance(result, gpd.GeoDataFrame)
    assert len(result) == 1
