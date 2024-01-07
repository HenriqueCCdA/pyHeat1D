import pytest

from pyheat1d.solver import Solver
from pyheat1d.system import System


@pytest.mark.unitary
def test_solver():
    system = System(neq=3)

    solv = Solver(system=system)

    assert solv.system.a.shape == (3, 3)
    assert solv.system.b.shape == (3,)


@pytest.mark.unitary
@pytest.mark.parametrize(
    "lower, diag, upper, b, e_x",
    [
        (
            [0.0, -1.0],
            [1.0, 7.0],
            [-1.0, 0.0],
            [2.0, 8],
            [11 / 3, 5 / 3],
        ),
        (
            [0.0, 2.0, 3.0],
            [1.0, 7.0, 5.0],
            [1.0, 8.0, 0.0],
            [6.0, 9.0, 6.0],
            [69.0, -63.0, 39.0],
        ),
        (
            [0.0, -1.0, -1.0, -1.0],
            [5.0, 5.0, 5.0, 5.0],
            [-1.0, -1.0, -1.0, 0.0],
            [5.5, 5.0, 11.5, 16.5],
            [1.5, 2.0, 3.5, 4],
        ),
    ],
    ids=[
        "neq=2",
        "neq=3",
        "neq=4",
    ],
)
def test_solver_tdma(lower, diag, upper, b, e_x):
    neq = len(e_x)
    system = System(neq)

    for i in range(neq):
        system.a[i, 0] = lower[i]
        system.a[i, 1] = diag[i]
        system.a[i, 2] = upper[i]
        system.b[i] = b[i]

    x = Solver(system=system).solver()

    for i in range(neq):
        assert x[i] == pytest.approx(e_x[i])
