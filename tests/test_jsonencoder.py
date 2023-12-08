import json

import numpy as np
import pytest

from pyheat1d.jsonencoder import JSONEncoderNumpy


@pytest.mark.unitary
def test_np_array2json():
    x = np.array([2.0, 3.0])

    assert json.dumps(x, cls=JSONEncoderNumpy) == "[2.0, 3.0]"


@pytest.mark.unitary
def test_JSONEncoderNumpy():
    x = np.array([2.0, 3.0])

    assert JSONEncoderNumpy().encode(x) == "[2.0, 3.0]"
