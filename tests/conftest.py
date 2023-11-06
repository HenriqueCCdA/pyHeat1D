import pytest
from pyheat1d.mesh import BoundaryCondition, Mesh


@pytest.fixture
def mesh():
    lbc = BoundaryCondition(type=1, params={"value": 10.0})
    rbc = BoundaryCondition(type=3, params={"value": 30.0, "h": 1.0})
    return Mesh(1.0, 10, lbc, rbc)
