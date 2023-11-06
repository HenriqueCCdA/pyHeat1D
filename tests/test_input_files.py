import os
from copy import deepcopy
from pathlib import Path

import pytest
from pyheat1d.input_files import (
    BoundaryConditionMissingKeyError,
    Input,
    InputFileNotFoundError,
    MatPropsMissingKeyError,
    MissingInputInfoError,
    load_input_file,
    validated,
)
from pyheat1d.mesh import BoundaryCondition, MatPropsRef

INPUT = Input(
    length=50.0,
    ndiv=100,
    dt=5.0,
    nstep=1000,
    lbc=BoundaryCondition(type=1, params={"value": 10.0}),
    rbc=BoundaryCondition(type=3, params={"value": 30.0, "h": 1.0}),
    initialt=20.0,
    prop=MatPropsRef(k=1.0, ro=2.0, cp=3.0),
)

DICT_INPUT = {
    "length": 50.0,
    "ndiv": 100,
    "dt": 5.0,
    "nstep": 1000,
    "lbc": {"type": 1, "params": {"value": 10.0}},
    "rbc": {"type": 3, "params": {"value": 30.0, "h": 1.0}},
    "initialt": 20.0,
    "prop": {"k": 1.0, "ro": 2.0, "cp": 3.0},
}

BASE_DIR = os.getcwd()
OUTPUT_FILE = Path(BASE_DIR + "/tests/files/newton.json")


@pytest.mark.unitary
def test_positive_read_json():
    infos = load_input_file(OUTPUT_FILE)

    assert infos == INPUT


@pytest.mark.unitary
def test_netative_read_json_file_not_found():
    msg = "O arquivo de entrada não foi achado: wrong_path."

    with pytest.raises(InputFileNotFoundError, match=msg):
        load_input_file("wrong_path")


@pytest.mark.unitary
@pytest.mark.parametrize("value", ["length", "nstep", "dt", "nstep", "lbc", "rbc", "initialt", "prop"])
def test_negative_missing_value(value):
    dict_ = DICT_INPUT.copy()
    dict_.pop(value)

    msg = f"O valor '{value}' é necessário no arquivo de entrada."

    with pytest.raises(MissingInputInfoError, match=msg):
        validated(dict_)


@pytest.mark.unitary
@pytest.mark.parametrize(
    "bc, key, error",
    [
        (
            "lbc",
            "type",
            "O valor 'type' é necessário na condição de contorno 'lbc'.",
        ),
        (
            "lbc",
            "params",
            "O valor 'params' é necessário na condição de contorno 'lbc'.",
        ),
        (
            "rbc",
            "type",
            "O valor 'type' é necessário na condição de contorno 'rbc'.",
        ),
        (
            "rbc",
            "params",
            "O valor 'params' é necessário na condição de contorno 'rbc'.",
        ),
    ],
    ids=[
        "lbc-type",
        "lbc-params",
        "rbc-type",
        "rbc-params",
    ],
)
def test_negative_bc_missing_keys(bc, key, error):
    dict_ = deepcopy(DICT_INPUT)

    dict_[bc].pop(key)

    with pytest.raises(BoundaryConditionMissingKeyError, match=error):
        validated(dict_)


@pytest.mark.unitary
@pytest.mark.parametrize(
    "key",
    [
        "k",
        "ro",
        "cp",
    ],
)
def test_negative_prop_missing_keys(key):
    dict_ = deepcopy(DICT_INPUT)

    dict_["prop"].pop(key)

    msg = f"O valor '{key}' é necessário na propriedade do material"

    with pytest.raises(MatPropsMissingKeyError, match=msg):
        validated(dict_)
