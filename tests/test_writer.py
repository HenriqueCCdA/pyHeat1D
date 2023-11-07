import json

import numpy as np
from pyheat1d.writer import WriterResults


def test_writer(tmpdir):
    path = tmpdir / "results.json"

    with WriterResults(path, indent=4) as writer:
        writer.append_in_buffer(0.0, np.array([0.0, 0.0]))
        writer.append_in_buffer(1.0, np.array([1.0, 2.0]))

        writer.dump()

    assert tmpdir.listdir()[0].basename == "results.json"

    results = json.load(path.open())

    assert results[0] == {"t": 0.0, "u": [0.0, 0.0]}
    assert results[1] == {"t": 1.0, "u": [1.0, 2.0]}
