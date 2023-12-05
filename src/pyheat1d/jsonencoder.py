"""Módulo com as expansões do JSONEncoders"""

import json

import numpy as np


class JSONEncoderNumpy(json.JSONEncoder):
    """Classe que expande JSONEncoder para array numpy"""

    def default(self, o):
        if isinstance(o, np.ndarray):
            return o.tolist()

        return super().default(o)
