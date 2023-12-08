import shutil
from pathlib import Path

import pytest
from typer.testing import CliRunner

from pyheat1d.cli import app

runner = CliRunner()


@pytest.mark.cli
@pytest.mark.integration
def test_version():
    result = runner.invoke(app, "--version")

    assert result.exit_code == 0
    assert "pyheat1d 0.1.0" in result.stdout

    result = runner.invoke(app, "-v")

    assert result.exit_code == 0
    assert "pyheat1d 0.1.0" in result.stdout


@pytest.mark.cli
@pytest.mark.integration
def test_run(tmpdir):
    case = Path("tests/files/input/newton.json")

    shutil.copy(case, tmpdir)

    input_case = str(tmpdir / "newton.json")

    result = runner.invoke(app, ["run", input_case])

    assert result.exit_code == 0

    excepted_dir_files = {f.basename for f in tmpdir.listdir()}

    assert excepted_dir_files == {"results.json", "mesh.json", "newton.json"}


@pytest.mark.cli
@pytest.mark.integration
def test_plot(mocker):
    plot = mocker.patch("pyheat1d.cli.plt.plot")
    show = mocker.patch("pyheat1d.cli.plt.show")

    output = str(Path("tests/files/output/"))

    result = runner.invoke(app, ["plot", output, "--steps", "0, 10"])

    assert result.exit_code == 0

    assert plot.call_count == 2
    assert show.call_count == 1


@pytest.mark.cli
@pytest.mark.integration
def test_positive_plot_step_beyond_the_last(mocker):
    plot = mocker.patch("pyheat1d.cli.plt.plot")
    show = mocker.patch("pyheat1d.cli.plt.show")

    output = str(Path("tests/files/output/"))

    result = runner.invoke(app, ["plot", str(output), "--steps", "0, 10, 10000"])
    assert result.exit_code == 0

    assert plot.call_count == 2
    assert show.call_count == 1


@pytest.mark.cli
@pytest.mark.integration
def test_negative_plot_mesh_json_not_found(mocker, tmpdir):
    results = Path("tests/files/output/results.json")

    shutil.copy(results, tmpdir)

    plot = mocker.patch("pyheat1d.cli.plt.plot")
    show = mocker.patch("pyheat1d.cli.plt.show")

    result = runner.invoke(app, ["plot", str(tmpdir), "--steps", "0, 10"])
    assert result.exit_code == 1
    assert "Error: Arquivo 'mesh.json' não achado." in result.stdout

    assert plot.call_count == 0
    assert show.call_count == 0


@pytest.mark.cli
@pytest.mark.integration
def test_negative_plot_results_json_not_found(mocker, tmpdir):
    results = Path("tests/files/output/mesh.json")

    shutil.copy(results, tmpdir)

    plot = mocker.patch("pyheat1d.cli.plt.plot")
    show = mocker.patch("pyheat1d.cli.plt.show")

    result = runner.invoke(app, ["plot", str(tmpdir), "--steps", "0, 10"])
    assert result.exit_code == 1
    assert "Error: Arquivo 'results.json' não achado." in result.stdout

    assert plot.call_count == 0
    assert show.call_count == 0
