from dataclasses import dataclass
from pathlib import Path

from pyheat1d.cells_loop import loop_over_cells
from pyheat1d.input_files import Input
from pyheat1d.mesh import Mesh
from pyheat1d.solver import Solver
from pyheat1d.system import System
from pyheat1d.writer import MeshWriter, ResultsResults


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
        output (Path): Diretorio de saida.
    """

    solver: Solver
    mesh: Mesh
    temporal_int: TemporalInt
    output_dir: Path

    def __init__(self, infos: Input, output_dir: Path):
        """
        Parameters:
            infos: Informação da simulação.
            output: Diretorio de saida.
        """

        self.output_dir = output_dir

        lbc, rbc = infos.lbc, infos.rbc
        length, n_div = infos.length, infos.ndiv

        self.temporal_int = TemporalInt(nstep=infos.nstep, dt=infos.dt)
        self.mesh = Mesh(length, n_div, lbc, rbc)

        # TODO: a EDO gerar a malha name me parece uma boa modelagem.
        self.mesh.update_prop(prop_name="k", value=infos.prop.k)
        self.mesh.update_prop(prop_name="cp", value=infos.prop.cp)
        self.mesh.update_prop(prop_name="ro", value=infos.prop.ro)

        self.mesh.mk_grid()

        self.mesh.cells.results.u[:] = infos.initialt  # TODO: cria um método

        self.solver = Solver(System(self.mesh.n_cells))

    def resolve(self) -> None:
        """Loop temporal."""

        t, nstep, dt = 0.0, self.temporal_int.nstep, self.temporal_int.dt

        output = self.output_dir / "mesh.json"
        MeshWriter(output, indent=2).dump(self.mesh.cells.nodes, self.mesh.nodes.x)

        output = self.output_dir / "results.json"

        with ResultsResults(output, indent=4) as writer:
            writer.append_in_buffer(t, self.mesh.cells.results.u)

            for _ in range(nstep):
                loop_over_cells(self.solver.system, self.mesh, dt)

                x = self.solver.solver()

                self.mesh.cells.results.u = x

                t += dt

                writer.append_in_buffer(t, self.mesh.cells.results.u)

            writer.dump()
