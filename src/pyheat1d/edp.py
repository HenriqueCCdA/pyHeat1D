from dataclasses import dataclass

from pyheat1d.cells_loop import loop_over_cells
from pyheat1d.input_files import Input
from pyheat1d.mesh import Mesh
from pyheat1d.solver import Solver
from pyheat1d.system import System


@dataclass
class TemporalInt:
    """
    Integração temporal.

    Parameters:
        nstep (int): Número de passos.
        dt (float): Passo de tempo.
    """

    nstep: int
    dt: float


class Edo:
    """
    Classe que representa a solução da euqação diferenncial parcial.

    Parameters:
        solver (Solver): Solução dos sistema de equaçẽos.
        mesh (Mesh): A malha.
        temporal_int (TemporalInt): Discretização temporal.
    """

    solver: Solver
    mesh: Mesh
    temporal_int: TemporalInt

    def __init__(self, infos: Input):
        """
        Parameters:
            infos: Informação da simulação
        """

        lbc, rbc = infos.lbc, infos.rbc
        length, n_div = infos.length, infos.ndiv

        self.temporal_int = TemporalInt(nstep=infos.nstep, dt=infos.dt)
        self.mesh = Mesh(length, n_div, lbc, rbc)

        self.mesh.update_prop(prop_name="k", value=infos.prop.k)
        self.mesh.update_prop(prop_name="cp", value=infos.prop.cp)
        self.mesh.update_prop(prop_name="ro", value=infos.prop.ro)

        self.mesh.cells.results.u[:] = infos.initialt  # TODO: cria um método

        self.solver = Solver(System(self.mesh.n_cells))

    def resolve(self) -> None:
        """Loop temporal."""

        t, nstep, dt = 0.0, self.temporal_int.nstep, self.temporal_int.dt

        for _ in range(nstep):
            loop_over_cells(self.solver.system, self.mesh, dt)

            x = self.solver.solver()

            self.mesh.cells.results.u = x

            t += dt
