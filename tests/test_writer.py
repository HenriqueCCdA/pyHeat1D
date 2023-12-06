import json
from pathlib import Path

import numpy as np
import pytest
from pyheat1d.writer import (
    MeshWriter,
    ResultsWriterEveryNSteps,
    ResultsWriterEveryTime,
    results_writer_strategy,
)


@pytest.mark.unitary
def test_results_writer_strategy():
    path = Path("results.json")

    writer = results_writer_strategy(path, indent=4, write_every_steps=4)

    assert isinstance(writer, ResultsWriterEveryNSteps)

    writer = results_writer_strategy(path, indent=4)

    assert isinstance(writer, ResultsWriterEveryTime)


@pytest.mark.unitary
def test_results_writer_every_time(tmpdir):
    path = tmpdir / "results.json"

    with ResultsWriterEveryTime(path, indent=4) as writer:
        writer.append_in_buffer(0, 0.0, np.array([0.0, 0.0]))
        writer.append_in_buffer(1, 1.0, np.array([1.0, 2.0]))

        writer.dump()

    assert tmpdir.listdir()[0].basename == "results.json"

    read_results = json.load(path.open())

    assert read_results[0] == {"istep": 0, "t": 0.0, "u": [0.0, 0.0]}
    assert read_results[1] == {"istep": 1, "t": 1.0, "u": [1.0, 2.0]}


@pytest.mark.unitary
def test_results_writer_every_n_steps(tmpdir):
    path = tmpdir / "results.json"

    with ResultsWriterEveryNSteps(path, indent=4, write_every_steps=4) as writer:
        writer.append_in_buffer(0, 0.0, np.array([0.0, 0.0]))
        writer.append_in_buffer(1, 1.0, np.array([1.0, 1.0]))
        writer.append_in_buffer(2, 2.0, np.array([1.0, 2.0]))
        writer.append_in_buffer(3, 3.0, np.array([1.0, 3.0]))
        writer.append_in_buffer(4, 4.0, np.array([1.0, 4.0]))
        writer.append_in_buffer(5, 5.0, np.array([1.0, 5.0]))
        writer.append_in_buffer(6, 6.0, np.array([1.0, 6.0]))
        writer.append_in_buffer(7, 7.0, np.array([1.0, 7.0]))
        writer.append_in_buffer(8, 8.0, np.array([1.0, 8.0]))

        writer.dump()

    assert tmpdir.listdir()[0].basename == "results.json"

    read_results = json.load(path.open())

    assert len(read_results) == 3
    assert read_results[0] == {"istep": 0, "t": 0.0, "u": [0.0, 0.0]}
    assert read_results[1] == {"istep": 4, "t": 4.0, "u": [1.0, 4.0]}
    assert read_results[2] == {"istep": 8, "t": 8.0, "u": [1.0, 8.0]}


@pytest.mark.unitary
def test_writer_mesh(tmpdir, mesh):
    path = tmpdir / "mesh.json"

    mesh.mk_grid()

    writer = MeshWriter(path, indent=4)
    writer.dump(mesh.cells.nodes, mesh.cells.centroids, mesh.nodes.x)

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

    expected_x = [0.05, 0.15, 0.25, 0.35, 0.45, 0.55, 0.65, 0.75, 0.85, 0.95]

    for e, r in zip(expected_x, read_mesh["xp"]):
        assert e == pytest.approx(r)
