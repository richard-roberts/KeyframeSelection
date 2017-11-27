from typing import List

from src.scene.coordinates.value import Value


class Coordinate:
    def __init__(self, values: List[Value]):
        self.values = values

    def as_point(self):
        point = []
        for value in self.values:
            point.append(value.value)
        return point
