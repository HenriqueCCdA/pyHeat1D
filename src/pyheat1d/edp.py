from dataclasses import dataclass
from pathlib import Path

from pyheat1d.cells_loop import loop_over_cells
from pyheat1d.input_files import Input
from pyheat1d.mesh import Mesh
from pyheat1d.simulation_times import register_timer
from pyheat1d.solver import Solver
from pyheat1d.system import System
from pyheat1d.writer import results_writer_strategy


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


class Edp:
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

    def __init__(self, infos: Input, mesh: Mesh, output_dir: Path):
        """
        Parameters:
            infos: Informação da simulação.
            mesh: Malha.
            output: Diretorio de saida.
        """

        self.output_dir = output_dir
        self.temporal_int = TemporalInt(nstep=infos.nstep, dt=infos.dt)
        self.mesh = mesh
        self.solver = Solver(System(self.mesh.n_cells))
        self.write_every_steps = infos.write_every_steps

    @register_timer("edp")
    def resolve(self) -> None:
        """Loop temporal."""

        t, nstep, dt = 0.0, self.temporal_int.nstep, self.temporal_int.dt

        output = self.output_dir / "results.json"

        ResultsWriter = results_writer_strategy(output, indent=4, write_every_steps=self.write_every_steps)

        with ResultsWriter as writer:
            writer.append_in_buffer(0, t, self.mesh.cells.results.u)
            for step in range(1, nstep + 1):
                loop_over_cells(self.solver.system, self.mesh, dt)

                x = self.solver.solver()

                self.mesh.cells.results.u = x

                t += dt

                writer.append_in_buffer(step, t, self.mesh.cells.results.u)

            writer.dump()
