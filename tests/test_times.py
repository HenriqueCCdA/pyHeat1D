import json
import time
from pathlib import Path

import pytest

from pyheat1d.errors import TimeLogWriteFileError
from pyheat1d.simulation_times import register_timer, run_times


@pytest.fixture(autouse=True)
def zero_timer():
    run_times.reset()


@pytest.mark.unitary
def test_run_run_times_data():
    assert run_times.cell_loop == 0.0
    assert run_times.solver == 0.0
    assert run_times.edp == 0.0


@pytest.mark.unitary
@pytest.mark.parametrize("name", ["edp", "solver", "cell_loop"])
def test_time_func_decorator(name):
    @register_timer(name)
    def wait_one_seconds():
        time.sleep(1)

    wait_one_seconds()

    assert getattr(run_times, name) == pytest.approx(1.0, rel=1.0e-2)


@pytest.mark.unitary
@pytest.mark.parametrize("name", ["edp", "solver", "cell_loop"])
def test_time_class_decorator(name):
    class A:
        @register_timer(name)
        def wait_one_seconds(self):
            time.sleep(1)

    A().wait_one_seconds()

    assert getattr(run_times, name) == pytest.approx(1.0, rel=1.0e-2)


@pytest.mark.unitary
def test_stdout_print_times_simulation(capsys):
    run_times.cell_loop = 1.0
    run_times.solver = 1.0
    run_times.edp = 2.0

    run_times.print_stdout_simulation_times()

    captured = capsys.readouterr()

    assert "Edp      : 2.000" in captured.out
    assert "Cell loop: 1.000" in captured.out
    assert "Solver   : 1.000" in captured.out


@pytest.mark.unitary
def test_write_times_simulation(tmp_path):
    run_times.cell_loop = 1.0
    run_times.solver = 1.0
    run_times.edp = 2.0

    folder = Path(tmp_path)

    run_times.write_log_simulation_times(folder=folder)

    file = folder / "time_log.json"

    data_read = json.load(file.open(mode="r", encoding="utf8"))

    assert data_read == {
        "edp": 2.000,
        "solver": 1.000,
        "cell_loop": 1.000,
    }


@pytest.mark.unitary
def test_negative_write_times_simulation_wrong_path():
    with pytest.raises(TimeLogWriteFileError, match="O arquivo 'wrong/time_log.json' não pode ser escrito."):
        run_times.write_log_simulation_times(folder=Path("wrong"))
