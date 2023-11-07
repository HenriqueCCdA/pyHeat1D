import pytest
from pyheat1d.edp import Edo
from pyheat1d.input_files import Input
from pyheat1d.mesh import BoundaryCondition, MatPropsRef


@pytest.mark.integration
def test_edo_solver_bc_const_u():
    infos = Input(
        length=1.0,
        ndiv=5,
        dt=1.0,
        nstep=100,
        lbc=BoundaryCondition(type=1, params={"value": 10.0}),
        rbc=BoundaryCondition(type=1, params={"value": 20.0}),
        initialt=15.0,
        prop=MatPropsRef(k=1.0, ro=2.0, cp=3.0),
    )

    edo = Edo(infos=infos)

    edo.resolve()

    excepted = [11.0, 13.0, 15.0, 17.0, 19.0]
    for u, e in zip(edo.mesh.cells.results.u, excepted):
        assert u == pytest.approx(e)


@pytest.mark.integration
def test_edo_solver_bc_convection():
    infos = Input(
        length=1.0,
        ndiv=5,
        dt=2.0,
        nstep=500,
        lbc=BoundaryCondition(type=3, params={"value": 10.0, "h": 2.0}),
        rbc=BoundaryCondition(type=3, params={"value": 20.0, "h": 1.0}),
        initialt=15.0,
        prop=MatPropsRef(k=2.0, ro=0.5, cp=2.0),
    )

    edo = Edo(infos=infos)

    edo.resolve()

    excepted = [
        13.043478260869598,
        13.478260869565256,
        13.91304347826091,
        14.34782608695656,
        14.78260869565221,
    ]
    for u, e in zip(edo.mesh.cells.results.u, excepted):
        assert u == pytest.approx(e)
