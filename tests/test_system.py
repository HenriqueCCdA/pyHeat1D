from pyheat1d.system import System


def test_system():
    system = System(neq=10)

    assert system.b.shape == (10,)
    assert system.a.shape == (10, 3)
