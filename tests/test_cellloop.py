from pyheat1d.cells_loop import loop_over_cells
from pyheat1d.system import System


def test_assemble_system(mesh):
    mesh.update_prop(prop_name="k", value=2.0)
    mesh.update_prop(prop_name="ro", value=2.0)
    mesh.update_prop(prop_name="cp", value=0.5)

    system = System(mesh.n_cells)

    loop_over_cells(system, mesh, 1.0)

    expeted = [400.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 27.272727272727273]

    for i in range(system.neq):
        assert system.b[i] == expeted[i]

    expeted = [
        (0.0, 60.1, -20.0),  # 1
        (-20.0, 40.1, -20.0),  # 2
        (-20.0, 40.1, -20.0),  # 3
        (-20.0, 40.1, -20.0),  # 4
        (-20.0, 40.1, -20.0),  # 5
        (-20.0, 40.1, -20.0),  # 6
        (-20.0, 40.1, -20.0),  # 7
        (-20.0, 40.1, -20.0),  # 8
        (-20.0, 40.1, -20.0),  # 9
        (-20.0, 21.00909090909091, 0.0),  # 10
    ]

    for i in range(system.neq):
        assert system.a[i, 0] == expeted[i][0]
        assert system.a[i, 1] == expeted[i][1]
        assert system.a[i, 2] == expeted[i][2]
