#!/usr/bin/env python3


"""Test the submitted solutions for exercise 2, problem 2 of AutoGIS."""

import pathlib
import tempfile

import dhash
import PIL

import geopandas
import pandas
import pyproj
import shapely.wkt

from points_decorator import points


class Test_Exercise_2_Problem_2:
    @points(
        1,
        "Problem 2: Did you read the CSV file"
        " into a data frame called `data`?"
    )
    def test_csv_read(self, problem2):
        assert isinstance(problem2.data, pandas.DataFrame)
        assert len(problem2.data) == 81379
        for column in ("lon", "lat", "timestamp", "userid"):
            assert column in problem2.data.columns

    @points(
        2,
        "Problem 2: `data` does not have a `geometry` column, "
        "or the geometry column does not contain `shapely.geometry.Points`"
    )
    def test_geometry_column(self, problem2):
        assert isinstance(problem2.data, pandas.DataFrame)
        assert "geometry" in problem2.data.columns
        assert problem2.data.geometry.apply(
            lambda g: isinstance(g, shapely.geometry.Point)
        ).unique() == [True]

    @points(
        1,
        "Problem 2: Did you convert `data` into a `geopandas.GeoDataFrame`?"
    )
    def test_gdf(self, problem2):
        assert isinstance(problem2.data, geopandas.GeoDataFrame)

    @points(
        1,
        "Problem 2: `data` does not seem to have a coordinate"
        " reference system defined."
    )
    def test_gdf_crs(self, problem2):
        assert problem2.data.crs == pyproj.CRS("EPSG:4326")

    @points(
        1,
        "Problem 2: Save the data to a Shapefile "
        "`kruger_points.shp` in `DATA_DIRECTORY`"
    )
    def test_shapefile(self, problem2):
        assert (problem2.DATA_DIRECTORY / "kruger_points.shp").exists()
        df = geopandas.read_file(problem2.DATA_DIRECTORY / "kruger_points.shp")
        assert len(df) == 81379

    @points(1, "Problem 2: Did you plot the data set?")
    def test_plot(self, problem2):
        with tempfile.TemporaryDirectory() as temp_dir:
            figure_path = pathlib.Path(temp_dir) / "plot.png"
            problem2._PLOT_1.get_figure().savefig(figure_path)
            image_hash = dhash.dhash_int(PIL.Image.open(figure_path))
        assert image_hash == 26657539604692504049140950267609623612
