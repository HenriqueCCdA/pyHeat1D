import numpy as np
import pytest
from pyheat1d.mesh import BoundaryCondition, MatProps, Mesh


@pytest.fixture
def mesh():
    return Mesh(1.0, 10)


@pytest.mark.unitary
def test_init(mesh):
    # cells
    assert mesh.cells.nodes.shape == (10, 2)
    assert mesh.cells.centroids.shape == (10,)
    assert mesh.cells.results.u.shape == (10,)
    assert mesh.cells.props.k.shape == (10,)
    assert mesh.cells.props.ro.shape == (10,)
    assert mesh.cells.props.cp.shape == (10,)

    # nodes
    assert mesh.nodes.x.shape == (11,)


@pytest.mark.unitary
def test_nodes(mesh):
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

    mesh._mk_points()

    x = mesh.nodes.x

    assert len(x) == 11

    for e, c in zip(expected, x):
        assert e == pytest.approx(c)


@pytest.mark.unitary
def test_cells(mesh):
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

    mesh._mk_cells()

    cells = mesh.cells.nodes

    assert len(cells) == 10

    for e, c in zip(expected, cells):
        assert e[0] == c[0]
        assert e[1] == c[1]


@pytest.mark.unitary
def test_centroid(mesh):
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

    mesh._mk_points()
    mesh._mk_centroid()

    centroid = mesh.cells.centroids

    assert len(centroid) == 10

    for e, c in zip(expected, centroid):
        assert e == pytest.approx(c)


@pytest.mark.unitary
def test_grid(mesh):
    mesh = Mesh(1.0, 2)

    mesh.mk_grid()

    assert mesh.nodes.x[0] == 0.0
    assert mesh.nodes.x[1] == 0.5
    assert mesh.nodes.x[2] == 1.0

    assert (mesh.cells.nodes[0][0], mesh.cells.nodes[0][1]) == (1, 2)
    assert (mesh.cells.nodes[1][0], mesh.cells.nodes[1][1]) == (2, 3)

    assert mesh.cells.centroids[0] == 0.25
    assert mesh.cells.centroids[1] == 0.75


@pytest.mark.unitary
def test_grid_infos(mesh):
    assert mesh.infos == {
        "dx": 0.1,
        "n_points": 11,
        "n_cells": 10,
        "length": 1.0,
    }


@pytest.mark.unitary
def test_positeve_boundary_condition():
    bc = BoundaryCondition(type=3, params={"value": 20, "h": 1.0})

    assert bc.type == 3
    assert bc.params["value"] == 20
    assert bc.params["h"] == 1.0


@pytest.mark.unitary
def test_positeve_matprops_scalar():
    bc = MatProps(k=1.0, ro=2.0, cp=2.1)

    assert bc.k == 1.0
    assert bc.ro == 2.0
    assert bc.cp == 2.1


@pytest.mark.unitary
def test_positeve_matprops_array():
    bc = MatProps(
        k=np.array([1.0, 2.0]),
        ro=np.array([3.0, 1.2]),
        cp=np.array([4.0, 2.2]),
    )

    assert bc.k[0] == 1.0
    assert bc.k[1] == 2.0

    assert bc.ro[0] == 3.0
    assert bc.ro[1] == 1.2

    assert bc.cp[0] == 4.0
    assert bc.cp[1] == 2.2


@pytest.mark.unitary
@pytest.mark.parametrize(
    "value, prop_name",
    [
        (2.0, "k"),
        (3.0, "cp"),
        (1.0, "ro"),
    ],
)
def test_update_prop(mesh, value, prop_name):
    mesh.update_prop(value, prop_name)

    array = getattr(mesh.cells.props, prop_name)
    for i in range(mesh.n_cells):
        assert array[i] == value
