import numpy as np

from pyheat1d.mesh import BoundaryCondition, Mesh
from pyheat1d.simulation_times import register_timer
from pyheat1d.system import System


@register_timer("cell_loop")
def loop_over_cells(
    system: System,
    mesh: Mesh,
    dt: float,
) -> None:
    """
    Loop sobre todas as celulas.

    Parameters:
        system: O Sistema de equações.
        mesh: A malha.
        dt: Passo de tempo.
    """
    a, b = system.a, system.b

    ro, cp, k = mesh.cells.props.ro, mesh.cells.props.cp, mesh.cells.props.k

    u = mesh.cells.results.u

    lbc, rbc = mesh.lbc, mesh.rbc

    n_cells, dx = mesh.n_cells, mesh.dx

    _loop_over_cells(a, b, u, ro, cp, k, lbc, rbc, n_cells, dt, dx)


def _loop_over_cells(
    a: np.ndarray,
    b: np.ndarray,
    u: np.ndarray,
    ro: np.ndarray,
    cp: np.ndarray,
    k: np.ndarray,
    lbc: BoundaryCondition,
    rbc: BoundaryCondition,
    n_cells: int,
    dt: float,
    dx: float,
) -> None:
    """
    Loop sobre todas as celulas.

    Parameters:
        a: Matriz de coeficientes.
        b: Vetor de forças.
        u: Valores do passo de termpo anterior.
        ro: Massa específica.
        cp: Calor específico.
        lbc: Condição de contorno a esquerda.
        rbc: Condição de contorno a direita.
        n_cells: Número de celulas.
        dx: Tamanho da célula.
        dt: Passo de tempo.
    """

    type_, params = lbc.type, lbc.params
    # temperatura pescrita
    aP0 = ro[0] * cp[0] * dx / dt
    kf = (k[0] + k[1]) * 0.5e0
    aE = kf / dx
    if type_ == 1:
        value = params["value"]
        sP = -2.0e0 * k[0] / dx
        sU = -sP * value
    # fluxo prescrito
    elif type_ == 2:
        value = params["value"]
        sP = 0.0e0
        sU = -value
    # lei de resfriamento
    elif type_ == 3:
        value, h = params["value"], params["h"]
        tmp = 1.0e0 + (h * 2.0e0 * dx) / k[0]
        tmp = h / tmp
        sP = -tmp
        sU = tmp * value

    #  W
    a[0, 0] = 0.0e0
    # p
    a[0, 1] = aP0 + aE - sP
    # E
    a[0, 2] = -aE
    # b
    b[0] = sU + aP0 * u[0]

    type_, params = rbc.type, rbc.params
    # ... temperatura pescrita
    aP0 = ro[-1] * cp[-1] * dx / dt
    kf = (k[-2] + k[-1]) * 0.5e0
    aW = kf / dx
    if type_ == 1:
        value = params["value"]
        sP = -2.0e0 * k[-1] / dx
        sU = -sP * value
    # ... fluxo prescrito
    elif type_ == 2:
        value = params["value"]
        sP = 0.0e0
        sU = -value
    # ... lei de resfriamento
    elif type_ == 3:
        value, h = params["value"], params["h"]
        tmp = 1.0e0 + (h * 2.0e0 * dx) / k[-1]
        tmp = h / tmp
        sP = -tmp
        sU = tmp * value

    # W
    a[-1, 0] = -aW
    # p
    a[-1, 1] = aP0 + aW - sP
    # E
    a[-1, 2] = 0.0e0
    # b
    b[-1] = sU + aP0 * u[-1]

    #
    for i in range(1, n_cells - 1):
        aP0 = ro[i] * cp[i] * dx / dt
        # ... w
        kf = (k[i - 1] + k[i]) * 0.5e0
        aW = kf / dx
        # ... w
        kf = (k[i] + k[i + 1]) * 0.5e0
        aE = kf / dx
        # ...
        a[i, 0] = -aW
        a[i, 1] = aP0 + aW + aE
        a[i, 2] = -aE
        # ...
        b[i] = aP0 * u[i]
