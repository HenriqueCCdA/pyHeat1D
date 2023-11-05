import pytest
from pyheat1d.grid import BoundaryCondition, MatProps, Mesh


@pytest.fixture
def grid():
    return Mesh(1.0, 10)


@pytest.mark.unitary
def test_nodes(grid):
    expected = [
        0.0,
        0.1,
        0.2,
        0.3,
        0.4,
        0.5,
        0.6,
        0.7,
        0.8,
        0.9,
        1.0,
    ]

    grid._mk_points()

    x = grid.x

    assert len(x) == 11

    for e, c in zip(expected, x):
        assert e == pytest.approx(c)


@pytest.mark.unitary
def test_cells(grid):
    expected = [
        (1, 2),
        (2, 3),
        (3, 4),
        (4, 5),
        (5, 6),
        (6, 7),
        (7, 8),
        (8, 9),
        (9, 10),
        (10, 11),
    ]

    grid._mk_cells()

    cells = grid.cells

    assert len(cells) == 10

    for e, c in zip(expected, cells):
        assert e[0] == c[0]
        assert e[1] == c[1]


@pytest.mark.unitary
def test_centroid(grid):
    expected = [
        0.05,
        0.15,
        0.25,
        0.35,
        0.45,
        0.55,
        0.65,
        0.75,
        0.85,
        0.95,
    ]

    grid._mk_points()
    grid._mk_centroid()

    centroid = grid.centroids

    assert len(centroid) == 10

    for e, c in zip(expected, centroid):
        assert e == pytest.approx(c)


@pytest.mark.unitary
def test_grid(grid):
    grid = Mesh(1.0, 2)

    grid.mk_grid()

    assert grid.x[0] == 0.0
    assert grid.x[1] == 0.5
    assert grid.x[2] == 1.0

    assert (grid.cells[0][0], grid.cells[0][1]) == (1, 2)
    assert (grid.cells[1][0], grid.cells[1][1]) == (2, 3)

    assert grid.centroids[0] == 0.25
    assert grid.centroids[1] == 0.75


def test_grid_infos(grid):
    assert grid.infos == {
        "dx": 0.1,
        "n_points": 11,
        "n_cells": 10,
        "length": 1.0,
    }


def test_positeve_boundary_condition():
    bc = BoundaryCondition(type=3, params={"value": 20, "h": 1.0})

    assert bc.type == 3
    assert bc.params["value"] == 20
    assert bc.params["h"] == 1.0


def test_positeve_matprops():
    bc = MatProps(k=1.0, ro=2.0, cp=2.1)

    assert bc.k == 1.0
    assert bc.ro == 2.0
    assert bc.cp == 2.1
