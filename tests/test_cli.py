import shutil
from pathlib import Path

import pytest
from pyheat1d.cli import app
from typer.testing import CliRunner

runner = CliRunner()


@pytest.mark.integration
def test_version():
    result = runner.invoke(app, "--version")

    assert result.exit_code == 0
    assert "pyheat1d 0.1.0" in result.stdout

    result = runner.invoke(app, "-v")

    assert result.exit_code == 0
    assert "pyheat1d 0.1.0" in result.stdout


@pytest.mark.integration
def test_run(tmpdir):
    case = Path("tests/files/newton.json")

    shutil.copy(case, tmpdir)

    input_case = str(tmpdir / "newton.json")

    result = runner.invoke(app, ["run", input_case])

    assert result.exit_code == 0

    excepted_dir_files = {f.basename for f in tmpdir.listdir()}

    assert excepted_dir_files == {"results.json", "mesh.json", "newton.json"}
