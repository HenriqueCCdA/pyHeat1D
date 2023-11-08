import json

import numpy as np
import pytest
from pyheat1d.writer import MeshWriter, ResultsResults


@pytest.mark.unitary
def test_writer_results(tmpdir):
    path = tmpdir / "results.json"

    with ResultsResults(path, indent=4) as writer:
        writer.append_in_buffer(0.0, np.array([0.0, 0.0]))
        writer.append_in_buffer(1.0, np.array([1.0, 2.0]))

        writer.dump()

    assert tmpdir.listdir()[0].basename == "results.json"

    read_results = json.load(path.open())

    assert read_results[0] == {"t": 0.0, "u": [0.0, 0.0]}
    assert read_results[1] == {"t": 1.0, "u": [1.0, 2.0]}


@pytest.mark.unitary
def test_writer_mesh(tmpdir, mesh):
    path = tmpdir / "mesh.json"

    mesh.mk_grid()

    writer = MeshWriter(path, indent=4)
    writer.dump(mesh.cells.nodes, mesh.nodes.x)

    assert tmpdir.listdir()[0].basename == "mesh.json"

    read_mesh = json.load(path.open())

    assert read_mesh["cell_nodes"] == [
        [1, 2],
        [2, 3],
        [3, 4],
        [4, 5],
        [5, 6],
        [6, 7],
        [7, 8],
        [8, 9],
        [9, 10],
        [10, 11],
    ]

    expected_x = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

    for e, r in zip(expected_x, read_mesh["x"]):
        assert e == pytest.approx(r)
