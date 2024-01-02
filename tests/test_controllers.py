import shutil
from pathlib import Path

import pytest
from typer.testing import CliRunner

from pyheat1d.controllers import run

runner = CliRunner()


@pytest.mark.cli
@pytest.mark.integration
def test_run(tmpdir):
    case = Path("tests/files/input/newton.json")

    shutil.copy(case, tmpdir)

    input_case = Path(tmpdir / "newton.json")

    run(input_file=input_case)

    excepted_dir_files = {f.basename for f in tmpdir.listdir()}

    assert excepted_dir_files == {"results.json", "mesh.json", "newton.json"}
