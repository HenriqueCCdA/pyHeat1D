import time

import pytest

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
