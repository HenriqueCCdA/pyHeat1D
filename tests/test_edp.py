import json

import pytest

from pyheat1d.edp import Edp
from pyheat1d.input_files import Input
from pyheat1d.mesh import BoundaryCondition, MatPropsRef, init_mesh


@pytest.mark.integration
def test_Edp_solver_bc_const_u(tmpdir):
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

    mesh = init_mesh(
        infos.length,
        infos.ndiv,
        infos.lbc,
        infos.rbc,
        infos.prop,
        infos.initialt,
    )

    edp = Edp(infos=infos, mesh=mesh, output_dir=tmpdir)

    edp.resolve()

    dir_files = {f.basename for f in tmpdir.listdir()}

    assert dir_files == {"results.json"}

    read_results = json.load(tmpdir / "results.json")
    assert len(read_results) == 101

    assert read_results[0]["t"] == 0.0

    excepted = [15.0, 15.0, 15.0, 15.0, 15.0]
    for e, r in zip(excepted, read_results[0]["u"]):
        assert e == r

    assert read_results[100]["t"] == 100.0

    excepted = [11.0, 13.0, 15.0, 17.0, 19.0]
    for e, r in zip(excepted, read_results[100]["u"]):
        assert e == pytest.approx(r)


@pytest.mark.integration
def test_Edp_solver_bc_const_u_write_every_3_steps(tmpdir):
    infos = Input(
        length=1.0,
        ndiv=5,
        dt=1.0,
        nstep=100,
        write_every_steps=3,
        lbc=BoundaryCondition(type=1, params={"value": 10.0}),
        rbc=BoundaryCondition(type=1, params={"value": 20.0}),
        initialt=15.0,
        prop=MatPropsRef(k=1.0, ro=2.0, cp=3.0),
    )

    mesh = init_mesh(
        infos.length,
        infos.ndiv,
        infos.lbc,
        infos.rbc,
        infos.prop,
        infos.initialt,
    )

    edp = Edp(infos=infos, mesh=mesh, output_dir=tmpdir)

    edp.resolve()

    dir_files = {f.basename for f in tmpdir.listdir()}

    assert dir_files == {"results.json"}

    read_results = json.load(tmpdir / "results.json")
    assert len(read_results) == 34

    assert read_results[0]["istep"] == 0
    assert read_results[0]["t"] == 0.0

    assert read_results[1]["istep"] == 3
    assert read_results[1]["t"] == 3.0

    assert read_results[2]["istep"] == 6
    assert read_results[2]["t"] == 6.0

    excepted = [15.0, 15.0, 15.0, 15.0, 15.0]
    for e, r in zip(excepted, read_results[0]["u"]):
        assert e == r

    excepted = [11.0, 13.0, 15.0, 17.0, 19.0]
    for e, r in zip(excepted, read_results[33]["u"]):
        assert e == pytest.approx(r)


@pytest.mark.integration
def test_Edp_solver_bc_convection(tmpdir):
    infos = Input(
        length=1.0,
        ndiv=5,
        dt=2.0,
        nstep=500,
        lbc=BoundaryCondition(type=3, params={"value": 10.0, "h": 2.0}),
        rbc=BoundaryCondition(type=3, params={"value": 20.0, "h": 1.0}),
        initialt=20.0,
        prop=MatPropsRef(k=2.0, ro=0.5, cp=2.0),
    )

    mesh = init_mesh(
        infos.length,
        infos.ndiv,
        infos.lbc,
        infos.rbc,
        infos.prop,
        infos.initialt,
    )

    edp = Edp(infos=infos, mesh=mesh, output_dir=tmpdir)

    edp.resolve()

    excepted_dir_files = {f.basename for f in tmpdir.listdir()}

    assert excepted_dir_files == {"results.json"}

    read_results = json.load(tmpdir / "results.json")

    assert len(read_results) == 501

    assert read_results[0]["t"] == 0.0

    excepted = [
        20.0,
        20.0,
        20.0,
        20.0,
        20.0,
    ]
    for e, r in zip(excepted, read_results[0]["u"]):
        assert e == pytest.approx(r)

    assert read_results[500]["t"] == 1000.0

    excepted = [
        13.043478260869598,
        13.478260869565256,
        13.91304347826091,
        14.34782608695656,
        14.78260869565221,
    ]
    for e, r in zip(excepted, read_results[500]["u"]):
        assert e == pytest.approx(r)
