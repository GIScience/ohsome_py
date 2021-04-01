# ohsome-py: A Python client for the ohsome API

[![status: experimental](https://github.com/GIScience/badges/raw/master/status/experimental.svg)](https://github.com/GIScience/badges#experimental)

The *ohsome-py* package helps you extract and analyse OpenStreetMap history data using the [ohsome API](https://docs.ohsome.org/ohsome-api/v1/) and Python. It handles queries to the [ohsome API](https://docs.ohsome.org/ohsome-api/v1/) and converts its responses to [Pandas](https://pandas.pydata.org/) and [GeoPandas](https://geopandas.org/) data frames to facilitate easy data handling and analysis.

The ohsome API provides various endpoints for [data aggregation](https://api.ohsome.org/v1/swagger-ui.html?urls.primaryName=Data%20Aggregation), [data extraction](https://api.ohsome.org/v1/swagger-ui.html?urls.primaryName=dataExtraction) and [contributions](https://api.ohsome.org/v1/swagger-ui.html?urls.primaryName=Contributions) to analyse the history of OSM data. Take a look at the [documentation of the ohsome API](https://docs.ohsome.org/ohsome-api/stable) or go through the [Tutorial](https://github.com/GIScience/ohsome-py/blob/master/notebooks/Tutorial.ipynb) to get started on how to use *ohsome-py*.


## Installation

*ohsome-py* requires Python >= 3.6. The easiest way to install *ohsome-py* is using pip:

```
$ pip install ohsome
```

If you want to run the Juypter Notebook [Tutorial](https://github.com/GIScience/ohsome-py/blob/master/notebooks/Tutorial.ipynb) you also need to install `jupyter` and `matplotlib`:

```
$ pip install jupyter matplotlib
```

## Usage

All queries are handled by an `OhsomeClient` object, which also provides information about the current ohsome API instance, e.g. `start_timestamp` and `end_timestamp` indicate the earliest and the latest possible dates for a query.

``` python
from ohsome import OhsomeClient
client = OhsomeClient()
client.start_timestamp # --> '2007-10-08T00:00:00Z'
client.end_timestamp # --> '2021-01-23T03:00Z'
```

### 1. Data Aggregation

**Example:** The Number of OSM ways tagged as _landuse=farmland_ using the [/elements/count](https://api.ohsome.org/v1/swagger-ui.html?urls.primaryName=Data%20Aggregation#/Count/count_1) endpoint:

``` python
response = client.elements.count.post(bboxes=[8.625,49.3711,8.7334,49.4397],
				      time="2014-01-01",
				      filter="landuse=farmland and type:way")
```

The single components of the endpoint URL are appended as method calls to the `OhsomeClient` object. Use automatic code completion to find valid endpoints. Alternatively, you can define the endpoint as argument in the `.post()` method.

``` python
response = client.post(endpoint="elements/count",
		       bboxes=[8.625,49.3711,8.7334,49.4397],
		       time="2020-01-01",
		       filter="landuse=farmland and type:way")
```

Responses from the data aggregation endpoints can be converted to a `pandas.DataFrame` object using the `OhsomeResponse.as_dataframe()` method.

```
response_df = response.as_dataframe()
```

### 2. Data Extraction

**Example:** OSM ways tagged as _landuse=farmland_ including their geometry and tags using the [/elements/geometry](https://api.ohsome.org/v1/swagger-ui.html?urls.primaryName=Data%20Extraction#/Data%20Extraction/elementsGeometry_1) endpoint:

``` python
client = OhsomeClient()
response = client.elements.geometry.post(bboxes=[8.625,49.3711,8.7334,49.4397],
					 time="2020-01-01",
					 filter="landuse=farmland and type:way",
					 properties="tags")
response_gdf = response.as_dataframe()
```

Responses from the data extraction endpoint can be converted to a `geopandas.GeoDataFrame`  using the `OhsomeResponse.as_dataframe()` method, since the data contains geometries.

### Query Parameters

All query parameters are described in the [ohsome API documentation](https://docs.ohsome.org/ohsome-api/stable) and can be passed as `string` objects to the `post()` method. Other Python data types are accepted as well.

#### Boundary

The [boundary](https://docs.ohsome.org/ohsome-api/stable/boundaries.html) of the query can be defined using the `bpolys`, `bboxes` and `bcircles` parameters. The coordinates have to be given in WGS 84 (EPSG:4326).

##### bpolys

The `bpolys` parameter can be passed as a `geopandas.GeoDataFrame` containing the polygon features.

``` python
bpolys = gpd.read_file("./data/polygons.geojson")
client.elements.count.groupByBoundary.post(bpolys=bpolys, filter="amenity=restaurant")
```

##### bboxes

The `bboxes` parameter contains the coordinates of one or several bounding boxes.

``` python
bboxes = [8.7137,49.4096,8.717,49.4119] # one bounding box
bboxes = [[8.7137,49.4096,8.717,49.4119], [8.7137,49.4096,8.717,49.4119]]
bboxes = {"A": [8.67066, 49.41423, 8.68177, 49.4204],
	  "B": [8.67066, 49.41423, 8.68177, 49.4204]}
```

##### bcircles

The `bcircles` parameter contains one or several circles defined through the coordinates of the centroids and the radius in meters.

```python
bcircles = [8.7137,49.4096, 100]
bcircles = [[8.7137,49.4096, 100], [8.7137,49.4096, 300]]
bcircles = {"Circle1": [8.695, 49.41, 200],
	    "Circle2": [8.696, 49.41, 200]}
```

#### Time

The [time](https://docs.ohsome.org/ohsome-api/stable/time.html) parameter must be ISO-8601 conform can be passed in several ways

```python
time = '2018-01-01/2018-03-01/P1M'
time = ['2018-01-01', '2018-02-01', '2018-03-01']
time = datetime.datetime(year=2018, month=3, day=1)
time = pandas.date_range("2018-01-01", periods=3, freq="M")
```

## Contribution Guidelines

If you want to contribute to this project, please fork the repository or create a new branch containing your changes.

**Install the pre-commit hooks** in our local git repo before commiting to ensure homogenous code style.

```
$ pre-commit install
```

**Run the tests** inside the repo using `pytest` (and `poetry` if you like) to make sure everything works.

```
$ poetry run pytest
```

Running the tests in a docker container containing an ohsome API instance is faster, but not mandatory. To set up and start such a docker container run the following command before running the tests.

```
$ docker run -dt --name ohsome-api -p 8080:8080 julianpsotta/ohsome-api:1.3.2
```

Create a **pull request to the development** branch once it is ready to be merged.

## References

The design of this package was inspired by the blog post [Using Python to Implement a Fluent Interface to Any REST API](https://sendgrid.com/blog/using-python-to-implement-a-fluent-interface-to-any-rest-api/) by Elmer Thomas.
