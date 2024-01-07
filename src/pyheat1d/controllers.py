"""Controladores da cli e aplicaçõa web"""
from pathlib import Path

from pyheat1d.edp import Edp
from pyheat1d.input_files import load_input_file
from pyheat1d.mesh import init_mesh
from pyheat1d.simulation_times import run_times
from pyheat1d.writer import MeshWriter


def run(input_file: Path) -> None:
    """Controlador que executa a simulação

    Parameters:
        input_file: Caminho do arquivo de entrada
    """
    input_file_path = input_file.absolute()
    base_dir_path = input_file_path.parent

    run_times.reset()

    input_data = load_input_file(input_file_path)

    mesh = init_mesh(
        input_data.length,
        input_data.ndiv,
        input_data.lbc,
        input_data.rbc,
        input_data.prop,
        input_data.initialt,
    )

    output = base_dir_path / "mesh.json"
    MeshWriter(output, indent=2).dump(mesh.cells.nodes, mesh.cells.centroids, mesh.nodes.x)

    edp = Edp(input_data, mesh, base_dir_path)

    edp.resolve()

    run_times.write_log_simulation_times(folder=base_dir_path)
