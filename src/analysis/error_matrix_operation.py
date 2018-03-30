from typing import List, Callable

import numpy as np

from src.animation.frame import Frame


class ErrorMatrixOperation:
    def __init__(self, objective_function: Callable):
        self.objective_function = objective_function

    def calculate(self, frames: List[Frame]):
        points = [np.array(frame.as_point()) for frame in frames]
        return self.objective_function(points)
