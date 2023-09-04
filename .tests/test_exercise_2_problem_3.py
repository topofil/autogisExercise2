#!/usr/bin/env python3


"""Test the submitted solutions for exercise 2, problem 3 of AutoGIS."""

import pytest

import geopandas
import pandas
import pyproj

from points_decorator import points


class Test_Exercise_2_Problem_3:
    @points(
        1,
        "Problem 3: Did you read the shapefile into a `GeoDataFrame` named "
        "`kruger_points`, and did you re-project it to EPSG:32735?"
    )
    def test_read_reproject(self, problem3):
        assert isinstance(problem3.kruger_points, geopandas.GeoDataFrame)
        assert len(problem3.kruger_points) == 81379
        assert problem3.kruger_points.crs == pyproj.CRS("EPSG:32735")

    @points(
        1,
        "Problem 3: Check again whether you grouped the points correctly!"
    )
    def test_grouped(self, problem3):
        assert isinstance(
            problem3.grouped_by_users,
            pandas.core.groupby.generic.DataFrameGroupBy
        )
        assert (
            len(problem3.grouped_by_users.groups)
            == problem3.kruger_points["userid"].nunique()
        )

    @points(
        2,
        "Problem 3: Have you created a data frame `movements` "
        "that contains LineStrings? "
        "Is it in the correct reference system?"
    )
    def test_movements_linestrings(self, problem3):
        assert isinstance(problem3.movements, geopandas.GeoDataFrame)
        assert problem3.movements.geometry.geom_type.unique() == ["LineString"]
        assert problem3.movements.crs == pyproj.CRS("EPSG:32735")

    @points(
        1,
        "Problem 3: Remember to calculate the distances between "
        "each user’s points (in `movements[\"distance\"])"
    )
    def test_movements_distance(self, problem3):
        assert "distance" in problem3.movements.columns
        assert not problem3.movements["distance"].hasnans
        assert problem3.movements["distance"].dtype == "float64"

    @points(
        0.66,
        "Problem 3: Calculate the shortest distance a user "
        "travelled between all their posts"
    )
    def test_shortest_distance(self, problem3):
        assert problem3.shortest_distance == pytest.approx(0.0)

    @points(
        0.66,
        "Problem 3: Calculate the mean distance travelled per user"
    )
    def test_mean_distance(self, problem3):
        assert problem3.mean_distance == pytest.approx(107133.51202944393)

    @points(
        0.67,
        "Problem 3: Calculate the longest distances a user travelled"
    )
    def test_max_distance(self, problem3):
        assert problem3.longest_distance == pytest.approx(6970668.816343962)

    @points(
        1,
        "Problem 3: Did you save the output into a "
        "shapefile `movements.shp` inside `DATA_DIRECTORY`?"
    )
    def test_shapefile(self, problem3):
        assert (problem3.DATA_DIRECTORY / "movements.shp").exists()
        df = geopandas.read_file(problem3.DATA_DIRECTORY / "movements.shp")
        assert len(df) == 9026
